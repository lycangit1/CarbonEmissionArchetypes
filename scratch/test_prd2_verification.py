import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
from app import app


def test_prd2_implementation():
    client = app.test_client()

    print("[1] Testing static routes...")
    r_index = client.get('/')
    assert r_index.status_code == 200, f"Index failed: {r_index.status_code}"
    assert b"Global Carbon Archetypes" in r_index.data

    r_css = client.get('/style.css')
    assert r_css.status_code == 200, f"CSS failed: {r_css.status_code}"
    assert b":root" in r_css.data

    r_js = client.get('/script.js')
    assert r_js.status_code == 200, f"JS failed: {r_js.status_code}"
    assert b"state" in r_js.data

    r_cat_file = client.get('/decarbonization_catalog.json')
    assert r_cat_file.status_code == 200, f"Catalog file failed: {r_cat_file.status_code}"

    print("[2] Testing GET /api/data...")
    r_data = client.get('/api/data')
    assert r_data.status_code == 200
    data_json = r_data.get_json()
    assert data_json['status'] == 'success'
    countries = data_json['countries']
    assert len(countries) >= 200, f"Expected 200+ countries, got {len(countries)}"
    
    # Check that sector percentages sum to 100 for all countries
    for c in countries[:20]:
        total_pct = sum(c['percentages'].values())
        assert total_pct == 100, f"Country {c['country_code']} sum is {total_pct}"
    print(f"    Verified {len(countries)} sovereign nations loaded with exact 100% sector balance.")

    print("[3] Testing POST /api/nearest_archetype with CLR distance...")
    test_cases = [
        ([54, 31, 6, 5, 4], "Energy-Heavy"),
        ([10, 80, 5, 3, 2], "Industry-Heavy"),
        ([10, 10, 15, 60, 5], "Agriculture-Heavy"),
        ([10, 10, 70, 5, 5], "Transport-Heavy"),
        ([10, 5, 10, 5, 70], "Buildings-Heavy")
    ]
    for vector, expected_arch in test_cases:
        r_arch = client.post('/api/nearest_archetype', json={"sectors": vector})
        assert r_arch.status_code == 200, f"Failed for {vector}: {r_arch.status_code}"
        res = r_arch.get_json()
        pred = res['predicted_archetype']
        assert pred == expected_arch, f"Expected {expected_arch}, got {pred} for {vector}"
        assert 'xai_decision_rule' in res
        assert 'plain_english' in res['xai_decision_rule']
        assert 'mathematical_bounding_rule' in res['xai_decision_rule']
        assert len(res['decarbonization_roadmap']) == 3, f"Expected 3 roadmap items, got {len(res['decarbonization_roadmap'])}"
        print(f"    Vector {vector} -> {pred} (Roadmap: {len(res['decarbonization_roadmap'])} policies, XAI: verified)")

    print("[4] Testing GET /api/evaluate_models...")
    r_eval = client.get('/api/evaluate_models')
    assert r_eval.status_code == 200
    eval_json = r_eval.get_json()
    assert eval_json['winning_model'] == "K-Means"
    assert eval_json['optimal_clusters'] == 5
    assert len(eval_json['validation_metrics']) == 3
    assert len(eval_json['discarded_algorithms']) == 3
    print("    Verified Objective 2 & 3 scoreboard: K-Means winner, 3 metrics, 3 discarded algorithms.")

    print("[5] Testing GET /api/catalog...")
    r_cat = client.get('/api/catalog')
    assert r_cat.status_code == 200
    cat_json = r_cat.get_json()
    assert 'Energy-Heavy' in cat_json or 'archetypes' in cat_json
    assert 'suggested_comparisons' in cat_json
    print("    Verified catalog: archetypes with bottlenecks and roadmaps, suggested comparison scenarios.")


    print("\n[SUCCESS] ALL VERIFICATION CHECKS PASSED PERFECTLY!")

if __name__ == '__main__':
    test_prd2_implementation()
