"""
Global Carbon Emission Archetypes - Multi-Algorithm Benchmarking
Phase B Target: model_training.py

This module implements:
1. Loading the CLR-transformed feature matrix (clr_transformed_df.csv).
2. Multi-algorithm benchmarking across 4 unsupervised clustering algorithms:
   - K-Means (k = 3 to 8)
   - Gaussian Mixture Models (k = 3 to 8)
   - Agglomerative (Hierarchical) Clustering (k = 3 to 8)
   - DBSCAN (Grid search across eps in [0.2, 1.5] and min_samples in [2, 5])
3. Rigorous validation metric computation for every configuration:
   - Silhouette Score (higher is better, [-1, 1])
   - Davies-Bouldin Index (lower is better, [0, inf))
   - Calinski-Harabasz Index (higher is better, [0, inf))
4. Ranking the top configuration for each algorithm.
5. Programmatic selection of the overall winner based on the highest Silhouette Score (Zero-Guessing Validation).
6. Appending winning cluster labels to proportions_df.csv and saving final_clustered_proportions.csv.
"""

import os
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any

from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score


FEATURE_COLUMNS = ['Energy', 'Industry', 'Transport', 'Agriculture', 'Buildings']


def load_clr_data(filepath: str = 'clr_transformed_df.csv') -> Tuple[pd.DataFrame, np.ndarray]:
    """
    Loads CLR-transformed features from CSV.
    
    Returns:
    --------
    Tuple[pd.DataFrame, np.ndarray]:
        - clr_df: Full DataFrame including metadata (Country_code_A3, Name).
        - X: (N, 5) numpy array of CLR feature coordinates.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}. Run data_pipeline.py first.")
        
    clr_df = pd.read_csv(filepath)
    missing_cols = [c for c in FEATURE_COLUMNS if c not in clr_df.columns]
    if missing_cols:
        raise ValueError(f"Missing required feature columns in {filepath}: {missing_cols}")
        
    X = clr_df[FEATURE_COLUMNS].values
    return clr_df, X


def benchmark_kmeans(X: np.ndarray, k_range: range = range(3, 9)) -> List[Dict[str, Any]]:
    """Evaluates K-Means across specified range of k."""
    results = []
    for k in k_range:
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = model.fit_predict(X)
        sil = float(silhouette_score(X, labels))
        db = float(davies_bouldin_score(X, labels))
        ch = float(calinski_harabasz_score(X, labels))
        results.append({
            'Algorithm': 'K-Means',
            'Config': f'k={k}',
            'k': k,
            'Silhouette': sil,
            'Davies-Bouldin': db,
            'Calinski-Harabasz': ch,
            'Model': model,
            'Labels': labels
        })
    return results


def benchmark_gmm(X: np.ndarray, k_range: range = range(3, 9)) -> List[Dict[str, Any]]:
    """Evaluates Gaussian Mixture Models across specified range of k."""
    results = []
    for k in k_range:
        model = GaussianMixture(n_components=k, random_state=42)
        labels = model.fit_predict(X)
        sil = float(silhouette_score(X, labels))
        db = float(davies_bouldin_score(X, labels))
        ch = float(calinski_harabasz_score(X, labels))
        results.append({
            'Algorithm': 'Gaussian Mixture Models (GMM)',
            'Config': f'k={k}',
            'k': k,
            'Silhouette': sil,
            'Davies-Bouldin': db,
            'Calinski-Harabasz': ch,
            'Model': model,
            'Labels': labels
        })
    return results


def benchmark_agglomerative(X: np.ndarray, k_range: range = range(3, 9)) -> List[Dict[str, Any]]:
    """Evaluates Agglomerative (Hierarchical) Clustering across specified range of k."""
    results = []
    for k in k_range:
        model = AgglomerativeClustering(n_clusters=k)
        labels = model.fit_predict(X)
        sil = float(silhouette_score(X, labels))
        db = float(davies_bouldin_score(X, labels))
        ch = float(calinski_harabasz_score(X, labels))
        results.append({
            'Algorithm': 'Agglomerative (Hierarchical)',
            'Config': f'k={k}',
            'k': k,
            'Silhouette': sil,
            'Davies-Bouldin': db,
            'Calinski-Harabasz': ch,
            'Model': model,
            'Labels': labels
        })
    return results


def benchmark_dbscan(
    X: np.ndarray,
    eps_values: np.ndarray = np.round(np.arange(0.2, 1.55, 0.1), 2),
    min_samples_values: List[int] = [2, 3, 4, 5]
) -> List[Dict[str, Any]]:
    """
    Grid-searches DBSCAN over eps and min_samples.
    Only retains runs that produce at least 2 distinct non-noise clusters.
    """
    results = []
    for eps in eps_values:
        for ms in min_samples_values:
            model = DBSCAN(eps=eps, min_samples=ms)
            labels = model.fit_predict(X)
            
            # Non-noise clusters count
            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            n_noise = int((labels == -1).sum())
            
            # Ensure valid multi-cluster configuration (>= 2 dense clusters)
            if n_clusters >= 2:
                try:
                    sil = float(silhouette_score(X, labels))
                    db = float(davies_bouldin_score(X, labels))
                    ch = float(calinski_harabasz_score(X, labels))
                    results.append({
                        'Algorithm': 'DBSCAN',
                        'Config': f'eps={eps}, min_samples={ms} (clusters={n_clusters}, noise={n_noise})',
                        'k': n_clusters,
                        'Silhouette': sil,
                        'Davies-Bouldin': db,
                        'Calinski-Harabasz': ch,
                        'Model': model,
                        'Labels': labels,
                        'n_noise': n_noise
                    })
                except Exception:
                    pass
    return results


def run_benchmarking(
    clr_filepath: str = 'clr_transformed_df.csv',
    proportions_filepath: str = 'proportions_df.csv',
    output_filepath: str = 'final_clustered_proportions.csv'
) -> Tuple[pd.DataFrame, Dict[str, Any], pd.DataFrame]:
    """
    Executes Phase B multi-algorithm benchmarking and programmatically selects the winner.
    """
    print("[*] Loading CLR-transformed dataset...")
    clr_df, X = load_clr_data(clr_filepath)
    print(f"    Loaded {len(clr_df)} observations with 5 macro-sector features.")
    
    print("\n[*] Benchmarking Algorithm 1: K-Means (k=3 to 8)...")
    km_res = benchmark_kmeans(X)
    
    print("[*] Benchmarking Algorithm 2: Gaussian Mixture Models (GMM) (k=3 to 8)...")
    gmm_res = benchmark_gmm(X)
    
    print("[*] Benchmarking Algorithm 3: Agglomerative (Hierarchical) Clustering (k=3 to 8)...")
    agg_res = benchmark_agglomerative(X)
    
    print("[*] Benchmarking Algorithm 4: DBSCAN (eps=0.2 to 1.5, min_samples=2 to 5)...")
    db_res = benchmark_dbscan(X)
    
    all_runs = km_res + gmm_res + agg_res + db_res
    df_all = pd.DataFrame([{k: v for k, v in r.items() if k not in ['Model', 'Labels']} for r in all_runs])
    df_all.to_csv('clustering_benchmark_all_runs.csv', index=False)
    
    # Identify top configuration per algorithm based on highest Silhouette Score
    top_per_algorithm = []
    for algo in ['K-Means', 'Gaussian Mixture Models (GMM)', 'Agglomerative (Hierarchical)', 'DBSCAN']:
        algo_runs = [r for r in all_runs if r['Algorithm'] == algo]
        if algo_runs:
            best_algo_run = max(algo_runs, key=lambda x: x['Silhouette'])
            top_per_algorithm.append(best_algo_run)
            
    top_ranking_df = pd.DataFrame([{
        'Algorithm': r['Algorithm'],
        'Optimal Configuration': r['Config'],
        'Silhouette Score': r['Silhouette'],
        'Davies-Bouldin Index': r['Davies-Bouldin'],
        'Calinski-Harabasz Index': r['Calinski-Harabasz']
    } for r in top_per_algorithm]).sort_values('Silhouette Score', ascending=False).reset_index(drop=True)
    
    # Programmatically select overall winner
    overall_winner = max(all_runs, key=lambda x: x['Silhouette'])
    
    print(f"\n[+] Programmatic Winner Selected: {overall_winner['Algorithm']} ({overall_winner['Config']})")
    print(f"    Highest Silhouette Score: {overall_winner['Silhouette']:.4f}")
    
    # Append winning labels to proportions DataFrame
    proportions_df = pd.read_csv(proportions_filepath)
    proportions_df['Cluster'] = overall_winner['Labels']
    
    # Save final clustered proportions
    proportions_df.to_csv(output_filepath, index=False)
    print(f"[+] Winning cluster labels saved to: {output_filepath}")
    
    # Save summary metadata for Phase C / Flask server
    summary = {
        'winner_algorithm': overall_winner['Algorithm'],
        'winner_config': overall_winner['Config'],
        'silhouette_score': overall_winner['Silhouette'],
        'davies_bouldin_index': overall_winner['Davies-Bouldin'],
        'calinski_harabasz_index': overall_winner['Calinski-Harabasz'],
        'total_countries': len(proportions_df),
        'cluster_counts': {str(k): int(v) for k, v in pd.Series(overall_winner['Labels']).value_counts().items()}
    }
    with open('model_training_summary.json', 'w') as f:
        json.dump(summary, f, indent=4)
        
    return top_ranking_df, overall_winner, proportions_df


if __name__ == '__main__':
    top_table, winner, clustered_df = run_benchmarking()
    
    print("\n" + "="*95)
    print("PHASE B: MULTI-ALGORITHM BENCHMARKING RESULTS")
    print("="*95)
    try:
        print(top_table.to_markdown(index=False))
    except Exception:
        # Fallback manual markdown generator
        headers = list(top_table.columns)
        print("| " + " | ".join(headers) + " |")
        print("| " + " | ".join(["---"] * len(headers)) + " |")
        for _, row in top_table.iterrows():
            print("| " + " | ".join([f"{v:.4f}" if isinstance(v, float) else str(v) for v in row]) + " |")
    print("="*95)
    print(f"Overall Winner: {winner['Algorithm']} | {winner['Config']}")
    print(f"Max Silhouette Score: {winner['Silhouette']:.4f}")
    print("="*95)
    print(f"First 5 rows of final_clustered_proportions.csv:")
    print(clustered_df.head(5).to_string())
    print("="*95)
