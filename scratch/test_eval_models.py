import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

df = pd.read_csv('clr_transformed_df.csv')
features = ['Energy', 'Industry', 'Transport', 'Agriculture', 'Buildings']
X = df[features].values

results = []

# 1. K-Means (k=2 to 10)
for k in range(2, 11):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X)
    s = silhouette_score(X, labels)
    db = davies_bouldin_score(X, labels)
    ch = calinski_harabasz_score(X, labels)
    results.append({
        'algorithm': 'K-Means',
        'k': k,
        'params': f'k={k}',
        'silhouette': float(s),
        'davies_bouldin': float(db),
        'calinski_harabasz': float(ch)
    })

# 2. Agglomerative (k=2 to 10)
for k in range(2, 11):
    agg = AgglomerativeClustering(n_clusters=k)
    labels = agg.fit_predict(X)
    s = silhouette_score(X, labels)
    db = davies_bouldin_score(X, labels)
    ch = calinski_harabasz_score(X, labels)
    results.append({
        'algorithm': 'Hierarchical (Agglomerative)',
        'k': k,
        'params': f'k={k}',
        'silhouette': float(s),
        'davies_bouldin': float(db),
        'calinski_harabasz': float(ch)
    })

# 3. GMM (k=2 to 10)
for k in range(2, 11):
    gmm = GaussianMixture(n_components=k, random_state=42, n_init=5)
    labels = gmm.fit_predict(X)
    s = silhouette_score(X, labels)
    db = davies_bouldin_score(X, labels)
    ch = calinski_harabasz_score(X, labels)
    results.append({
        'algorithm': 'Gaussian Mixture Model (GMM)',
        'k': k,
        'params': f'k={k}',
        'silhouette': float(s),
        'davies_bouldin': float(db),
        'calinski_harabasz': float(ch)
    })

# 4. DBSCAN
for eps in [0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 1.8, 2.0]:
    for min_samples in [2, 3, 4, 5]:
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(X)
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        if n_clusters >= 2:
            s = silhouette_score(X, labels)
            db_score = davies_bouldin_score(X, labels)
            ch = calinski_harabasz_score(X, labels)
            results.append({
                'algorithm': 'DBSCAN',
                'k': n_clusters,
                'params': f'eps={eps}, min_samples={min_samples}',
                'silhouette': float(s),
                'davies_bouldin': float(db_score),
                'calinski_harabasz': float(ch)
            })

res_df = pd.DataFrame(results)

# Min-Max Normalization:
# Silhouette: higher is better
# Calinski-Harabasz: higher is better
# Davies-Bouldin: lower is better
s_min, s_max = res_df['silhouette'].min(), res_df['silhouette'].max()
db_min, db_max = res_df['davies_bouldin'].min(), res_df['davies_bouldin'].max()
ch_min, ch_max = res_df['calinski_harabasz'].min(), res_df['calinski_harabasz'].max()

res_df['s_norm'] = (res_df['silhouette'] - s_min) / (s_max - s_min) if s_max > s_min else 1.0
res_df['db_norm'] = (db_max - res_df['davies_bouldin']) / (db_max - db_min) if db_max > db_min else 1.0
res_df['ch_norm'] = (res_df['calinski_harabasz'] - ch_min) / (ch_max - ch_min) if ch_max > ch_min else 1.0
res_df['composite_score'] = (res_df['s_norm'] + res_df['db_norm'] + res_df['ch_norm']) / 3.0

res_df = res_df.sort_values(by='composite_score', ascending=False).reset_index(drop=True)

winner = res_df.iloc[0]
print(f"=== ABSOLUTE WINNER BY CONSENSUS ===")
print(f"Algorithm: {winner['algorithm']}")
print(f"Optimal Clusters (k): {winner['k']}")
print(f"Parameters: {winner['params']}")
print(f"Composite Consensus Score: {winner['composite_score']:.4f}")
print(f"Silhouette Score: {winner['silhouette']:.4f} (higher is better)")
print(f"Davies-Bouldin Index: {winner['davies_bouldin']:.4f} (lower is better)")
print(f"Calinski-Harabasz Index: {winner['calinski_harabasz']:.2f} (higher is better)")

print("\n=== TOP CONFIGURATION PER ALGORITHM ===")
for algo in res_df['algorithm'].unique():
    best_algo = res_df[res_df['algorithm'] == algo].iloc[0]
    print(f"{algo:30s} | k={best_algo['k']:2d} ({best_algo['params']:25s}) | Composite={best_algo['composite_score']:.3f} | Sil={best_algo['silhouette']:.3f} | DB={best_algo['davies_bouldin']:.3f} | CH={best_algo['calinski_harabasz']:.1f}")
