# -*- coding: utf-8 -*-
"""
Generates the fully refactored, live dynamic frontend/index.html connected
to the Flask backend API at http://localhost:5000.
"""

HTML_CONTENT = r'''<!DOCTYPE html>
<html class="dark" lang="en">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <meta content="web_dashboard" name="shell-type"/>
  <title>Global Carbon Emission Archetypes Explorer | EDGAR Machine Learning Pipeline</title>
  
  <!-- Typography & Icons -->
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet"/>
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@100..900&family=Space+Grotesk:wght@100..900&display=swap" rel="stylesheet"/>
  
  <style>
    @layer base {
      html, body { margin:0; padding:0; }
      body { overscroll-behavior:none; }
      main > :first-child { margin-top:0 !important; }
      main > :last-child { margin-bottom:0 !important; }
    }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #131316; }
    ::-webkit-scrollbar-thumb { background: #2e2e33; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #3e3e44; }
  </style>

  <script src="https://cdn.tailwindcss.com"></script>
  <script id="tailwind-config">
    tailwind.config = {
      darkMode: "class",
      theme: {
        extend: {
          colors: {
            "surface": "#131316",
            "surface-container-lowest": "#0e0e11",
            "surface-container-low": "#18181b",
            "surface-container": "#1f1f22",
            "surface-container-high": "#27272a",
            "surface-container-highest": "#353438",
            "surface-bright": "#39393c",
            "primary": "#ffb690",
            "primary-container": "#f97316",
            "on-primary-container": "#582200",
            "tertiary": "#4edea3",
            "tertiary-container": "#00b07a",
            "error": "#ffb4ab",
            "outline": "#a78b7d",
            "on-surface": "#e4e1e5",
            "on-surface-variant": "#e0c0b1"
          },
          fontFamily: {
            "headline-lg": ["Space Grotesk", "sans-serif"],
            "headline-md": ["Space Grotesk", "sans-serif"],
            "headline-sm": ["Space Grotesk", "sans-serif"],
            "body-md": ["Geist", "sans-serif"],
            "body-sm": ["Geist", "sans-serif"],
            "label-mono": ["Geist", "monospace"],
            "label-md": ["Geist", "sans-serif"]
          }
        }
      }
    };
  </script>
</head>

<body class="bg-surface font-body-md text-body-md text-on-surface antialiased selection:bg-primary-container selection:text-white">
  
  <!-- Global Fixed Header -->
  <header class="fixed top-0 left-0 right-0 h-16 bg-surface-container-lowest/90 backdrop-blur-md z-50 flex items-center justify-between px-6 border-b border-surface-container-highest">
    <div class="flex items-center gap-4">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 bg-surface-container-high flex items-center justify-center border border-surface-container-highest rounded-lg shadow-sm">
          <span class="material-symbols-outlined text-primary text-[22px]">public</span>
        </div>
        <div class="flex flex-col">
          <span class="font-headline-sm text-sm font-semibold tracking-tight text-on-surface uppercase">Emission Archetypes</span>
          <span class="font-label-mono text-[10px] text-outline tracking-wider">EDGAR MACHINE LEARNING ENGINE</span>
        </div>
      </div>
      <div class="hidden lg:flex items-center gap-2 px-2.5 py-1 bg-surface-container-low border border-surface-container-highest rounded-full">
        <span class="w-2 h-2 rounded-full bg-tertiary animate-pulse" id="backend-status-dot"></span>
        <span class="font-label-mono text-[11px] text-tertiary uppercase font-medium" id="backend-status-text">Backend Connected</span>
      </div>
    </div>

    <!-- Right Header Actions -->
    <div class="flex items-center gap-3">
      <!-- Benchmark Drawer Selector Button -->
      <button class="flex items-center gap-2 bg-surface-container-high hover:bg-surface-bright px-3 py-1.5 border border-surface-container-highest rounded-lg transition-colors text-left" id="toggle-benchmark-drawer-header">
        <span class="material-symbols-outlined text-outline text-[16px]">travel_explore</span>
        <div class="flex flex-col">
          <span class="font-label-mono text-[9px] uppercase text-outline">Selected Party</span>
          <span class="font-label-md text-xs text-primary font-semibold truncate max-w-[140px]" id="header-country-label">United States (USA)</span>
        </div>
        <span class="material-symbols-outlined text-outline text-[14px]">expand_more</span>
      </button>

      <!-- Global Inventory Tag -->
      <div class="hidden sm:flex flex-col text-right pl-3 border-l border-surface-container-highest">
        <span class="font-label-md text-xs text-on-surface font-semibold">EDGAR v8.0 Inventory</span>
        <span class="font-label-mono text-[10px] text-outline uppercase">225 Sovereign States</span>
      </div>
      <div class="w-8 h-8 rounded-full bg-primary/20 border border-primary/40 flex items-center justify-center">
        <span class="material-symbols-outlined text-primary text-[18px]">account_balance</span>
      </div>
    </div>
  </header>

  <!-- Left Sidebar Navigation -->
  <aside class="fixed left-0 top-16 bottom-0 w-64 bg-surface-container-lowest z-40 flex flex-col border-r border-surface-container-highest">
    <div class="px-4 py-3 border-b border-surface-container-highest flex items-center justify-between">
      <span class="font-label-mono text-[11px] text-outline uppercase tracking-wider">Navigation</span>
      <span class="material-symbols-outlined text-outline text-[16px]">tune</span>
    </div>

    <nav class="flex-1 flex flex-col gap-1 p-3 overflow-y-auto">
      <a class="flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors font-label-md text-xs bg-surface-container-high text-primary border-l-2 border-primary" href="#matrix-view">
        <span class="material-symbols-outlined text-[18px]">grid_view</span>
        <span>Archetype Matrix</span>
      </a>
      <a class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-on-surface-variant hover:bg-surface-container hover:text-on-surface transition-colors font-label-md text-xs" href="#macro-simulator">
        <span class="material-symbols-outlined text-[18px]">tune</span>
        <span>Macro-Sector Simulator</span>
      </a>
      <a class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-on-surface-variant hover:bg-surface-container hover:text-on-surface transition-colors font-label-md text-xs" href="#xai-rules">
        <span class="material-symbols-outlined text-[18px]">psychology</span>
        <span>Explainable AI (XAI)</span>
      </a>
      <a class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-on-surface-variant hover:bg-surface-container hover:text-on-surface transition-colors font-label-md text-xs" href="#equivalence-engine">
        <span class="material-symbols-outlined text-[18px]">calculate</span>
        <span>Equivalence Engine</span>
      </a>
      <a class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-on-surface-variant hover:bg-surface-container hover:text-on-surface transition-colors font-label-md text-xs" href="#audit-ledger">
        <span class="material-symbols-outlined text-[18px]">menu_book</span>
        <span>Decision Tree Ledger</span>
      </a>
    </nav>

    <!-- Simplex Projection Status Widget -->
    <div class="p-4 border-t border-surface-container-highest bg-surface-container-low">
      <div class="flex items-center justify-between mb-1.5">
        <span class="font-label-mono text-[10px] text-outline uppercase tracking-wider">Simplex Space</span>
        <span class="font-label-mono text-[10px] text-tertiary font-bold">CLR TRANSFORMED</span>
      </div>
      <div class="w-full h-1.5 bg-surface-container-highest rounded-full overflow-hidden">
        <div class="h-full bg-tertiary w-full"></div>
      </div>
      <div class="flex justify-between items-center mt-2 text-[10px] font-label-mono text-outline">
        <span>5 Macro Sectors</span>
        <span>Sum = 100.0%</span>
      </div>
    </div>
  </aside>

  <!-- Main Content Layout -->
  <div class="pl-64">
    <main class="w-full pt-16 bg-surface min-h-screen px-6 lg:px-8 py-6">
      <div class="flex flex-col w-full gap-6 max-w-7xl mx-auto">

        <!-- Top Header & Overview Bar -->
        <header class="flex flex-col lg:flex-row lg:items-end justify-between gap-4 pb-4 border-b border-surface-container-highest">
          <div class="flex flex-col gap-1 max-w-3xl">
            <div class="flex items-center gap-2 mb-1">
              <span class="px-2 py-0.5 rounded text-[10px] uppercase font-label-mono tracking-widest bg-primary/10 text-primary border border-primary/20">Phase D · REST API Integrated</span>
              <span class="text-outline text-body-sm">·</span>
              <span class="text-outline font-label-mono text-[11px] tracking-wide">EDGAR 2023 AR5 Metric</span>
            </div>
            <h1 class="font-headline-lg text-2xl lg:text-3xl text-on-surface tracking-tight font-semibold">
              Carbon Emission Archetypes Explorer
            </h1>
            <p class="font-body-md text-sm text-on-surface-variant">
              Interactive continuous simplex simulation, machine-learned emission archetypes (DBSCAN / CLR), and explainable bounding-box climate policy equivalence.
            </p>
          </div>

          <!-- Quick Actions & Drawer Toggle -->
          <div class="flex items-center gap-2.5 flex-wrap">
            <button class="group flex items-center gap-2 px-3.5 py-2 bg-surface-container-high hover:bg-surface-bright text-on-surface rounded-xl border border-surface-container-highest transition-all duration-200 shadow-sm" id="toggle-benchmark-drawer">
              <span class="material-symbols-outlined text-primary text-[18px] transition-transform group-hover:scale-110">public</span>
              <div class="flex flex-col text-left">
                <span class="font-label-mono text-[9px] uppercase text-outline">Country Baseline</span>
                <span class="font-label-md text-xs text-on-surface font-semibold" id="active-country-label">United States (USA)</span>
              </div>
              <span class="material-symbols-outlined text-outline text-[16px] ml-1 transition-transform duration-200" id="drawer-chevron">expand_more</span>
            </button>
            <button class="flex items-center gap-1.5 px-3 py-2 bg-surface-container-low hover:bg-surface-container text-on-surface-variant hover:text-on-surface rounded-xl border border-surface-container-highest text-xs transition-colors" id="reset-sim-btn">
              <span class="material-symbols-outlined text-[16px]">restart_alt</span>
              <span>Reset Mix</span>
            </button>
          </div>
        </header>

        <!-- Collapsible Benchmark Selection Panel (225 Real Countries) -->
        <section class="hidden overflow-hidden transition-all duration-300" id="benchmark-drawer">
          <div class="bg-surface-container-low rounded-2xl border border-surface-container-highest p-5 mb-2">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-surface-container-highest">
              <div>
                <h3 class="font-headline-sm text-sm text-on-surface font-semibold">National Empirical Baselines (EDGAR Database)</h3>
                <p class="font-body-sm text-xs text-outline">Select from 225 empirical country distributions to project directly into continuous CLR space.</p>
              </div>
              <div class="relative w-full md:w-80">
                <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-outline text-[16px]">search</span>
                <input class="w-full pl-9 pr-3 py-1.5 bg-surface-container-highest text-on-surface rounded-lg border border-outline/20 font-body-sm text-xs focus:outline-none focus:border-primary placeholder:text-outline/60" id="country-search-input" placeholder="Search 225 Countries or ISO Codes..." type="text"/>
              </div>
            </div>

            <!-- Dynamic Country Preset Pills Container -->
            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2.5 pt-4 max-h-60 overflow-y-auto pr-1" id="country-presets-container">
              <!-- Dynamically populated from /api/data -->
              <div class="col-span-full py-4 text-center font-label-mono text-xs text-outline animate-pulse">Loading verified national inventories from database...</div>
            </div>
          </div>
        </section>

        <!-- SECTION 1: Interactive Macro-Sector Simulator & Machine Learning Archetype -->
        <section class="w-full bg-[#18181b] border border-[#27272a] rounded-2xl p-6 lg:p-7 shadow-2xl relative overflow-hidden flex flex-col gap-6" id="macro-simulator">
          <!-- Ambient Corner Light -->
          <div class="absolute -top-32 -right-32 w-80 h-80 bg-primary/5 rounded-full blur-3xl pointer-events-none"></div>

          <!-- Dynamic Machine-Learned Archetype Match Banner -->
          <div class="relative z-10 w-full rounded-xl bg-[#222225] border border-[#2e2e33] p-5 transition-all duration-300 shadow-sm" id="archetype-banner">
            <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
              <div class="flex items-start gap-4">
                <div class="w-13 h-13 shrink-0 rounded-xl bg-[#f97316]/10 border border-[#f97316]/30 flex items-center justify-center text-[#f97316] p-3" id="archetype-icon-wrapper">
                  <span class="material-symbols-outlined text-[30px]" id="archetype-icon">bolt</span>
                </div>
                <div class="flex flex-col gap-1">
                  <div class="flex items-center gap-2 flex-wrap">
                    <span class="px-2.5 py-0.5 rounded font-label-mono text-[10px] tracking-wider uppercase bg-[#f97316]/20 text-[#f97316] font-semibold border border-[#f97316]/40" id="archetype-cluster-pill">Cluster 0 · Energy-Dominant</span>
                    <span class="font-label-mono text-[11px] text-tertiary flex items-center gap-1 font-semibold" id="archetype-confidence">
                      <span class="w-1.5 h-1.5 rounded-full bg-tertiary"></span> 98.2% Model Proximity
                    </span>
                  </div>
                  <h2 class="font-headline-md text-xl text-[#f4f4f5] font-semibold tracking-tight" id="archetype-title">
                    Energy-Dominant Economies
                  </h2>
                  <p class="font-body-sm text-xs text-[#a1a1aa] max-w-3xl leading-relaxed" id="archetype-desc">
                    Structural reliance on grid energy generation and thermal power systems. Electrification and renewable dispatch yield the primary return on global abatement.
                  </p>
                </div>
              </div>

              <!-- Metric Badges from Model Inference -->
              <div class="flex items-center gap-4 pt-3 lg:pt-0 border-t lg:border-t-0 border-[#2e2e33]">
                <div class="flex flex-col items-start lg:items-end px-2">
                  <span class="font-label-mono text-[10px] uppercase text-[#a1a1aa]">Primary Leverage</span>
                  <span class="font-headline-sm text-sm font-semibold text-[#f97316]" id="archetype-driver">Energy Sector</span>
                  <span class="font-label-mono text-[10px] text-tertiary font-medium" id="archetype-dist-label">CLR Δ = 0.588</span>
                </div>
                <div class="w-px h-10 bg-[#2e2e33] hidden sm:block"></div>
                <div class="flex flex-col items-start lg:items-end px-2">
                  <span class="font-label-mono text-[10px] uppercase text-[#a1a1aa]">Cluster Size</span>
                  <div class="flex items-baseline gap-1">
                    <span class="font-headline-md text-lg font-bold text-[#f4f4f5]" id="archetype-country-count">196</span>
                    <span class="font-label-mono text-[10px] text-[#a1a1aa]">Nations</span>
                  </div>
                  <span class="font-label-mono text-[10px] text-outline">87.1% Global Distribution</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Scenario Shortcuts & Auto-Rebalancing Status Header -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#2e2e33] pb-3">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="font-label-mono text-[11px] text-[#a1a1aa] uppercase tracking-wider">Cluster Archetype Scenarios:</span>
              <div class="flex items-center gap-1.5 flex-wrap">
                <button class="scenario-btn px-2.5 py-1 text-xs rounded-lg bg-[#222225] text-[#f4f4f5] hover:bg-surface-bright border border-[#2e2e33] transition-colors" data-scenario="cluster0">Energy-Dominant (Cluster 0)</button>
                <button class="scenario-btn px-2.5 py-1 text-xs rounded-lg bg-[#222225] text-[#f4f4f5] hover:bg-surface-bright border border-[#2e2e33] transition-colors" data-scenario="cluster1">Agriculture-Dominant (Cluster 1)</button>
                <button class="scenario-btn px-2.5 py-1 text-xs rounded-lg bg-[#222225] text-[#f4f4f5] hover:bg-surface-bright border border-[#2e2e33] transition-colors" data-scenario="cluster2">Industry-Dominant (Cluster 2)</button>
                <button class="scenario-btn px-2.5 py-1 text-xs rounded-lg bg-[#222225] text-[#f4f4f5] hover:bg-surface-bright border border-[#2e2e33] transition-colors" data-scenario="transit">Transit-Intensive (Cluster -1)</button>
                <button class="scenario-btn px-2.5 py-1 text-xs rounded-lg bg-[#222225] text-[#f4f4f5] hover:bg-surface-bright border border-[#2e2e33] transition-colors" data-scenario="balanced">Equal Simplex (20%)</button>
              </div>
            </div>

            <!-- Auto-Rebalancing Sum Badge -->
            <div class="flex items-center gap-2 self-start sm:self-auto">
              <div class="flex items-center gap-2 px-3 py-1 rounded-full bg-tertiary/10 text-tertiary border border-tertiary/30 font-label-mono text-xs" id="allocation-badge">
                <span class="w-2 h-2 rounded-full bg-tertiary"></span>
                <span id="allocation-sum-text">Total Sector Allocation: 100% (Simplex Balanced)</span>
              </div>
            </div>
          </div>

          <!-- 5 Macro-Sector Sliders Grid -->
          <div class="grid grid-cols-1 md:grid-cols-5 gap-3 lg:gap-4">
            <!-- 1. Energy Sector -->
            <div class="slider-module flex flex-col justify-between p-4 rounded-xl bg-[#222225] border border-[#2e2e33] hover:border-[#f97316]/50 transition-colors" data-sector="energy">
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-1.5">
                  <span class="w-2.5 h-2.5 rounded-sm bg-[#f97316]"></span>
                  <span class="font-label-md text-xs font-semibold text-[#f4f4f5]">Energy</span>
                </div>
                <span class="font-label-mono text-[9px] text-[#f97316] uppercase tracking-wider">Power / Grid</span>
              </div>
              <div class="flex items-baseline justify-between my-2">
                <span class="font-headline-lg text-2xl font-bold text-[#f4f4f5]" id="energy-val-display">38<span class="text-sm font-normal text-outline">%</span></span>
                <span class="font-label-mono text-[11px] text-[#a1a1aa]" id="energy-mt-display">2,171 Mt</span>
              </div>
              <div class="space-y-2">
                <input class="sector-slider w-full h-2 rounded-none bg-[#111111] appearance-none cursor-pointer accent-[#f97316]" data-sector-id="energy" id="energy-slider" max="100" min="0" type="range" value="38"/>
                <div class="flex items-center justify-between gap-1 pt-1">
                  <button class="step-btn px-2 py-0.5 rounded bg-[#18181b] hover:bg-surface-bright text-outline hover:text-on-surface font-label-mono text-xs border border-[#2e2e33]" data-dir="-1" data-target="energy">-1%</button>
                  <span class="font-label-mono text-[9px] text-outline">AUTO-BALANCED</span>
                  <button class="step-btn px-2 py-0.5 rounded bg-[#18181b] hover:bg-surface-bright text-outline hover:text-on-surface font-label-mono text-xs border border-[#2e2e33]" data-dir="1" data-target="energy">+1%</button>
                </div>
              </div>
            </div>

            <!-- 2. Industry Sector -->
            <div class="slider-module flex flex-col justify-between p-4 rounded-xl bg-[#222225] border border-[#2e2e33] hover:border-[#8b5cf6]/50 transition-colors" data-sector="industry">
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-1.5">
                  <span class="w-2.5 h-2.5 rounded-sm bg-[#8b5cf6]"></span>
                  <span class="font-label-md text-xs font-semibold text-[#f4f4f5]">Industry</span>
                </div>
                <span class="font-label-mono text-[9px] text-[#8b5cf6] uppercase tracking-wider">Manufacturing</span>
              </div>
              <div class="flex items-baseline justify-between my-2">
                <span class="font-headline-lg text-2xl font-bold text-[#f4f4f5]" id="industry-val-display">24<span class="text-sm font-normal text-outline">%</span></span>
                <span class="font-label-mono text-[11px] text-[#a1a1aa]" id="industry-mt-display">1,371 Mt</span>
              </div>
              <div class="space-y-2">
                <input class="sector-slider w-full h-2 rounded-none bg-[#111111] appearance-none cursor-pointer accent-[#8b5cf6]" data-sector-id="industry" id="industry-slider" max="100" min="0" type="range" value="24"/>
                <div class="flex items-center justify-between gap-1 pt-1">
                  <button class="step-btn px-2 py-0.5 rounded bg-[#18181b] hover:bg-surface-bright text-outline hover:text-on-surface font-label-mono text-xs border border-[#2e2e33]" data-dir="-1" data-target="industry">-1%</button>
                  <span class="font-label-mono text-[9px] text-outline">AUTO-BALANCED</span>
                  <button class="step-btn px-2 py-0.5 rounded bg-[#18181b] hover:bg-surface-bright text-outline hover:text-on-surface font-label-mono text-xs border border-[#2e2e33]" data-dir="1" data-target="industry">+1%</button>
                </div>
              </div>
            </div>

            <!-- 3. Transport Sector -->
            <div class="slider-module flex flex-col justify-between p-4 rounded-xl bg-[#222225] border border-[#2e2e33] hover:border-[#10b981]/50 transition-colors" data-sector="transport">
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-1.5">
                  <span class="w-2.5 h-2.5 rounded-sm bg-[#10b981]"></span>
                  <span class="font-label-md text-xs font-semibold text-[#f4f4f5]">Transport</span>
                </div>
                <span class="font-label-mono text-[9px] text-[#10b981] uppercase tracking-wider">Mobility</span>
              </div>
              <div class="flex items-baseline justify-between my-2">
                <span class="font-headline-lg text-2xl font-bold text-[#f4f4f5]" id="transport-val-display">18<span class="text-sm font-normal text-outline">%</span></span>
                <span class="font-label-mono text-[11px] text-[#a1a1aa]" id="transport-mt-display">1,028 Mt</span>
              </div>
              <div class="space-y-2">
                <input class="sector-slider w-full h-2 rounded-none bg-[#111111] appearance-none cursor-pointer accent-[#10b981]" data-sector-id="transport" id="transport-slider" max="100" min="0" type="range" value="18"/>
                <div class="flex items-center justify-between gap-1 pt-1">
                  <button class="step-btn px-2 py-0.5 rounded bg-[#18181b] hover:bg-surface-bright text-outline hover:text-on-surface font-label-mono text-xs border border-[#2e2e33]" data-dir="-1" data-target="transport">-1%</button>
                  <span class="font-label-mono text-[9px] text-outline">AUTO-BALANCED</span>
                  <button class="step-btn px-2 py-0.5 rounded bg-[#18181b] hover:bg-surface-bright text-outline hover:text-on-surface font-label-mono text-xs border border-[#2e2e33]" data-dir="1" data-target="transport">+1%</button>
                </div>
              </div>
            </div>

            <!-- 4. Agriculture Sector -->
            <div class="slider-module flex flex-col justify-between p-4 rounded-xl bg-[#222225] border border-[#2e2e33] hover:border-[#ec4899]/50 transition-colors" data-sector="agriculture">
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-1.5">
                  <span class="w-2.5 h-2.5 rounded-sm bg-[#ec4899]"></span>
                  <span class="font-label-md text-xs font-semibold text-[#f4f4f5]">Agriculture</span>
                </div>
                <span class="font-label-mono text-[9px] text-[#ec4899] uppercase tracking-wider">AFOLU / Soil</span>
              </div>
              <div class="flex items-baseline justify-between my-2">
                <span class="font-headline-lg text-2xl font-bold text-[#f4f4f5]" id="agriculture-val-display">12<span class="text-sm font-normal text-outline">%</span></span>
                <span class="font-label-mono text-[11px] text-[#a1a1aa]" id="agriculture-mt-display">686 Mt</span>
              </div>
              <div class="space-y-2">
                <input class="sector-slider w-full h-2 rounded-none bg-[#111111] appearance-none cursor-pointer accent-[#ec4899]" data-sector-id="agriculture" id="agriculture-slider" max="100" min="0" type="range" value="12"/>
                <div class="flex items-center justify-between gap-1 pt-1">
                  <button class="step-btn px-2 py-0.5 rounded bg-[#18181b] hover:bg-surface-bright text-outline hover:text-on-surface font-label-mono text-xs border border-[#2e2e33]" data-dir="-1" data-target="agriculture">-1%</button>
                  <span class="font-label-mono text-[9px] text-outline">AUTO-BALANCED</span>
                  <button class="step-btn px-2 py-0.5 rounded bg-[#18181b] hover:bg-surface-bright text-outline hover:text-on-surface font-label-mono text-xs border border-[#2e2e33]" data-dir="1" data-target="agriculture">+1%</button>
                </div>
              </div>
            </div>

            <!-- 5. Buildings Sector -->
            <div class="slider-module flex flex-col justify-between p-4 rounded-xl bg-[#222225] border border-[#2e2e33] hover:border-[#eab308]/50 transition-colors" data-sector="buildings">
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-1.5">
                  <span class="w-2.5 h-2.5 rounded-sm bg-[#eab308]"></span>
                  <span class="font-label-md text-xs font-semibold text-[#f4f4f5]">Buildings</span>
                </div>
                <span class="font-label-mono text-[9px] text-[#eab308] uppercase tracking-wider">Built Env</span>
              </div>
              <div class="flex items-baseline justify-between my-2">
                <span class="font-headline-lg text-2xl font-bold text-[#f4f4f5]" id="buildings-val-display">8<span class="text-sm font-normal text-outline">%</span></span>
                <span class="font-label-mono text-[11px] text-[#a1a1aa]" id="buildings-mt-display">457 Mt</span>
              </div>
              <div class="space-y-2">
                <input class="sector-slider w-full h-2 rounded-none bg-[#111111] appearance-none cursor-pointer accent-[#eab308]" data-sector-id="buildings" id="buildings-slider" max="100" min="0" type="range" value="8"/>
                <div class="flex items-center justify-between gap-1 pt-1">
                  <button class="step-btn px-2 py-0.5 rounded bg-[#18181b] hover:bg-surface-bright text-outline hover:text-on-surface font-label-mono text-xs border border-[#2e2e33]" data-dir="-1" data-target="buildings">-1%</button>
                  <span class="font-label-mono text-[9px] text-outline">AUTO-BALANCED</span>
                  <button class="step-btn px-2 py-0.5 rounded bg-[#18181b] hover:bg-surface-bright text-outline hover:text-on-surface font-label-mono text-xs border border-[#2e2e33]" data-dir="1" data-target="buildings">+1%</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Cumulative Composition Ribbon -->
          <div class="w-full flex flex-col gap-1.5 pt-1">
            <div class="flex items-center justify-between text-xs font-label-mono text-[#a1a1aa]">
              <span>Cumulative Composition Ribbon</span>
              <span class="text-tertiary" id="ribbon-balance-indicator">100.0% Simplex Balanced</span>
            </div>
            <div class="w-full h-3 bg-[#111111] rounded-sm overflow-hidden flex shadow-inner">
              <div class="h-full bg-[#f97316] transition-all duration-150" id="bar-energy" style="width: 38%"></div>
              <div class="h-full bg-[#8b5cf6] transition-all duration-150" id="bar-industry" style="width: 24%"></div>
              <div class="h-full bg-[#10b981] transition-all duration-150" id="bar-transport" style="width: 18%"></div>
              <div class="h-full bg-[#ec4899] transition-all duration-150" id="bar-agriculture" style="width: 12%"></div>
              <div class="h-full bg-[#eab308] transition-all duration-150" id="bar-buildings" style="width: 8%"></div>
            </div>
          </div>
        </section>

        <!-- SECTION 2: Science & Analytical Cards Grid (XAI Rules & PRD Equivalence) -->
        <div class="grid grid-cols-1 xl:grid-cols-12 gap-6 w-full">
          
          <!-- Card 1: Explainable AI Decision Rules (Phase C) -->
          <section class="xl:col-span-6 bg-[#18181b] border border-[#27272a] rounded-2xl p-6 lg:p-7 flex flex-col justify-between gap-5 shadow-xl relative" id="xai-rules">
            <div class="flex flex-col gap-4">
              <!-- Header -->
              <div class="flex items-start justify-between gap-3 border-b border-[#2e2e33] pb-4">
                <div class="flex flex-col gap-1">
                  <div class="flex items-center gap-2">
                    <span class="material-symbols-outlined text-primary text-[22px]">psychology</span>
                    <h3 class="font-headline-md text-lg font-semibold text-[#f4f4f5]">Explainable AI (XAI) Decision Rules</h3>
                  </div>
                  <p class="font-body-sm text-xs text-[#a1a1aa]">
                    Surrogate Decision Tree (max_depth=3) extracted from winning CLR cluster assignments.
                  </p>
                </div>
                <div class="px-2.5 py-1 rounded bg-[#222225] border border-[#2e2e33] font-label-mono text-[10px] text-tertiary flex items-center gap-1.5 shrink-0">
                  <span class="w-1.5 h-1.5 rounded-full bg-tertiary"></span>
                  <span id="xai-accuracy-badge">SURROGATE ACCURACY: 98.22%</span>
                </div>
              </div>

              <!-- Triggered Classification Logic Box -->
              <div class="flex flex-col gap-2">
                <span class="font-label-mono text-[10px] uppercase text-outline tracking-wider">Triggered Classification Logic</span>
                <div class="bg-[#222225] border border-[#2e2e33] rounded-xl p-4 flex flex-col gap-2.5 shadow-sm" id="rule-trace-box">
                  <div class="flex items-center gap-2 font-label-mono text-xs">
                    <span class="px-2 py-0.5 rounded bg-primary/20 text-primary border border-primary/30 font-semibold" id="rule-node-label">PHASE C SURROGATE</span>
                    <span class="text-[#f4f4f5] font-medium leading-snug" id="primary-rule-eval">IF Energy &gt; 2.1% AND Industry &le; 75.0% THEN Classify as Energy-Dominant Economies (Cluster 0)</span>
                  </div>
                  <p class="font-body-sm text-xs text-[#a1a1aa] leading-relaxed" id="rule-rationale-text">
                    Energy sector accounts for the structural centroid of the national emissions profile across core global economies.
                  </p>
                  <div class="flex items-center justify-between text-xs pt-2 border-t border-[#2e2e33]">
                    <span class="text-outline font-label-mono text-[11px]">Euclidean Distance in CLR Space:</span>
                    <span class="font-label-mono text-tertiary font-medium text-[11px]" id="boundary-distance">Minimum Centroid Δ = 0.588</span>
                  </div>
                </div>
              </div>

              <!-- Sector Feature Vector in CLR Coordinates -->
              <div class="flex flex-col gap-2">
                <div class="flex items-center justify-between">
                  <span class="font-label-mono text-[10px] uppercase text-outline tracking-wider">Continuous Sector Vector (CLR Coordinates)</span>
                  <span class="font-label-mono text-[10px] text-outline">Simplex Coordinate</span>
                </div>
                <div class="space-y-2 text-xs font-label-mono">
                  <div>
                    <div class="flex justify-between text-[11px] mb-1 text-[#f4f4f5]">
                      <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-xs bg-[#f97316]"></span>Energy</span>
                      <span class="text-[#f97316]" id="shap-energy">38% (CLR: +0.78)</span>
                    </div>
                    <div class="w-full h-1.5 bg-[#111111] rounded-full overflow-hidden">
                      <div class="h-full bg-[#f97316]" id="shap-bar-energy" style="width: 76%"></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex justify-between text-[11px] mb-1 text-[#f4f4f5]">
                      <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-xs bg-[#8b5cf6]"></span>Industry</span>
                      <span class="text-[#8b5cf6]" id="shap-industry">24% (CLR: +0.32)</span>
                    </div>
                    <div class="w-full h-1.5 bg-[#111111] rounded-full overflow-hidden">
                      <div class="h-full bg-[#8b5cf6]" id="shap-bar-industry" style="width: 48%"></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex justify-between text-[11px] mb-1 text-[#f4f4f5]">
                      <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-xs bg-[#10b981]"></span>Transport</span>
                      <span class="text-[#10b981]" id="shap-transport">18% (CLR: +0.04)</span>
                    </div>
                    <div class="w-full h-1.5 bg-[#111111] rounded-full overflow-hidden">
                      <div class="h-full bg-[#10b981]" id="shap-bar-transport" style="width: 36%"></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex justify-between text-[11px] mb-1 text-[#f4f4f5]">
                      <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-xs bg-[#ec4899]"></span>Agriculture</span>
                      <span class="text-[#ec4899]" id="shap-agriculture">12% (CLR: -0.37)</span>
                    </div>
                    <div class="w-full h-1.5 bg-[#111111] rounded-full overflow-hidden">
                      <div class="h-full bg-[#ec4899]" id="shap-bar-agriculture" style="width: 24%"></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex justify-between text-[11px] mb-1 text-[#f4f4f5]">
                      <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-xs bg-[#eab308]"></span>Buildings</span>
                      <span class="text-[#eab308]" id="shap-buildings">8% (CLR: -0.77)</span>
                    </div>
                    <div class="w-full h-1.5 bg-[#111111] rounded-full overflow-hidden">
                      <div class="h-full bg-[#eab308]" id="shap-bar-buildings" style="width: 16%"></div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Full Rules Audit Ledger (Scrollable List of 6 Rules) -->
              <div class="flex flex-col gap-2 pt-2 border-t border-[#2e2e33]" id="audit-ledger">
                <div class="flex items-center justify-between">
                  <span class="font-label-mono text-[10px] uppercase text-outline tracking-wider">All Extracted Surrogate Rules (Phase C)</span>
                  <span class="font-label-mono text-[10px] text-tertiary">6 Bounding Boxes</span>
                </div>
                <div class="space-y-1.5 max-h-40 overflow-y-auto pr-1" id="all-rules-container">
                  <!-- Populated from /api/rules -->
                  <div class="p-2 rounded bg-[#222225] border border-[#2e2e33] text-[11px] font-label-mono text-outline">Loading surrogate rules...</div>
                </div>
              </div>
            </div>

            <!-- Footer Policy Recommendation -->
            <div class="p-3 bg-[#111111] rounded-xl border border-[#2e2e33] flex items-center justify-between text-xs">
              <div class="flex items-center gap-2 text-[#a1a1aa]">
                <span class="material-symbols-outlined text-primary text-[18px]">lightbulb</span>
                <span id="xai-recommendation-short">Accelerate baseload coal-to-clean grid conversion and renewable dispatch infrastructure.</span>
              </div>
              <span class="text-outline font-label-mono text-[10px] shrink-0">POLICY GUIDANCE</span>
            </div>
          </section>

          <!-- Card 2: Equivalence Measure Calculations & Real-World Impact -->
          <section class="xl:col-span-6 bg-[#18181b] border border-[#27272a] rounded-2xl p-6 lg:p-7 flex flex-col justify-between gap-5 shadow-xl relative" id="equivalence-engine">
            <div class="flex flex-col gap-4">
              <!-- Header & Controls -->
              <div class="flex items-start justify-between gap-3 border-b border-[#2e2e33] pb-4 flex-wrap">
                <div class="flex flex-col gap-1">
                  <div class="flex items-center gap-2">
                    <span class="material-symbols-outlined text-tertiary text-[22px]">calculate</span>
                    <h3 class="font-headline-md text-lg font-semibold text-[#f4f4f5]">Carbon Equivalence Calculations</h3>
                  </div>
                  <p class="font-body-sm text-xs text-[#a1a1aa]">
                    Mathematical equivalence: Required sector activity cut on dominant sector to match benchmark reduction.
                  </p>
                </div>

                <!-- Benchmark Cut Selector & Unit Toggle -->
                <div class="flex items-center gap-2">
                  <div class="inline-flex rounded-lg p-0.5 bg-[#111111] border border-[#2e2e33] text-[11px] font-label-mono">
                    <button class="bench-cut-btn px-2 py-1 rounded bg-[#222225] text-primary font-semibold" data-cut="5">5%</button>
                    <button class="bench-cut-btn px-2 py-1 rounded text-outline hover:text-[#f4f4f5]" data-cut="10">10%</button>
                    <button class="bench-cut-btn px-2 py-1 rounded text-outline hover:text-[#f4f4f5]" data-cut="15">15%</button>
                  </div>
                  <div class="inline-flex rounded-lg p-0.5 bg-[#111111] border border-[#2e2e33] text-[11px] font-label-mono">
                    <button class="unit-toggle-btn px-2 py-1 rounded bg-[#222225] text-primary font-semibold" data-unit="mt">Mt</button>
                    <button class="unit-toggle-btn px-2 py-1 rounded text-outline hover:text-[#f4f4f5]" data-unit="gt">Gt</button>
                  </div>
                </div>
              </div>

              <!-- Hero Net Metric Reading -->
              <div class="p-4 rounded-xl bg-[#222225] border border-[#2e2e33] flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div>
                  <span class="font-label-mono text-[10px] uppercase text-[#a1a1aa]">Annual Baseline Emissions</span>
                  <div class="flex items-baseline gap-2">
                    <span class="font-headline-xl text-3xl font-bold text-[#f4f4f5]" id="hero-co2-val">5,714</span>
                    <span class="font-headline-sm text-sm text-primary font-medium" id="hero-co2-unit">Mt CO₂e / yr</span>
                  </div>
                  <span class="font-label-mono text-[10px] text-outline" id="hero-country-status">United States (USA) · EDGAR 2023 AR5</span>
                </div>
                <div class="flex flex-col items-start sm:items-end p-3 bg-[#111111] rounded-lg border border-[#2e2e33]">
                  <span class="font-label-mono text-[10px] uppercase text-outline">Target Reduction ΔE_target</span>
                  <span class="font-headline-md text-lg font-bold text-primary" id="target-delta-val">285.70 Mt</span>
                  <span class="font-label-mono text-[10px] text-tertiary" id="benchmark-label-val">5.0% Benchmark Target</span>
                </div>
              </div>

              <!-- 4-Grid of Equivalence Measures -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                <!-- 1. Dominant Sector Activity Cut -->
                <div class="p-4 rounded-xl bg-[#222225] border border-primary/30 flex flex-col gap-1.5 shadow-sm">
                  <div class="flex items-center gap-1.5 text-primary">
                    <span class="material-symbols-outlined text-[18px]">trending_down</span>
                    <span class="font-label-mono text-[10px] uppercase tracking-wider font-semibold">Sector Activity Cut</span>
                  </div>
                  <span class="font-headline-md text-xl font-bold text-primary" id="eq-activity-cut-val">12.94% Cut</span>
                  <span class="font-body-sm text-xs text-[#a1a1aa]" id="eq-dominant-desc">Energy sector reduction required to match benchmark target</span>
                </div>

                <!-- 2. Dominant Sector Baseline -->
                <div class="p-4 rounded-xl bg-[#222225] border border-[#2e2e33] flex flex-col gap-1.5 shadow-sm">
                  <div class="flex items-center gap-1.5 text-[#8b5cf6]">
                    <span class="material-symbols-outlined text-[18px]">analytics</span>
                    <span class="font-label-mono text-[10px] uppercase tracking-wider text-outline font-semibold">Dominant Baseline</span>
                  </div>
                  <span class="font-headline-md text-xl font-bold text-[#f4f4f5]" id="eq-dominant-baseline-val">2,207.0 Mt</span>
                  <span class="font-body-sm text-xs text-[#a1a1aa]" id="eq-dominant-share-desc">Energy accounts for 38.6% of baseline emissions</span>
                </div>

                <!-- 3. Forest Sequestration Equivalent -->
                <div class="p-4 rounded-xl bg-[#222225] border border-[#2e2e33] flex flex-col gap-1.5 shadow-sm">
                  <div class="flex items-center gap-1.5 text-tertiary">
                    <span class="material-symbols-outlined text-[18px]">forest</span>
                    <span class="font-label-mono text-[10px] uppercase tracking-wider text-outline font-semibold">Forest Sequestration</span>
                  </div>
                  <span class="font-headline-md text-xl font-bold text-[#f4f4f5]" id="eq-trees-val">13.0 Billion</span>
                  <span class="font-body-sm text-xs text-[#a1a1aa]">Tree seedlings grown for 10 years to offset ΔE_target</span>
                </div>

                <!-- 4. Coal Power Plants Retired -->
                <div class="p-4 rounded-xl bg-[#222225] border border-[#2e2e33] flex flex-col gap-1.5 shadow-sm">
                  <div class="flex items-center gap-1.5 text-[#f97316]">
                    <span class="material-symbols-outlined text-[18px]">factory</span>
                    <span class="font-label-mono text-[10px] uppercase tracking-wider text-outline font-semibold">Coal Units Retired</span>
                  </div>
                  <span class="font-headline-md text-xl font-bold text-[#f4f4f5]" id="eq-coal-val">73 Plants</span>
                  <span class="font-body-sm text-xs text-[#a1a1aa]">Standard 500MW coal plants abated annually</span>
                </div>
              </div>
            </div>

            <!-- Equivalence Mathematical Formula Footer -->
            <div class="flex flex-col gap-1.5 pt-2 border-t border-[#2e2e33]">
              <div class="flex justify-between font-label-mono text-xs text-[#a1a1aa]">
                <span>Equivalence Formula: Sector Activity Cut = ΔE_target / Dominant Baseline</span>
                <span class="text-tertiary font-medium" id="math-proof-label">ΔE = 5.0% × Total</span>
              </div>
              <div class="w-full h-1.5 bg-[#111111] rounded-full overflow-hidden relative">
                <div class="h-full bg-primary transition-all duration-300" id="pace-bar" style="width: 12.94%"></div>
              </div>
            </div>
          </section>
        </div>

      </div>
    </main>
  </div>

  <!-- Real JavaScript Telemetry & Data Binding Engine -->
  <script>
    (function initCarbonTelemetryApp() {
      const API_BASE = 'http://localhost:5000';

      // Application State
      const state = {
        sectors: {
          energy: 38,
          industry: 24,
          transport: 18,
          agriculture: 12,
          buildings: 8
        },
        country: 'USA',
        countryName: 'United States',
        totalBaselineMt: 5714,
        benchmarkPct: 5.0,
        unitMode: 'mt',
        countriesData: [],
        emissionsData: [],
        rulesData: null,
        debounceTimer: null
      };

      // DOM Elements
      const sliders = {
        energy: document.getElementById('energy-slider'),
        industry: document.getElementById('industry-slider'),
        transport: document.getElementById('transport-slider'),
        agriculture: document.getElementById('agriculture-slider'),
        buildings: document.getElementById('buildings-slider')
      };

      const displays = {
        energy: document.getElementById('energy-val-display'),
        industry: document.getElementById('industry-val-display'),
        transport: document.getElementById('transport-val-display'),
        agriculture: document.getElementById('agriculture-val-display'),
        buildings: document.getElementById('buildings-val-display'),
        energyMt: document.getElementById('energy-mt-display'),
        industryMt: document.getElementById('industry-mt-display'),
        transportMt: document.getElementById('transport-mt-display'),
        agricultureMt: document.getElementById('agriculture-mt-display'),
        buildingsMt: document.getElementById('buildings-mt-display')
      };

      const bars = {
        energy: document.getElementById('bar-energy'),
        industry: document.getElementById('bar-industry'),
        transport: document.getElementById('bar-transport'),
        agriculture: document.getElementById('bar-agriculture'),
        buildings: document.getElementById('bar-buildings')
      };

      const shapBars = {
        energy: document.getElementById('shap-bar-energy'),
        industry: document.getElementById('shap-bar-industry'),
        transport: document.getElementById('shap-bar-transport'),
        agriculture: document.getElementById('shap-bar-agriculture'),
        buildings: document.getElementById('shap-bar-buildings')
      };

      const shapLabels = {
        energy: document.getElementById('shap-energy'),
        industry: document.getElementById('shap-industry'),
        transport: document.getElementById('shap-transport'),
        agriculture: document.getElementById('shap-agriculture'),
        buildings: document.getElementById('shap-buildings')
      };

      const drawer = document.getElementById('benchmark-drawer');
      const drawerToggleBtn = document.getElementById('toggle-benchmark-drawer');
      const drawerToggleHeader = document.getElementById('toggle-benchmark-drawer-header');
      const drawerChevron = document.getElementById('drawer-chevron');
      const activeCountryLabel = document.getElementById('active-country-label');
      const headerCountryLabel = document.getElementById('header-country-label');
      const countryPresetsContainer = document.getElementById('country-presets-container');
      const countrySearchInput = document.getElementById('country-search-input');

      // Drawer toggle handler
      function toggleDrawer() {
        drawer.classList.toggle('hidden');
        drawerChevron.classList.toggle('rotate-180');
      }
      if (drawerToggleBtn) drawerToggleBtn.addEventListener('click', toggleDrawer);
      if (drawerToggleHeader) drawerToggleHeader.addEventListener('click', toggleDrawer);

      // Strict Mathematical Auto-Rebalancing for 5 Sliders (Sum = 100%)
      function updateAllocation(changedSector, targetVal) {
        targetVal = Math.max(0, Math.min(100, Math.round(targetVal)));
        const sectorKeys = ['energy', 'industry', 'transport', 'agriculture', 'buildings'];
        const otherKeys = sectorKeys.filter(k => k !== changedSector);
        const targetOtherSum = 100 - targetVal;
        const currentOtherSum = otherKeys.reduce((sum, k) => sum + state.sectors[k], 0);

        state.sectors[changedSector] = targetVal;

        if (currentOtherSum === 0) {
          const base = Math.floor(targetOtherSum / otherKeys.length);
          let rem = targetOtherSum % otherKeys.length;
          otherKeys.forEach(k => {
            state.sectors[k] = base + (rem > 0 ? 1 : 0);
            if (rem > 0) rem--;
          });
        } else {
          let assignedSum = 0;
          otherKeys.forEach((k, idx) => {
            if (idx === otherKeys.length - 1) {
              state.sectors[k] = Math.max(0, targetOtherSum - assignedSum);
            } else {
              const scaled = Math.round((state.sectors[k] / currentOtherSum) * targetOtherSum);
              const clamped = Math.max(0, Math.min(targetOtherSum - assignedSum, scaled));
              state.sectors[k] = clamped;
              assignedSum += clamped;
            }
          });
        }

        // Strict mathematical correction for rounding residuals
        let sum = Object.values(state.sectors).reduce((a, b) => a + b, 0);
        if (sum !== 100) {
          const diff = 100 - sum;
          const largestKey = otherKeys.reduce((a, b) => state.sectors[a] >= state.sectors[b] ? a : b);
          state.sectors[largestKey] = Math.max(0, state.sectors[largestKey] + diff);
        }

        renderSliderDisplays();
        debouncedPipelineRun();
      }

      // Update Slider Visuals and Displays
      function renderSliderDisplays() {
        const sectorKeys = ['energy', 'industry', 'transport', 'agriculture', 'buildings'];
        sectorKeys.forEach(sec => {
          const val = state.sectors[sec];
          if (sliders[sec]) sliders[sec].value = val;
          if (displays[sec]) {
            displays[sec].innerHTML = `${val}<span class="text-sm font-normal text-outline">%</span>`;
          }
          if (bars[sec]) bars[sec].style.width = `${val}%`;

          // Sector Mt display
          const secMt = Math.round((val / 100) * state.totalBaselineMt);
          if (displays[`${sec}Mt`]) {
            displays[`${sec}Mt`].textContent = `${secMt.toLocaleString()} Mt`;
          }
        });

        // Verification indicator
        const total = sectorKeys.reduce((acc, k) => acc + state.sectors[k], 0);
        const sumBadge = document.getElementById('allocation-badge');
        const sumText = document.getElementById('allocation-sum-text');
        if (total === 100) {
          sumBadge.className = 'flex items-center gap-2 px-3 py-1 rounded-full bg-tertiary/10 text-tertiary border border-tertiary/30 font-label-mono text-xs';
          sumText.textContent = 'Total Sector Allocation: 100% (Simplex Balanced)';
        } else {
          sumBadge.className = 'flex items-center gap-2 px-3 py-1 rounded-full bg-error/10 text-error border border-error/30 font-label-mono text-xs';
          sumText.textContent = `Total Allocation: ${total}% (Unbalanced)`;
        }
      }

      // Debounce pipeline execution to keep UI hyper-responsive
      function debouncedPipelineRun() {
        if (state.debounceTimer) clearTimeout(state.debounceTimer);
        state.debounceTimer = setTimeout(() => {
          triggerBackendPipeline();
        }, 120);
      }

      // Connect to Backend REST API Endpoints
      async function triggerBackendPipeline() {
        const payload = {
          sectors: state.sectors,
          country: state.country,
          baselineMt: state.totalBaselineMt,
          benchmark_reduction_pct: state.benchmarkPct
        };

        try {
          const [archRes, equivRes] = await Promise.all([
            fetch(`${API_BASE}/api/nearest_archetype`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload)
            }).then(r => r.json()),
            fetch(`${API_BASE}/api/calculate_equivalence`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload)
            }).then(r => r.json())
          ]);

          // 1. Bind Nearest Archetype & CLR Space Metrics
          if (archRes && !archRes.error) {
            bindArchetypeToDOM(archRes);
          }

          // 2. Bind PRD Equivalence Calculations
          if (equivRes && !equivRes.error) {
            bindEquivalenceToDOM(equivRes);
          }

          // Connection status indicator
          document.getElementById('backend-status-dot').className = 'w-2 h-2 rounded-full bg-tertiary animate-pulse';
          document.getElementById('backend-status-text').textContent = 'Backend Connected';
        } catch (err) {
          console.error('[API Connection Warning]', err);
          document.getElementById('backend-status-dot').className = 'w-2 h-2 rounded-full bg-error';
          document.getElementById('backend-status-text').textContent = 'Backend Offline';
        }
      }

      // Bind Nearest Archetype from ML clustering
      function bindArchetypeToDOM(archRes) {
        const titleEl = document.getElementById('archetype-title');
        const pillEl = document.getElementById('archetype-cluster-pill');
        const descEl = document.getElementById('archetype-desc');
        const driverEl = document.getElementById('archetype-driver');
        const iconEl = document.getElementById('archetype-icon');
        const iconWrapEl = document.getElementById('archetype-icon-wrapper');
        const distEl = document.getElementById('archetype-dist-label');
        const boundaryDistEl = document.getElementById('boundary-distance');
        const countEl = document.getElementById('archetype-country-count');
        const recEl = document.getElementById('xai-recommendation-short');

        const clusterId = archRes.nearest_cluster_id;
        const archName = archRes.nearest_archetype;
        const details = archRes.archetype || {};

        if (titleEl) titleEl.textContent = archName;
        if (pillEl) pillEl.textContent = `Cluster ${clusterId} · ${archName.split(' ')[0]}-Dominant`;
        if (descEl && details.desc) descEl.textContent = details.desc;
        if (driverEl && details.driver) driverEl.textContent = details.driver;
        if (iconEl && details.icon) iconEl.textContent = details.icon;
        if (recEl && details.recommendation) recEl.textContent = details.recommendation;

        const minDist = archRes.minimum_distance;
        if (distEl) distEl.textContent = `CLR Δ = ${minDist.toFixed(3)}`;
        if (boundaryDistEl) boundaryDistEl.textContent = `Minimum Centroid Δ = ${minDist.toFixed(3)}`;

        // Cluster size metadata
        const clusterCounts = { 0: 196, 1: 7, 2: 5, "-1": 17 };
        if (countEl) countEl.textContent = clusterCounts[clusterId] || 1;

        // Color branding by cluster
        if (iconWrapEl && details.color) {
          iconWrapEl.style.borderColor = `${details.color}50`;
          iconWrapEl.style.color = details.color;
        }

        // Feature vector displays (CLR coordinates)
        if (archRes.clr_coordinates) {
          const clr = archRes.clr_coordinates;
          const share = archRes.input_normalized_shares;
          const sectors = ['energy', 'industry', 'transport', 'agriculture', 'buildings'];
          sectors.forEach(s => {
            const capSec = s.charAt(0).toUpperCase() + s.slice(1);
            const clrVal = clr[capSec] !== undefined ? clr[capSec].toFixed(2) : '0.00';
            const shareVal = (share[capSec] * 100).toFixed(0);
            if (shapLabels[s]) {
              shapLabels[s].textContent = `${shareVal}% (CLR: ${clrVal > 0 ? '+' : ''}${clrVal})`;
            }
            if (shapBars[s]) {
              // Scale visual bar from 0 to 100
              shapBars[s].style.width = `${Math.min(100, Math.max(8, shareVal * 2))}%`;
            }
          });
        }

        // Highlight matching surrogate rule in XAI card
        highlightMatchingRule(clusterId);
      }

      // Highlight matching rule in Explainable AI ledger
      function highlightMatchingRule(clusterId) {
        if (!state.rulesData || !state.rulesData.xai_rules) return;
        
        const primaryRuleEl = document.getElementById('primary-rule-eval');
        const rationaleEl = document.getElementById('rule-rationale-text');
        
        // Find matching rule for this cluster
        const rule = state.rulesData.xai_rules.find(r => r.cluster_id === clusterId);
        if (rule) {
          if (primaryRuleEl) primaryRuleEl.textContent = rule.rule_text;
          if (rationaleEl) {
            const rationales = {
              0: "Energy sector accounts for the structural centroid of the national emissions profile across core global economies.",
              1: "Agricultural cultivation, livestock enteric fermentation, and land use predominate total emissions.",
              2: "Manufacturing, mineral smelting, and concentrated industrial chemical processes constitute near 100% of emissions.",
              "-1": "Disproportionate international transport corridors, mobility infrastructure, or specialized trade logistics define national profile."
            };
            rationaleEl.textContent = rationales[clusterId] || `Bounding box split separates Cluster ${clusterId} with high fidelity.`;
          }
        }

        // Highlight in audit list
        document.querySelectorAll('.rule-item').forEach(item => {
          if (parseInt(item.dataset.clusterId, 10) === clusterId) {
            item.className = 'rule-item p-2.5 rounded-lg bg-primary/10 border border-primary/40 text-xs font-label-mono text-[#f4f4f5] transition-all';
          } else {
            item.className = 'rule-item p-2 rounded-lg bg-[#222225] border border-[#2e2e33] text-[11px] font-label-mono text-[#a1a1aa] transition-all hover:border-[#3e3e44]';
          }
        });
      }

      // Bind PRD Mathematical Equivalence Results to DOM
      function bindEquivalenceToDOM(equivRes) {
        const item = (equivRes.results && equivRes.results.length > 0) ? equivRes.results[0] : null;
        if (!item) return;

        const totalGg = item.country_total_emissions_Gg || (state.totalBaselineMt * 1000);
        const deltaGg = item.delta_e_target_Gg || (totalGg * (state.benchmarkPct / 100.0));
        const domSector = item.dominant_sector || 'Energy';
        const domBaselineGg = item.dominant_sector_baseline_emissions_Gg || (totalGg * (state.sectors.energy / 100));
        const domSharePct = item.dominant_sector_share_pct || state.sectors.energy;
        const cutPct = item.sector_activity_cut_pct || ((deltaGg / domBaselineGg) * 100);

        // Convert Gg to Mt: 1 Gg = 0.001 Mt
        const totalMt = totalGg / 1000.0;
        const deltaMt = deltaGg / 1000.0;
        const domBaselineMt = domBaselineGg / 1000.0;

        // Hero units
        let displayTotal = totalMt;
        let displayUnit = 'Mt CO₂e / yr';
        if (state.unitMode === 'gt') {
          displayTotal = totalMt / 1000.0;
          displayUnit = 'Gt CO₂e / yr';
        }

        const heroValEl = document.getElementById('hero-co2-val');
        const heroUnitEl = document.getElementById('hero-co2-unit');
        const heroStatusEl = document.getElementById('hero-country-status');
        const targetDeltaEl = document.getElementById('target-delta-val');
        const benchLabelEl = document.getElementById('benchmark-label-val');

        if (heroValEl) heroValEl.textContent = displayTotal >= 1000 ? Math.round(displayTotal).toLocaleString() : displayTotal.toFixed(2);
        if (heroUnitEl) heroUnitEl.textContent = displayUnit;
        if (heroStatusEl) heroStatusEl.textContent = `${state.countryName} (${state.country}) · Total Baseline`;
        if (targetDeltaEl) targetDeltaEl.textContent = `${deltaMt.toFixed(2)} Mt`;
        if (benchLabelEl) benchLabelEl.textContent = `${state.benchmarkPct.toFixed(1)}% Benchmark Target`;

        // 4-Grid Equivalence Cards
        const cutValEl = document.getElementById('eq-activity-cut-val');
        const domDescEl = document.getElementById('eq-dominant-desc');
        const domBaseEl = document.getElementById('eq-dominant-baseline-val');
        const domShareEl = document.getElementById('eq-dominant-share-desc');
        const treesEl = document.getElementById('eq-trees-val');
        const coalEl = document.getElementById('eq-coal-val');
        const mathProofEl = document.getElementById('math-proof-label');
        const paceBar = document.getElementById('pace-bar');

        if (cutValEl) cutValEl.textContent = `${cutPct.toFixed(2)}% Cut`;
        if (domDescEl) domDescEl.textContent = `${domSector} sector reduction required to match benchmark target`;
        if (domBaseEl) domBaseEl.textContent = `${domBaselineMt.toFixed(1)} Mt`;
        if (domShareEl) domShareEl.textContent = `${domSector} accounts for ${domSharePct.toFixed(1)}% of baseline emissions`;

        // Real-world physical conversion: EPA Standard
        // 1 Mt CO2 approx 45.45 million tree seedlings grown for 10 years
        const treeSeedlingsBillion = ((deltaMt * 45.45) / 1000.0).toFixed(1);
        if (treesEl) treesEl.textContent = `${treeSeedlingsBillion} Billion`;

        // Standard 500MW coal plant = 3.89 Mt CO2 per year
        const coalPlantsRetired = Math.round(deltaMt / 3.89);
        if (coalEl) coalEl.textContent = `${coalPlantsRetired.toLocaleString()} Plants`;

        if (mathProofEl) mathProofEl.textContent = `Formula: ΔE (${deltaMt.toFixed(1)} Mt) / Baseline (${domBaselineMt.toFixed(1)} Mt) = ${cutPct.toFixed(2)}%`;
        if (paceBar) paceBar.style.width = `${Math.min(100, Math.max(5, cutPct))}%`;
      }

      // Initial Fetch & Bootstrapping
      async function bootApplication() {
        try {
          const [dataRes, rulesRes] = await Promise.all([
            fetch(`${API_BASE}/api/data`).then(r => r.json()),
            fetch(`${API_BASE}/api/rules`).then(r => r.json())
          ]);

          state.countriesData = dataRes.clustered_proportions || [];
          state.emissionsData = dataRes.macro_sector_emissions || [];
          state.rulesData = rulesRes || {};

          // 1. Populate Country Presets in Drawer
          populateCountryDrawer();

          // 2. Populate Decision Tree Rules in XAI Card
          populateRulesLedger();

          // 3. Load default initial country: USA
          selectCountry('USA');

        } catch (err) {
          console.error('[Initialization Error]', err);
          document.getElementById('backend-status-dot').className = 'w-2 h-2 rounded-full bg-error';
          document.getElementById('backend-status-text').textContent = 'Backend Offline';
        }
      }

      // Populate Country Selector Drawer
      function populateCountryDrawer() {
        if (!countryPresetsContainer || !state.countriesData.length) return;
        countryPresetsContainer.innerHTML = '';

        // Priority preset countries across different clusters
        const priorityCodes = ['USA', 'CHN', 'IND', 'DEU', 'BRA', 'JPN', 'SGP', 'ASM', 'MHL', 'GBR', 'FRA', 'IDN'];

        // Sort: priority countries first, then alphabetical
        const sortedCountries = [...state.countriesData].sort((a, b) => {
          const aPri = priorityCodes.indexOf(a.Country_code_A3);
          const bPri = priorityCodes.indexOf(b.Country_code_A3);
          if (aPri !== -1 && bPri !== -1) return aPri - bPri;
          if (aPri !== -1) return -1;
          if (bPri !== -1) return 1;
          return a.Name.localeCompare(b.Name);
        });

        sortedCountries.forEach(c => {
          const code = c.Country_code_A3;
          const name = c.Name;
          const cluster = c.Cluster;

          // Find emission total
          const emissRow = state.emissionsData.find(e => e.Country_code_A3 === code);
          let totalMt = 0;
          if (emissRow) {
            const sectors = ['Energy', 'Industry', 'Transport', 'Agriculture', 'Buildings'];
            const sumGg = sectors.reduce((acc, s) => acc + (emissRow[s] || 0), 0);
            totalMt = Math.round(sumGg / 1000.0);
          }

          const btn = document.createElement('button');
          btn.className = `country-pill flex flex-col p-2.5 rounded-xl border text-left transition-all group ${code === state.country ? 'bg-surface-container-highest border-primary/40' : 'bg-surface-container hover:bg-surface-container-high border-surface-container-highest'}`;
          btn.dataset.code = code;
          btn.dataset.name = name;

          btn.innerHTML = `
            <div class="flex items-center justify-between w-full mb-1">
              <span class="font-label-md text-xs font-semibold text-on-surface group-hover:text-primary truncate">${name}</span>
              <span class="text-[10px] font-label-mono px-1 rounded bg-[#111111] text-outline">${code}</span>
            </div>
            <div class="flex items-center justify-between text-[10px] font-label-mono text-outline">
              <span>${totalMt >= 1000 ? (totalMt/1000).toFixed(1) + ' Gt' : totalMt + ' Mt'}</span>
              <span class="text-primary font-medium">Cl ${cluster}</span>
            </div>
          `;

          btn.addEventListener('click', () => {
            selectCountry(code);
            drawer.classList.add('hidden');
            drawerChevron.classList.remove('rotate-180');
          });

          countryPresetsContainer.appendChild(btn);
        });
      }

      // Populate Explainable AI Rules Ledger
      function populateRulesLedger() {
        const rulesContainer = document.getElementById('all-rules-container');
        if (!rulesContainer || !state.rulesData || !state.rulesData.xai_rules) return;

        const rules = state.rulesData.xai_rules;
        rulesContainer.innerHTML = '';

        rules.forEach((rule, idx) => {
          const div = document.createElement('div');
          div.className = 'rule-item p-2 rounded-lg bg-[#222225] border border-[#2e2e33] text-[11px] font-label-mono text-[#a1a1aa] transition-all hover:border-[#3e3e44]';
          div.dataset.clusterId = rule.cluster_id;

          div.innerHTML = `
            <div class="flex items-center justify-between mb-1">
              <span class="font-semibold text-primary">Rule #${idx + 1} · Cluster ${rule.cluster_id}</span>
              <span class="text-[10px] px-1.5 py-0.2 rounded bg-[#111111] text-tertiary">${rule.sample_count} training samples</span>
            </div>
            <div class="text-[#e4e1e5] font-medium leading-relaxed">${rule.rule_text}</div>
          `;

          rulesContainer.appendChild(div);
        });
      }

      // Select and Load Real Country Data
      function selectCountry(countryCode) {
        const propRow = state.countriesData.find(c => c.Country_code_A3 === countryCode);
        const emissRow = state.emissionsData.find(e => e.Country_code_A3 === countryCode);

        if (!propRow) return;

        state.country = countryCode;
        state.countryName = propRow.Name;

        // Calculate total baseline in Mt
        if (emissRow) {
          const sumGg = ['Energy', 'Industry', 'Transport', 'Agriculture', 'Buildings']
            .reduce((acc, s) => acc + (emissRow[s] || 0), 0);
          state.totalBaselineMt = Math.max(1, Math.round(sumGg / 1000.0));
        }

        // Convert decimal proportions to integer % summing to 100
        const sectors = ['Energy', 'Industry', 'Transport', 'Agriculture', 'Buildings'];
        let rawPercents = sectors.map(s => Math.round((propRow[s] || 0) * 100));
        let sum = rawPercents.reduce((a, b) => a + b, 0);
        if (sum !== 100) {
          const diff = 100 - sum;
          rawPercents[0] += diff; // Adjust on Energy
        }

        state.sectors = {
          energy: Math.max(0, rawPercents[0]),
          industry: Math.max(0, rawPercents[1]),
          transport: Math.max(0, rawPercents[2]),
          agriculture: Math.max(0, rawPercents[3]),
          buildings: Math.max(0, rawPercents[4])
        };

        // Update Labels
        if (activeCountryLabel) activeCountryLabel.textContent = `${state.countryName} (${countryCode})`;
        if (headerCountryLabel) headerCountryLabel.textContent = `${state.countryName} (${countryCode})`;

        // Highlight active button in drawer
        document.querySelectorAll('.country-pill').forEach(btn => {
          if (btn.dataset.code === countryCode) {
            btn.classList.add('bg-surface-container-highest', 'border-primary/40');
            btn.classList.remove('bg-surface-container');
          } else {
            btn.classList.remove('bg-surface-container-highest', 'border-primary/40');
            btn.classList.add('bg-surface-container');
          }
        });

        renderSliderDisplays();
        triggerBackendPipeline();
      }

      // Slider Event Listeners
      Object.keys(sliders).forEach(sec => {
        const slider = sliders[sec];
        if (!slider) return;
        slider.addEventListener('input', (e) => {
          updateAllocation(sec, parseFloat(e.target.value));
        });
      });

      // Step button event listeners (+/- 1%)
      document.querySelectorAll('.step-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          const target = btn.dataset.target;
          const dir = parseInt(btn.dataset.dir, 10);
          updateAllocation(target, state.sectors[target] + dir);
        });
      });

      // Reset Simulation Button
      const resetBtn = document.getElementById('reset-sim-btn');
      if (resetBtn) {
        resetBtn.addEventListener('click', () => {
          selectCountry(state.country);
        });
      }

      // Preset Archetype Scenario Buttons (Centroids from model_training & PRD)
      const scenarios = {
        cluster0: { energy: 45, industry: 18, transport: 18, agriculture: 12, buildings: 7 },
        cluster1: { energy: 1, industry: 4, transport: 1, agriculture: 93, buildings: 1 },
        cluster2: { energy: 1, industry: 96, transport: 1, agriculture: 1, buildings: 1 },
        transit:  { energy: 18, industry: 12, transport: 42, agriculture: 20, buildings: 8 },
        balanced: { energy: 20, industry: 20, transport: 20, agriculture: 20, buildings: 20 }
      };

      document.querySelectorAll('.scenario-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          const sc = scenarios[btn.dataset.scenario];
          if (sc) {
            state.sectors = { ...sc };
            renderSliderDisplays();
            debouncedPipelineRun();
          }
        });
      });

      // Benchmark Cut Selection Buttons (5%, 10%, 15%)
      document.querySelectorAll('.bench-cut-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          document.querySelectorAll('.bench-cut-btn').forEach(b => {
            b.className = 'bench-cut-btn px-2 py-1 rounded text-outline hover:text-[#f4f4f5]';
          });
          btn.className = 'bench-cut-btn px-2 py-1 rounded bg-[#222225] text-primary font-semibold';
          state.benchmarkPct = parseFloat(btn.dataset.cut);
          triggerBackendPipeline();
        });
      });

      // Unit Toggle Buttons (Mt / Gt)
      document.querySelectorAll('.unit-toggle-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          document.querySelectorAll('.unit-toggle-btn').forEach(b => {
            b.className = 'unit-toggle-btn px-2 py-1 rounded text-outline hover:text-[#f4f4f5]';
          });
          btn.className = 'unit-toggle-btn px-2 py-1 rounded bg-[#222225] text-primary font-semibold';
          state.unitMode = btn.dataset.unit;
          triggerBackendPipeline();
        });
      });

      // Country Search Filter (Searches 225 real nations)
      if (countrySearchInput) {
        countrySearchInput.addEventListener('input', (e) => {
          const q = e.target.value.toLowerCase().trim();
          document.querySelectorAll('.country-pill').forEach(pill => {
            const name = (pill.dataset.name || '').toLowerCase();
            const code = (pill.dataset.code || '').toLowerCase();
            if (name.includes(q) || code.includes(q)) {
              pill.classList.remove('hidden');
            } else {
              pill.classList.add('hidden');
            }
          });
        });
      }

      // Boot application on load
      bootApplication();
    })();
  </script>
</body>
</html>
'''

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(HTML_CONTENT)

print(f"Successfully generated frontend/index.html ({len(HTML_CONTENT)} bytes)")
