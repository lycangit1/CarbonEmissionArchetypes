import urllib.request
import json

# 1. Test index.html
with urllib.request.urlopen('http://localhost:5000/') as res:
    html = res.read().decode('utf-8')
    assert 'plotly-2.35.2.min.js' in html, 'Plotly CDN missing'
    assert 'pca-3d-plot' in html, 'pca-3d-plot container missing'
    assert 'Objective 2 & 3:' not in html, 'Old objective prefix still present'
    assert 'Multi-algorithm evaluation across internal cluster validation indices' in html, 'Subtitle mismatch'
    assert 'Centered Log-Ratio (CLR)' in html, 'Winner text mismatch'
    assert 'Validation Metrics Comparison Table' in html, 'Metrics table missing'
    print('[PASSED] index.html content verified.')

# 2. Test style.css
with urllib.request.urlopen('http://localhost:5000/style.css') as res:
    css = res.read().decode('utf-8')
    assert 'padding: 1.2rem 1rem;' in css, 'Table padding missing'
    assert 'max-width: 320px;' in css, 'Column width constraint missing'
    assert 'margin-bottom: 3rem;' in css, 'Winner card margin missing'
    assert '.pca-plot-container' in css, 'PCA CSS missing'
    print('[PASSED] style.css verified.')

# 3. Test script.js
with urllib.request.urlopen('http://localhost:5000/script.js') as res:
    js = res.read().decode('utf-8')
    assert 'init3DPcaVisualizer' in js, 'init3DPcaVisualizer missing'
    assert 'Plotly.animate' in js, 'Plotly.animate missing'
    assert 'PCA_ALGO_META' in js, 'PCA_ALGO_META missing'
    print('[PASSED] script.js verified.')

# 4. Test /api/evaluate_models
with urllib.request.urlopen('http://localhost:5000/api/evaluate_models') as res:
    data = json.loads(res.read().decode('utf-8'))
    assert 'pca_points' in data and len(data['pca_points']) == 225, 'PCA points length mismatch'
    assert 'pca_explained_variance' in data, 'PCA explained variance missing'
    assert 'validation_metrics' in data, 'Validation metrics missing'
    print(f'[PASSED] /api/evaluate_models returned {len(data["pca_points"])} points with variance {data["pca_explained_variance"]}.')

print('ALL AUTOMATED VERIFICATION CHECKS PASSED SUCCESSFULLY!')
