import urllib.request, json
res = json.loads(urllib.request.urlopen('http://localhost:5000/api/evaluate_models').read())
points = res['pca_points']

ag_pts = [p for p in points if p['archetype'] == 'Agriculture-Heavy']
for p in ag_pts:
    print(f"{p['code']:4s} {p['name']:30s} x={p['x']:7.3f} y={p['y']:7.3f}")

