import urllib.request, json
res = json.loads(urllib.request.urlopen('http://localhost:5000/api/evaluate_models').read())
points = res['pca_points']
for i, p in enumerate(points):
    try:
        title = f"{p['name']} ({p['code']})"
        x_val = float(p['x'])
        y_val = float(p['y'])
        dom = p['dominant_sector']
        dom_pct = p['dominant_percentage']
        arch = p['archetype']
        clusters = p['clusters']
        hier = clusters['hierarchical']
        gmm = clusters['gmm']
        db = clusters['dbscan']
    except Exception as e:
        print(f"Error on point {i} ({p.get('name')}): {e}")
print("Point validation complete!")

