"""
Global Carbon Emission Archetypes - Data Engineering & Compositional Preprocessing Pipeline
Phase A Target: data_pipeline.py

This module implements:
1. Ingestion of the EDGAR AR5 GHG dataset (1970-2024).
2. Filtering for year 2023 emissions.
3. Removal of Land-Use Change and Forestry (LUCF / LULUCF; IPCC codes starting with 5 or 3B)
   to ensure non-negative emission values.
4. Aggregation of granular IPCC sector categories into exactly 5 macro-sectors:
   - Energy (IPCC 1A1, 1A5, 1B - strictly labeled 'Energy', never 'Electricity')
   - Industry (IPCC 1A2, 2A-2G, 3A-3D)
   - Transport (IPCC 1A3, 1C)
   - Agriculture (IPCC 4A-4G)
   - Buildings (IPCC 1A4)
5. Computation of country-level proportional shares summing to 1.0 (compositional simplex).
6. Zero imputation with delta = 1e-5 to protect logarithmic operations.
7. Centered Log-Ratio (CLR) transformation: ln(x_i / geometric_mean(x)).
8. Generation of clean DataFrames ready for scikit-learn clustering.
"""

import os
import numpy as np
import pandas as pd
from typing import Tuple, Optional


# Exact 5 macro-sector names required by PRD
MACRO_SECTORS = ['Energy', 'Industry', 'Transport', 'Agriculture', 'Buildings']


def map_ipcc_code_to_macro_sector(ipcc_code: str) -> Optional[str]:
    """
    Maps granular IPCC 1996/2006 codes to exactly 5 macro-sectors.
    
    Strict naming convention applied:
    - Sector 1A1 is mapped to 'Energy' (never 'Electricity').
    - Fuel extraction/fugitive emissions (1B) and other energy (1A5) are mapped to 'Energy'.
    - Manufacturing combustion (1A2), industrial processes (2), and solvents (3) are 'Industry'.
    - Domestic transport (1A3) and international transport (1C) are 'Transport'.
    - Residential and commercial combustion (1A4) are 'Buildings'.
    - Agricultural activities (4 in 1996, 3A/3C in 2006) are 'Agriculture'.
    - Waste (6) and Other (7) are excluded from the 5 structural macro-sectors.
    """
    code = str(ipcc_code).strip()
    
    # 1. Energy Industries (1A1), Fugitive emissions (1B), and Other Energy (1A5)
    if code.startswith(('1A1', '1.A.1', '1A5', '1.A.5', '1B', '1.B')):
        return 'Energy'
    
    # 2. Industry: Manufacturing (1A2), Industrial Processes (2), Solvents (3)
    elif code.startswith(('1A2', '1.A.2', '2', '3A', '3C', '3D')):
        return 'Industry'
    
    # 3. Transport: Domestic transport (1A3) and International aviation/shipping (1C)
    elif code.startswith(('1A3', '1.A.3', '1C', '1.C')):
        return 'Transport'
    
    # 4. Buildings: Residential, commercial, and institutional (1A4)
    elif code.startswith(('1A4', '1.A.4')):
        return 'Buildings'
    
    # 5. Agriculture: Agricultural livestock, soils, burning (4 in 1996, 3.A/3.C in 2006)
    elif code.startswith(('4', '3.A', '3.C', '3A.1', '3A.2', '3C')):
        return 'Agriculture'
    
    return None


def load_and_filter_edgar_data(
    filepath: str = 'EDGAR_AR5_GHG_1970_2024.xlsx',
    sheet_name: str = 'IPCC 1996',
    year: int = 2023,
    drop_bunkers: bool = False
) -> pd.DataFrame:
    """
    Loads raw EDGAR emissions Excel dataset, isolates the target year,
    and drops Land-Use Change and Forestry rows (codes starting with 5 or 3B).
    
    Parameters:
    -----------
    filepath : str
        Path to the EDGAR Excel file.
    sheet_name : str
        Sheet containing IPCC emissions ('IPCC 1996' or 'IPCC 2006').
    year : int
        Target analysis year (default: 2023).
    drop_bunkers : bool
        Whether to drop international bunker fuel entities ('AIR' and 'SEA').
        
    Returns:
    --------
    pd.DataFrame: Filtered dataset for the target year.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at {filepath}")
    
    # Header is at row index 9 (skiprows=9)
    df = pd.read_excel(filepath, sheet_name=sheet_name, skiprows=9)
    
    year_col = f'Y_{year}'
    if year_col not in df.columns:
        raise KeyError(f"Year column '{year_col}' not found in dataset columns.")
    
    # Determine the sector code column
    sector_col = None
    for col_candidate in ['ipcc_code_1996_for_standard_report', 'ipcc_code_2006_for_standard_report', 'IPCC']:
        if col_candidate in df.columns:
            sector_col = col_candidate
            break
            
    if sector_col is None:
        raise KeyError("Could not locate IPCC sector code column in sheet.")
    
    # Filtering Requirement:
    # Drop all rows associated with "Land-Use Change and Forestry" (IPCC codes starting with 5 or 3B)
    lucf_mask = df[sector_col].astype(str).str.strip().str.startswith(('5', '3B', '3.B'))
    filtered_df = df[~lucf_mask].copy()
    
    # Optional filter for international aviation/shipping bunker entities
    if drop_bunkers and 'Country_code_A3' in filtered_df.columns:
        filtered_df = filtered_df[~filtered_df['Country_code_A3'].isin(['AIR', 'SEA'])].copy()
        
    return filtered_df


def aggregate_macro_sectors(
    df: pd.DataFrame,
    year: int = 2023
) -> pd.DataFrame:
    """
    Aggregates granular IPCC codes into the 5 specified macro-sectors
    and sums annual emissions per country.
    
    Returns:
    --------
    pd.DataFrame: Country x Macro-Sector emissions in Gg CO2eq.
    """
    sector_col = [c for c in df.columns if 'ipcc_code' in c.lower()][0]
    year_col = f'Y_{year}'
    
    df_mapped = df.copy()
    df_mapped['Macro_Sector'] = df_mapped[sector_col].apply(map_ipcc_code_to_macro_sector)
    
    # Drop unmapped sectors (e.g. Waste 6, Other 7)
    df_mapped = df_mapped.dropna(subset=['Macro_Sector'])
    
    # Aggregate emissions by Country and Macro-Sector
    pivot_df = df_mapped.groupby(
        ['Country_code_A3', 'Name', 'Macro_Sector'],
        as_index=False
    )[year_col].sum()
    
    country_sector_df = pivot_df.pivot(
        index=['Country_code_A3', 'Name'],
        columns='Macro_Sector',
        values=year_col
    ).fillna(0.0)
    
    # Enforce standard column ordering
    country_sector_df = country_sector_df.reindex(columns=MACRO_SECTORS, fill_value=0.0)
    
    return country_sector_df


def compute_compositional_proportions(
    emissions_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Computes proportional shares per country across the 5 macro-sectors
    such that each row sums to 1.0 (constrained simplex).
    
    Returns:
    --------
    pd.DataFrame: Proportional sector shares [0.0 - 1.0].
    """
    row_totals = emissions_df.sum(axis=1)
    
    # Protect against any zero totals
    zero_countries = row_totals[row_totals == 0].index.tolist()
    if zero_countries:
        print(f"Warning: {len(zero_countries)} countries have 0 total emissions across 5 sectors.")
        row_totals = row_totals.replace(0, np.nan)
        
    proportions_df = emissions_df.div(row_totals, axis=0)
    return proportions_df


def clr_transformation(
    proportions_df: pd.DataFrame,
    eps: float = 1e-5
) -> pd.DataFrame:
    """
    Applies the Centered Log-Ratio (CLR) transformation to compositional data:
        clr(x_i) = ln(x_i / geometric_mean(x)) = ln(x_i) - (1/D) * sum(ln(x_j))
        
    Mathematical properties:
    - Overcomes the simplex constraint, enabling Euclidean distance algorithms (K-Means, PCA).
    - Preserves subcompositional coherence.
    - Each country row in CLR space sums to 0.0.
    
    Parameters:
    -----------
    proportions_df : pd.DataFrame
        Matrix of proportional shares (summing to 1.0).
    eps : float
        Replacement value for absolute zeros (default: 1e-5) to protect log function.
        
    Returns:
    --------
    pd.DataFrame: Centered Log-Ratio transformed coordinates.
    """
    # Impute absolute zeros with eps (1e-5)
    imputed_props = proportions_df.copy()
    imputed_props = imputed_props.clip(lower=eps)
    
    # Compute natural logarithm of proportions
    log_x = np.log(imputed_props)
    
    # Compute geometric mean logarithm per country: (1/D) * sum(ln(x_j))
    log_geom_mean = log_x.mean(axis=1)
    
    # CLR: ln(x_i) - ln(geometric_mean)
    clr_transformed_df = log_x.sub(log_geom_mean, axis=0)
    
    return clr_transformed_df


def run_pipeline(
    filepath: str = 'EDGAR_AR5_GHG_1970_2024.xlsx',
    year: int = 2023,
    save_outputs: bool = True
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Executes the full Phase A compositional preprocessing pipeline.
    
    Returns:
    --------
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        - clr_transformed_df: CLR-transformed coordinates ready for scikit-learn.
        - proportions_df: Proportional shares summing to 1.0.
        - raw_emissions_df: Absolute emissions in Gg CO2eq.
    """
    print(f"[*] Ingesting and filtering EDGAR dataset for year {year}...")
    filtered_raw = load_and_filter_edgar_data(filepath, sheet_name='IPCC 1996', year=year)
    
    print("[*] Aggregating granular IPCC codes into 5 macro-sectors (Energy, Industry, Transport, Agriculture, Buildings)...")
    raw_emissions_df = aggregate_macro_sectors(filtered_raw, year=year)
    
    print("[*] Computing compositional proportional shares (sum to 1.0)...")
    proportions_df = compute_compositional_proportions(raw_emissions_df)
    
    print("[*] Applying Centered Log-Ratio (CLR) transformation with 1e-5 zero imputation...")
    clr_transformed_df = clr_transformation(proportions_df, eps=1e-5)
    
    if save_outputs:
        clr_transformed_df.to_csv('clr_transformed_df.csv')
        proportions_df.to_csv('proportions_df.csv')
        raw_emissions_df.to_csv('macro_sector_emissions_df.csv')
        print("[+] Processed datasets saved to disk: clr_transformed_df.csv, proportions_df.csv, macro_sector_emissions_df.csv")
        
    return clr_transformed_df, proportions_df, raw_emissions_df


if __name__ == '__main__':
    clr_df, props_df, raw_df = run_pipeline()
    
    print("\n" + "="*80)
    print("PHASE A EXECUTION COMPLETE")
    print("="*80)
    print(f"Total Country Count: {len(clr_df)}")
    print("\nFirst five rows of clr_transformed_df:")
    print(clr_df.head(5).to_string())
    print("="*80)
