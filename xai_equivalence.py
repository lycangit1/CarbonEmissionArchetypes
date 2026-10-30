"""
Global Carbon Emission Archetypes - Explainable AI (XAI) & Equivalence Analysis
Phase C Target: xai_equivalence.py

This module implements:
1. Loading final clustered proportions (final_clustered_proportions.csv) and absolute sector emissions (macro_sector_emissions_df.csv).
2. Training a surrogate DecisionTreeClassifier (max_depth=3) on the 5 sector proportions to model cluster boundaries.
3. Extracting human-readable bounding-box rules in plain English (e.g. "IF Energy > 2.1% AND Buildings > 0.1%").
4. Calculating the mean proportional centroids for each cluster and assigning structural archetype names:
   - Cluster 0: "Energy-Dominant Economies" (strict PRD requirement)
   - Cluster 1: "Agriculture-Dominant Economies"
   - Cluster 2: "Industry-Dominant Micro-Economies"
   - Cluster -1: "Outlier / Specialized Transit Economies"
5. Implementing the exact PRD Equivalence Measure for diverse countries:
   - Delta E_target = Benchmark % Reduction * Country Total Emissions
   - Sector Activity Cut = Delta E_target / Dominant Sector Baseline Emissions
6. Saving results to xai_equivalence_results.json for frontend dashboard consumption.
"""

import os
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Any
from sklearn.tree import DecisionTreeClassifier, _tree


MACRO_SECTORS = ['Energy', 'Industry', 'Transport', 'Agriculture', 'Buildings']

# Structural naming aligned with PRD conventions
ARCHETYPE_NAMES = {
    0: "Energy-Dominant Economies",
    1: "Agriculture-Dominant Economies",
    2: "Industry-Dominant Micro-Economies",
    -1: "Outlier / Specialized Transit Economies"
}


def load_datasets(
    clustered_path: str = 'final_clustered_proportions.csv',
    emissions_path: str = 'macro_sector_emissions_df.csv'
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Loads proportions and absolute emissions, merging on country identifiers."""
    if not os.path.exists(clustered_path):
        raise FileNotFoundError(f"Missing {clustered_path}. Run model_training.py first.")
    if not os.path.exists(emissions_path):
        raise FileNotFoundError(f"Missing {emissions_path}. Run data_pipeline.py first.")
        
    prop_df = pd.read_csv(clustered_path)
    emiss_df = pd.read_csv(emissions_path)
    
    # Merge datasets
    merged_df = pd.merge(
        prop_df,
        emiss_df,
        on=['Country_code_A3', 'Name'],
        suffixes=('_share', '_emissions')
    )
    return prop_df, emiss_df, merged_df


def train_surrogate_decision_tree(
    prop_df: pd.DataFrame,
    max_depth: int = 3
) -> Tuple[DecisionTreeClassifier, float]:
    """
    Trains an interpretable surrogate DecisionTreeClassifier to extract
    rule-based bounding boxes separating the clusters.
    """
    X = prop_df[MACRO_SECTORS].values
    y = prop_df['Cluster'].values
    
    dt = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    dt.fit(X, y)
    accuracy = float(dt.score(X, y))
    return dt, accuracy


def extract_plain_english_rules(
    tree_model: DecisionTreeClassifier,
    feature_names: List[str]
) -> List[Dict[str, Any]]:
    """
    Traverses the DecisionTree to generate human-readable bounding-box rules.
    """
    tree_ = tree_model.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    
    rules = []
    
    def recurse(node: int, conditions: List[str]):
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            # Left branch: feature <= threshold
            recurse(tree_.children_left[node], conditions + [f"{name} <= {threshold*100:.1f}%"])
            # Right branch: feature > threshold
            recurse(tree_.children_right[node], conditions + [f"{name} > {threshold*100:.1f}%"])
        else:
            # Leaf node
            val = tree_.value[node][0]
            pred_class_idx = int(np.argmax(val))
            cluster_id = int(tree_model.classes_[pred_class_idx])
            n_samples = int(tree_.n_node_samples[node])
            archetype_name = ARCHETYPE_NAMES.get(cluster_id, f"Cluster {cluster_id}")
            
            rule_text = "IF " + " AND ".join(conditions) + f" THEN Classify as {archetype_name} (Cluster {cluster_id})"
            rules.append({
                'cluster_id': cluster_id,
                'archetype_name': archetype_name,
                'sample_count': n_samples,
                'conditions': conditions,
                'rule_text': rule_text
            })
            
    recurse(0, [])
    return rules


def compute_cluster_centroids(prop_df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """
    Calculates the mean proportional profile for each cluster and formats structural descriptions.
    """
    centroids = {}
    grouped = prop_df.groupby('Cluster')[MACRO_SECTORS].mean()
    counts = prop_df['Cluster'].value_counts().to_dict()
    
    for cluster_id in sorted(grouped.index):
        c_id = int(cluster_id)
        arch_name = ARCHETYPE_NAMES.get(c_id, f"Cluster {c_id}")
        shares = {sec: float(round(grouped.loc[cluster_id, sec], 4)) for sec in MACRO_SECTORS}
        
        # Identify dominant sector in centroid
        dominant_sec = max(shares, key=shares.get)
        
        centroids[str(c_id)] = {
            'cluster_id': c_id,
            'archetype_name': arch_name,
            'country_count': int(counts.get(cluster_id, 0)),
            'dominant_sector': dominant_sec,
            'mean_proportions': shares
        }
    return centroids


def calculate_equivalence_measure(
    merged_df: pd.DataFrame,
    country_codes: List[str],
    benchmark_pct: float = 0.05
) -> List[Dict[str, Any]]:
    """
    Implements the PRD Equivalence Measure:
        Delta E_target = Benchmark % Reduction * Country Total Emissions
        Sector Activity Cut = Delta E_target / Dominant Sector Baseline Emissions
    """
    results = []
    
    for code in country_codes:
        country_rows = merged_df[merged_df['Country_code_A3'] == code]
        if country_rows.empty:
            print(f"Warning: Country code {code} not found in dataset.")
            continue
            
        row = country_rows.iloc[0]
        
        # Extract emissions and shares
        emissions = {sec: float(row[f"{sec}_emissions"]) for sec in MACRO_SECTORS}
        shares = {sec: float(row[f"{sec}_share"]) for sec in MACRO_SECTORS}
        
        total_emissions = float(sum(emissions.values()))
        
        # Dominant sector: sector with largest absolute emissions / share
        dominant_sector = max(emissions, key=emissions.get)
        dominant_baseline = emissions[dominant_sector]
        dominant_share = shares[dominant_sector]
        
        # PRD Mathematical Formulas
        delta_e_target = benchmark_pct * total_emissions
        sector_activity_cut = (delta_e_target / dominant_baseline) if dominant_baseline > 0 else 0.0
        
        cluster_id = int(row['Cluster'])
        arch_name = ARCHETYPE_NAMES.get(cluster_id, f"Cluster {cluster_id}")
        
        results.append({
            'country_code': code,
            'country_name': str(row['Name']),
            'cluster_id': cluster_id,
            'archetype_name': arch_name,
            'benchmark_reduction_pct': float(benchmark_pct * 100),
            'country_total_emissions_Gg': float(round(total_emissions, 2)),
            'dominant_sector': dominant_sector,
            'dominant_sector_baseline_emissions_Gg': float(round(dominant_baseline, 2)),
            'dominant_sector_share_pct': float(round(dominant_share * 100, 2)),
            'delta_e_target_Gg': float(round(delta_e_target, 2)),
            'sector_activity_cut_pct': float(round(sector_activity_cut * 100, 2))
        })
        
    return results


def run_xai_and_equivalence(
    output_json_path: str = 'xai_equivalence_results.json'
) -> Dict[str, Any]:
    """Runs Phase C pipeline end-to-end and exports results to JSON."""
    print("[*] Loading final clustered proportions and emissions datasets...")
    prop_df, emiss_df, merged_df = load_datasets()
    
    print("[*] Training surrogate DecisionTreeClassifier (max_depth=3)...")
    tree_model, accuracy = train_surrogate_decision_tree(prop_df, max_depth=3)
    print(f"    Surrogate Tree Classification Accuracy: {accuracy*100:.2f}%")
    
    print("[*] Extracting plain-English bounding-box rules...")
    rules = extract_plain_english_rules(tree_model, MACRO_SECTORS)
    
    print("[*] Calculating mean proportional cluster centroids...")
    centroids = compute_cluster_centroids(prop_df)
    
    print("[*] Calculating Equivalence Measures for diverse benchmark countries...")
    # Select diverse countries across different clusters:
    # 1. USA (Cluster 0: Energy-Dominant)
    # 2. ASM (Cluster 1: Agriculture-Dominant)
    # 3. SGP (Cluster -1: Outlier / Specialized Transit)
    # 4. MHL (Cluster 2: Industry-Dominant Micro-Economy)
    benchmark_countries = ['USA', 'ASM', 'SGP', 'MHL']
    equivalence_results = calculate_equivalence_measure(merged_df, benchmark_countries, benchmark_pct=0.05)
    
    payload = {
        'surrogate_tree_accuracy': accuracy,
        'features': MACRO_SECTORS,
        'archetype_names': ARCHETYPE_NAMES,
        'cluster_centroids': centroids,
        'xai_rules': rules,
        'equivalence_calculations': equivalence_results
    }
    
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=4)
        
    print(f"[+] XAI and Equivalence results successfully saved to: {output_json_path}")
    return payload


if __name__ == '__main__':
    results = run_xai_and_equivalence()
    
    print("\n" + "="*95)
    print("PHASE C: EXPLAINABLE AI (XAI) - EXTRACTED BOUNDING-BOX RULES")
    print("="*95)
    for i, r in enumerate(results['xai_rules'], 1):
        print(f"Rule {i:02d} (n={r['sample_count']:3d}): {r['rule_text']}")
        
    print("\n" + "="*95)
    print("PHASE C: EQUIVALENCE MEASURE OUTPUT (5.0% BENCHMARK REDUCTION)")
    print("="*95)
    eq_df = pd.DataFrame(results['equivalence_calculations'])
    display_cols = [
        'country_code', 'country_name', 'archetype_name',
        'dominant_sector', 'dominant_sector_share_pct',
        'country_total_emissions_Gg', 'delta_e_target_Gg',
        'sector_activity_cut_pct'
    ]
    
    # Try markdown print with fallback
    try:
        print(eq_df[display_cols].to_markdown(index=False))
    except Exception:
        print(eq_df[display_cols].to_string(index=False))
    print("="*95)
