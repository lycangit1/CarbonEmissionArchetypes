import urllib.request
import json

print("=== STARTING ABOUT/HISTORY SECTION VERIFICATION ===")

# 1. Test index.html
with urllib.request.urlopen("http://localhost:5000/") as res:
    html = res.read().decode("utf-8")
    
    # Check Selector Lights Navigation
    assert "selector-lights-track" in html, "selector-lights-track missing"
    assert "about-tab-btn" in html, "about-tab-btn missing"
    assert "selector-light-dot" in html, "selector-light-dot missing"
    
    # Check 5 Tabs
    assert 'data-tab="tab-panel-problem"' in html, "Tab 1 problem button missing"
    assert 'data-tab="tab-panel-methodology"' in html, "Tab 2 methodology button missing"
    assert 'data-tab="tab-panel-archetypes"' in html, "Tab 3 archetypes button missing"
    assert 'data-tab="tab-panel-data"' in html, "Tab 4 data button missing"
    assert 'data-tab="tab-panel-literature"' in html, "Tab 5 literature button missing"
    
    # Check TAB 1 content
    assert "The Flaw in Global Climate Accounting: Absolute vs. Structural Metrics" in html, "Problem card title missing"
    assert "Unsupervised Compositional Learning: Structural Archetypes" in html, "Solution card title missing"
    assert "Project Research Objectives" in html, "Objectives heading missing"
    assert "Data Engineering" in html, "Objective 1 missing"
    assert "Pattern Discovery" in html, "Objective 2 missing"
    assert "Mathematical Validation" in html, "Objective 3 missing"
    assert "Policy Equivalence" in html, "Objective 4 missing"
    
    # Check TAB 2 content
    assert "iso-isometric-stage" in html, "3D isometric stage missing"
    assert "iso-block-1" in html and "iso-block-4" in html, "3D isometric blocks missing"
    assert "The Percentage Problem & Centered Log-Ratio (CLR) Transformation" in html, "Accordion 1 missing"
    assert "Aitchison Simplex" in html, "Simplex text missing"
    assert "clr(x_i) = ln( x_i / g(x) )" in html or "clr(x" in html, "CLR formula missing"
    assert "Unsupervised Algorithmic Benchmarking & Consensus Selection" in html, "Accordion 2 missing"
    assert "Explainable AI (XAI) Surrogate Bounding Rules & Policy Mapping" in html, "Accordion 3 missing"
    
    # Check TAB 3 content
    assert "The 5 Global Decarbonization Archetypes" in html, "Archetypes heading missing"
    assert "Energy-Heavy" in html, "Energy-Heavy card missing"
    assert "Industry-Heavy" in html, "Industry-Heavy card missing"
    assert "Transport-Heavy" in html, "Transport-Heavy card missing"
    assert "Agriculture-Heavy" in html, "Agriculture-Heavy card missing"
    assert "Buildings-Heavy" in html, "Buildings-Heavy card missing"
    assert "arch-roadmap-accordion" in html, "Roadmap dropdown missing"
    
    # Check TAB 4 content
    assert "225" in html, "Hero stat 225 missing"
    assert "Sovereign Nations & Autonomous Territories" in html, "Hero stat headline missing"
    assert "EDGAR (v8.0)" in html, "EDGAR card missing"
    assert "Our World in Data (OWID)" in html, "OWID card missing"
    assert "Climate Watch Data" in html, "Climate Watch card missing"
    assert "CEDS" in html, "CEDS card missing"
    assert "MEIC Inventory" in html, "MEIC card missing"
    
    # Check TAB 5 content
    assert "PRISMA 2020 Systematic Literature Review" in html, "PRISMA review card missing"
    assert "60 Records Identified" in html, "PRISMA 60 records missing"
    assert "22 Core Studies Included" in html, "PRISMA 22 studies missing"
    assert "Inclusion Criteria" in html, "Inclusion criteria missing"
    assert "Exclusion Criteria" in html, "Exclusion criteria missing"
    assert "ARIMA" in html, "ARIMA exclusion note missing"
    assert "Academic Disclaimer & Scope of Equivalence" in html, "Academic disclaimer title missing"
    assert "Note: The cross-archetype equivalence measure developed in this study is illustrative of relative structural scale. It does not make causal or predictive claims about policy outcomes." in html, "Disclaimer exact text missing"
    
    print("[PASSED] index.html Section 5 university-grade documentation verified.")

# 2. Test style.css
with urllib.request.urlopen("http://localhost:5000/style.css") as res:
    css = res.read().decode("utf-8")
    assert ".selector-lights-track" in css, ".selector-lights-track CSS missing"
    assert ".selector-light-dot" in css, ".selector-light-dot CSS missing"
    assert ".about-tab-panel" in css, ".about-tab-panel CSS missing"
    assert ".iso-isometric-stage" in css, ".iso-isometric-stage 3D CSS missing"
    assert "preserve-3d" in css, "preserve-3d CSS missing"
    assert "isoFloat" in css, "isoFloat animation missing"
    assert ".method-accordion" in css, ".method-accordion CSS missing"
    assert ".archetypes-catalog-grid" in css, ".archetypes-catalog-grid CSS missing"
    assert ".stat-giant-num" in css, ".stat-giant-num CSS missing"
    assert ".prisma-flow-grid" in css, ".prisma-flow-grid CSS missing"
    assert ".academic-disclaimer-box" in css, ".academic-disclaimer-box CSS missing"
    print("[PASSED] style.css Section 5 styling verified.")

# 3. Test script.js
with urllib.request.urlopen("http://localhost:5000/script.js") as res:
    js = res.read().decode("utf-8")
    assert "setupAboutTabs" in js, "setupAboutTabs missing in script.js"
    assert "about-tab-btn" in js, "about-tab-btn missing in script.js"
    print("[PASSED] script.js setupAboutTabs logic verified.")

print("=== ALL VERIFICATION CHECKS COMPLETED SUCCESSFULLY! ===")
