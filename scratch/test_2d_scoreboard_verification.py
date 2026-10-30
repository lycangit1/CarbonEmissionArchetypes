import urllib.request
import json

print("=== STARTING 2D SCOREBOARD VERIFICATION ===")

# 1. Test index.html
with urllib.request.urlopen("http://localhost:5000/") as res:
    html = res.read().decode("utf-8")
    assert "plotly" not in html.lower(), "Plotly still found in index.html!"
    assert "pca-3d-plot" not in html, "3D plot container still found in index.html!"
    assert "kmeans-2d-canvas" in html, "kmeans-2d-canvas missing from index.html"
    assert "dbscan-2d-canvas" in html, "dbscan-2d-canvas missing from index.html"
    assert "silhouette-bar-canvas" in html, "silhouette-bar-canvas missing from index.html"
    assert "Objective 2 & 3:" not in html, "'Objective 2 & 3:' found in header"
    assert "Multi-algorithm evaluation across internal cluster validation indices to objectively determine optimal grouping without human labeling bias." in html, "Subtitle mismatch"
    assert "K-Means: 5 Distinct Economic Groups" in html, "Left map title missing"
    assert "DBSCAN: Failed (Undivided Noise)" in html, "Right map title missing"
    assert "discarded-model-toggles" in html, "discarded-model-toggles missing"
    assert "Silhouette Score Comparison (Higher is Better)" in html, "Silhouette bar chart title missing"
    assert "Centered Log-Ratio (CLR)" in html, "CLR explanation text missing"
    print("[PASSED] index.html structure and texts verified.")

# 2. Test style.css
with urllib.request.urlopen("http://localhost:5000/style.css") as res:
    css = res.read().decode("utf-8")
    assert ".pca-plot-container" not in css, "Old 3D PCA CSS still in style.css"
    assert ".cluster-comparison-section" in css, ".cluster-comparison-section missing"
    assert ".cluster-maps-grid" in css, ".cluster-maps-grid missing"
    assert ".silhouette-chart-card" in css, ".silhouette-chart-card missing"
    assert "padding: 1.2rem 1rem;" in css, "Table padding: 1.2rem 1rem missing"
    assert "max-width: 320px;" in css, "Column 3 max-width: 320px missing"
    assert "margin-bottom: 3rem;" in css, "Card spacing margin-bottom: 3rem missing"
    print("[PASSED] style.css 2D and table rules verified.")

# 3. Test script.js
with urllib.request.urlopen("http://localhost:5000/script.js") as res:
    js = res.read().decode("utf-8")
    assert "Plotly" not in js, "Plotly still referenced in script.js"
    assert "render2DClusterMaps" in js, "render2DClusterMaps function missing"
    assert "renderSilhouetteBarChart" in js, "renderSilhouetteBarChart function missing"
    assert "kmeans2DChart" in js, "kmeans2DChart missing in state"
    assert "dbscan2DChart" in js, "dbscan2DChart missing in state"
    assert "silhouetteChart" in js, "silhouetteChart missing in state"
    print("[PASSED] script.js 2D Chart.js logic verified.")

# 4. Test /api/evaluate_models
with urllib.request.urlopen("http://localhost:5000/api/evaluate_models") as res:
    data = json.loads(res.read().decode("utf-8"))
    assert "validation_metrics" in data, "validation_metrics missing in API"
    assert "pca_points" in data and len(data["pca_points"]) == 225, "pca_points count mismatch"
    sil_metric = next(m for m in data["validation_metrics"] if "Silhouette" in m["metric_name"])
    assert sil_metric["kmeans_score"] == 0.479, "K-Means silhouette score mismatch"
    print(f"[PASSED] /api/evaluate_models verified with {len(data['pca_points'])} data points.")

print("=== ALL VERIFICATION CHECKS PASSED SUCCESSFULLY! ===")
