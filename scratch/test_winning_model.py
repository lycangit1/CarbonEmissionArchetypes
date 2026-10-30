import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

clr_df = pd.read_csv('clr_transformed_df.csv')
MACRO_SECTORS = ['Energy', 'Industry', 'Transport', 'Agriculture', 'Buildings']
X = clr_df[MACRO_SECTORS].values

# Fit winning model: KMeans k=2
km2 = KMeans(n_clusters=2, random_state=42, n_init=10).fit(X)
print("Centroids k=2:")
print(km2.cluster_centers_)

# Test a country: China baseline [48, 28, 8, 11, 5]
p = np.array([48, 28, 8, 11, 5], dtype=float)
p = p / p.sum()
log_p = np.log(np.clip(p, 1e-5, None))
clr = log_p - log_p.mean()

dists = [np.linalg.norm(clr - c) for c in km2.cluster_centers_]
print("Distances:", dists)
print("Predicted cluster:", np.argmin(dists))

# Test agrarian country: [0, 5, 0, 95, 0]
p_agri = np.array([0, 5, 0, 95, 0], dtype=float)
p_agri = p_agri / p_agri.sum()
clr_agri = np.log(np.clip(p_agri, 1e-5, None)) - np.log(np.clip(p_agri, 1e-5, None)).mean()
dists_agri = [np.linalg.norm(clr_agri - c) for c in km2.cluster_centers_]
print("Agrarian distances:", dists_agri)
print("Agrarian predicted cluster:", np.argmin(dists_agri))
