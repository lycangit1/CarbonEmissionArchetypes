# -*- coding: utf-8 -*-
"""
Generates frontend/index.html with:
1. Section 0: Algorithmic Validation (Objectives 2 & 3)
   - Scientific Consensus Card: Winning Model and Optimal Archetypes
   - Small clean data table showing Silhouette, Davies-Bouldin, and Calinski-Harabasz indices
   - Complete 4-Algorithm Benchmark Leaderboard
2. Dynamic adaptation in the main interactive simulator below:
   - Simulator dynamically runs against the consensus winning model
   - Dynamic model badges and archetype classification
   - Mode switcher between Validated Consensus (k=2) and Detailed Sub-Archetypes (k=4)
3. Preserves all country data, auto-rebalancing sliders, and physical impact calculations.
"""

HTML_CONTENT = r'''<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Global Carbon Archetype Simulator · Objectives 2 & 3 Validated</title>
  
  <!-- Modern Clean Typography & Material Icons -->
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet"/>
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet"/>

  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: "class",
      theme: {
        extend: {
          colors: {
            brand: {
              energy: "#f97316",      /* Warm orange */
              industry: "#8b5cf6",    /* Royal violet */
              transport: "#06b6d4",   /* Cyan */
              agriculture: "#10b981", /* Emerald */
              buildings: "#f59e0b"    /* Amber */
            }
          },
          fontFamily: {
            sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto", "sans-serif"],
            display: ["Space Grotesk", "Inter", "sans-serif"]
          }
        }
      }
    };
  </script>

  <style>
    /* Custom Slider Accent Styles */
    input[type=range] {
      -webkit-appearance: none;
      appearance: none;
      background: #27272a;
      border-radius: 9999px;
      height: 8px;
    }
    input[type=range]::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: #ffffff;
      cursor: pointer;
      box-shadow: 0 0 10px rgba(0,0,0,0.5);
      border: 2px solid #52525b;
      transition: transform 0.1s ease, border-color 0.1s ease;
    }
    input[type=range]::-webkit-slider-thumb:hover {
      transform: scale(1.15);
      border-color: #f97316;
    }
    input[type=range]::-moz-range-thumb {
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: #ffffff;
      cursor: pointer;
      border: 2px solid #52525b;
    }
  </style>
</head>

<body class="bg-[#0c0c0e] text-[#f4f4f5] font-sans antialiased min-h-screen selection:bg-orange-500 selection:text-white">

  <!-- Main Container with Generous Padding & Whitespace -->
  <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10 lg:py-14 space-y-10">

    <!-- Header & Context -->
    <header class="text-center space-y-3 pb-2">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-800/80 border border-zinc-700 text-xs text-zinc-300 font-medium shadow-sm">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span>EDGAR Global Emissions Database · Objectives 2 & 3 Validated</span>
      </div>
      <h1 class="text-3xl sm:text-4xl lg:text-5xl font-bold font-display tracking-tight text-white">
        Global Carbon Archetype Simulator
      </h1>
      <p class="text-base sm:text-lg text-zinc-400 max-w-2xl mx-auto leading-relaxed">
        Explore how shifting national sector emissions reclassifies economies into distinct climate transition archetypes.
      </p>
    </header>

    <!-- SECTION 0: Algorithmic Validation (Objectives 2 & 3) -->
    <section class="bg-[#16161a] border border-zinc-800 rounded-2xl p-6 sm:p-8 shadow-xl space-y-6" id="section-algorithmic-validation">
      
      <!-- Section Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-zinc-800/80 pb-5">
        <div>
          <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded-md bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <span class="material-symbols-outlined text-[16px]">verified</span>
            <span>Phase-I Research Methodology · Objectives 2 & 3</span>
          </div>
          <h2 class="text-xl sm:text-2xl font-bold font-display text-white flex items-center gap-2.5">
            <span>Algorithmic Validation (Objectives 2 & 3)</span>
          </h2>
          <p class="text-sm text-zinc-400 mt-1">
            Empirical evaluation across 4 clustering algorithms and 3 internal validation indices to dynamically discover optimal national carbon archetypes without human priors.
          </p>
        </div>

        <div class="flex items-center gap-2">
          <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-700/80 text-xs font-mono text-zinc-300">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span id="benchmark-total-runs">59 Runs Evaluated</span>
          </span>
        </div>
      </div>

      <!-- Scientific Consensus Hero Card -->
      <div class="bg-gradient-to-br from-zinc-900 via-zinc-900 to-indigo-950/30 border border-indigo-500/30 rounded-xl p-5 sm:p-6 shadow-lg">
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div class="space-y-3 flex-1">
            <div class="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-medium">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
              <span>Scientific Consensus Achieved</span>
            </div>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
              <!-- Card 1: Winning Model -->
              <div class="bg-zinc-800/60 border border-zinc-700/60 rounded-lg p-4">
                <span class="text-xs uppercase tracking-wider text-zinc-400 font-medium">Winning Model</span>
                <div class="text-xl sm:text-2xl font-bold font-display text-white mt-1 flex items-center gap-2" id="consensus-winning-algo">
                  <span>K-Means</span>
                  <span class="text-xs px-2 py-0.5 rounded bg-orange-500/20 text-orange-400 border border-orange-500/30 font-mono">Rank 1</span>
                </div>
                <p class="text-xs text-zinc-400 mt-1.5 leading-relaxed">
                  Superior separation and cohesion across continuous CLR compositional coordinates.
                </p>
              </div>

              <!-- Card 2: Optimal Archetypes -->
              <div class="bg-zinc-800/60 border border-zinc-700/60 rounded-lg p-4">
                <span class="text-xs uppercase tracking-wider text-zinc-400 font-medium">Optimal Archetypes</span>
                <div class="text-xl sm:text-2xl font-bold font-display text-emerald-400 mt-1 flex items-center gap-2" id="consensus-optimal-k">
                  <span>2 Archetypes</span>
                  <span class="text-xs px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-mono">k = 2</span>
                </div>
                <p class="text-xs text-zinc-400 mt-1.5 leading-relaxed">
                  Global macro-partitioning: Energy-Dominant vs. Agrarian/Micro-Economies.
                </p>
              </div>
            </div>
          </div>

          <!-- Overall Composite Score Badge -->
          <div class="lg:text-right shrink-0 bg-zinc-900/90 border border-zinc-800 rounded-xl p-5 flex lg:flex-col items-center lg:items-end justify-between gap-2 min-w-[200px]">
            <div>
              <span class="text-xs uppercase tracking-wider text-zinc-400 font-medium block">Consensus Score</span>
              <div class="text-3xl sm:text-4xl font-black font-display text-white font-mono" id="consensus-composite-score">0.9449</div>
            </div>
            <span class="text-[11px] text-zinc-400 max-w-[180px] lg:text-right">
              Harmonized across Silhouette, Davies-Bouldin, & Calinski-Harabasz
            </span>
          </div>
        </div>
      </div>

      <!-- Trio of Validation Indices for Winning Setup -->
      <div class="space-y-3">
        <div class="flex items-center justify-between">
          <h3 class="text-sm font-semibold uppercase tracking-wider text-zinc-300 font-display flex items-center gap-2">
            <span class="material-symbols-outlined text-orange-400 text-[18px]">analytics</span>
            <span>Tri-Index Validation Metrics (Winning Configuration)</span>
          </h3>
          <span class="text-xs text-zinc-500">Higher is better for S & CH · Lower is better for DB</span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <!-- Metric 1: Silhouette Score -->
          <div class="bg-zinc-900/90 border border-zinc-800 rounded-xl p-4 space-y-1.5 hover:border-zinc-700 transition-colors">
            <div class="flex items-center justify-between">
              <span class="text-xs font-medium text-zinc-400 uppercase tracking-wider">Silhouette Score (S)</span>
              <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Higher = Better</span>
            </div>
            <div class="text-2xl font-bold font-mono text-white" id="metric-sil">0.7136</div>
            <p class="text-[11px] text-zinc-400">Measures cluster separation & cohesion (theoretical max: +1.0).</p>
          </div>

          <!-- Metric 2: Davies-Bouldin Index -->
          <div class="bg-zinc-900/90 border border-zinc-800 rounded-xl p-4 space-y-1.5 hover:border-zinc-700 transition-colors">
            <div class="flex items-center justify-between">
              <span class="text-xs font-medium text-zinc-400 uppercase tracking-wider">Davies-Bouldin Index (DB)</span>
              <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">Lower = Better</span>
            </div>
            <div class="text-2xl font-bold font-mono text-white" id="metric-db">0.8074</div>
            <p class="text-[11px] text-zinc-400">Cluster compactness-to-separation ratio (zero is ideal).</p>
          </div>

          <!-- Metric 3: Calinski-Harabasz Index -->
          <div class="bg-zinc-900/90 border border-zinc-800 rounded-xl p-4 space-y-1.5 hover:border-zinc-700 transition-colors">
            <div class="flex items-center justify-between">
              <span class="text-xs font-medium text-zinc-400 uppercase tracking-wider">Calinski-Harabasz (CH)</span>
              <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/20">Higher = Better</span>
            </div>
            <div class="text-2xl font-bold font-mono text-white" id="metric-ch">141.61</div>
            <p class="text-[11px] text-zinc-400">Variance ratio criterion confirming sharp density boundaries.</p>
          </div>
        </div>
      </div>

      <!-- Multi-Algorithm Benchmark Comparison Table -->
      <div class="space-y-3">
        <div class="flex items-center justify-between">
          <h3 class="text-sm font-semibold uppercase tracking-wider text-zinc-300 font-display flex items-center gap-2">
            <span class="material-symbols-outlined text-indigo-400 text-[18px]">table_chart</span>
            <span>4-Algorithm Benchmark Leaderboard</span>
          </h3>
          <span class="text-xs text-zinc-500 font-mono">CLR Compositional Space (225 Nations)</span>
        </div>

        <div class="overflow-x-auto rounded-xl border border-zinc-800">
          <table class="w-full text-left text-xs">
            <thead class="bg-zinc-900/90 text-zinc-400 font-semibold uppercase tracking-wider border-b border-zinc-800">
              <tr>
                <th class="py-3 px-4">Algorithm</th>
                <th class="py-3 px-4">Optimal Parameters</th>
                <th class="py-3 px-4 text-right">Silhouette (S ↑)</th>
                <th class="py-3 px-4 text-right">Davies-Bouldin (DB ↓)</th>
                <th class="py-3 px-4 text-right">Calinski-Harabasz (CH ↑)</th>
                <th class="py-3 px-4 text-right">Consensus Score</th>
                <th class="py-3 px-4 text-center">Status</th>
              </tr>
            </thead>
            <tbody id="benchmark-table-body" class="divide-y divide-zinc-800/80 bg-zinc-900/40 font-mono">
              <!-- Dynamically populated from /api/evaluate_models -->
              <tr class="hover:bg-zinc-800/40">
                <td class="py-3 px-4 font-sans font-medium text-white flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                  <span>K-Means</span>
                </td>
                <td class="py-3 px-4 text-zinc-300">k = 2</td>
                <td class="py-3 px-4 text-right text-emerald-400">0.7136</td>
                <td class="py-3 px-4 text-right text-blue-400">0.8074</td>
                <td class="py-3 px-4 text-right text-purple-400">141.61</td>
                <td class="py-3 px-4 text-right text-white font-bold">0.9449</td>
                <td class="py-3 px-4 text-center">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px]">Consensus Winner</span>
                </td>
              </tr>
              <tr class="hover:bg-zinc-800/40">
                <td class="py-3 px-4 font-sans font-medium text-zinc-200">Hierarchical (Agglomerative)</td>
                <td class="py-3 px-4 text-zinc-300">k = 2</td>
                <td class="py-3 px-4 text-right text-emerald-400">0.7136</td>
                <td class="py-3 px-4 text-right text-blue-400">0.8074</td>
                <td class="py-3 px-4 text-right text-purple-400">141.61</td>
                <td class="py-3 px-4 text-right text-zinc-200">0.9449</td>
                <td class="py-3 px-4 text-center">
                  <span class="px-2 py-0.5 rounded bg-zinc-800 text-zinc-300 text-[10px]">Tied Consensus</span>
                </td>
              </tr>
              <tr class="hover:bg-zinc-800/40">
                <td class="py-3 px-4 font-sans font-medium text-zinc-200">Gaussian Mixture Model (GMM)</td>
                <td class="py-3 px-4 text-zinc-300">k = 2</td>
                <td class="py-3 px-4 text-right text-emerald-400">0.7136</td>
                <td class="py-3 px-4 text-right text-blue-400">0.8074</td>
                <td class="py-3 px-4 text-right text-purple-400">141.61</td>
                <td class="py-3 px-4 text-right text-zinc-200">0.9449</td>
                <td class="py-3 px-4 text-center">
                  <span class="px-2 py-0.5 rounded bg-zinc-800 text-zinc-300 text-[10px]">Tied Consensus</span>
                </td>
              </tr>
              <tr class="hover:bg-zinc-800/40">
                <td class="py-3 px-4 font-sans font-medium text-zinc-300">DBSCAN</td>
                <td class="py-3 px-4 text-zinc-400">eps=2.0, min_samples=2 (k=6)</td>
                <td class="py-3 px-4 text-right text-zinc-400">0.5539</td>
                <td class="py-3 px-4 text-right text-zinc-400">1.1000</td>
                <td class="py-3 px-4 text-right text-zinc-400">64.62</td>
                <td class="py-3 px-4 text-right text-zinc-400">0.7043</td>
                <td class="py-3 px-4 text-center">
                  <span class="px-2 py-0.5 rounded bg-zinc-800/50 text-zinc-400 text-[10px]">Density Baseline</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </section>

    <!-- SECTION 1: Country Baseline (Top) -->
    <section class="bg-[#16161a] border border-zinc-800 rounded-2xl p-6 sm:p-8 shadow-xl space-y-6">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-zinc-800/80 pb-5">
        <div>
          <h2 class="text-lg font-semibold font-display text-white flex items-center gap-2">
            <span class="material-symbols-outlined text-orange-400 text-[22px]">public</span>
            <span>Select a Nation to Inspect</span>
          </h2>
          <p class="text-sm text-zinc-400 mt-0.5">
            Load empirical emissions distributions from 225 sovereign parties.
          </p>
        </div>

        <!-- Country Select Dropdown -->
        <div class="w-full sm:w-72">
          <select id="country-select" class="w-full bg-zinc-900 border border-zinc-700 text-white rounded-xl px-3.5 py-2.5 text-sm font-medium focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500 transition-colors cursor-pointer shadow-sm">
            <option value="" disabled>Loading nations...</option>
          </select>
        </div>
      </div>

      <!-- Quick Preset Nation Pills -->
      <div class="space-y-2">
        <span class="text-xs font-medium uppercase tracking-wider text-zinc-500">Quick Select:</span>
        <div class="flex flex-wrap gap-2" id="preset-pills-container">
          <button class="preset-pill px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 transition-colors" data-code="CHN">China</button>
          <button class="preset-pill px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 transition-colors" data-code="USA">United States</button>
          <button class="preset-pill px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 transition-colors" data-code="IND">India</button>
          <button class="preset-pill px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 transition-colors" data-code="DEU">Germany</button>
          <button class="preset-pill px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 transition-colors" data-code="BRA">Brazil</button>
          <button class="preset-pill px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 transition-colors" data-code="JPN">Japan</button>
          <button class="preset-pill px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 transition-colors" data-code="SGP">Singapore</button>
          <button class="preset-pill px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 transition-colors" data-code="ASM">American Samoa</button>
          <button class="preset-pill px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 transition-colors" data-code="MHL">Marshall Islands</button>
        </div>
      </div>

      <!-- Active Nation Profile Summary Banner -->
      <div class="bg-zinc-900/90 border border-zinc-800 rounded-xl p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div class="space-y-1">
          <span class="text-xs uppercase font-medium tracking-wider text-zinc-500">Inspecting Sovereign Party</span>
          <div class="flex items-baseline gap-2">
            <h3 class="text-xl sm:text-2xl font-bold font-display text-white" id="selected-nation-name">China</h3>
            <span class="text-xs font-mono text-zinc-400 px-2 py-0.5 rounded bg-zinc-800" id="selected-nation-code">CHN</span>
          </div>
          <p class="text-xs text-zinc-400">Total National Emissions: <span class="text-white font-semibold" id="selected-nation-emissions">15,112 Mt CO₂e / yr</span></p>
        </div>

        <div class="flex flex-col sm:items-end justify-center">
          <span class="text-xs uppercase font-medium tracking-wider text-zinc-500 mb-1">Empirical Baseline Profile</span>
          <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-lg bg-orange-500/10 border border-orange-500/30 text-orange-400 font-semibold text-sm shadow-sm" id="baseline-profile-badge">
            <span class="material-symbols-outlined text-[18px]" id="baseline-profile-icon">bolt</span>
            <span id="baseline-profile-text">Energy-Dominant & Industrialized Macro-Economy</span>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 2: Interactive Policy Simulator (Middle) -->
    <section class="bg-[#16161a] border border-zinc-800 rounded-2xl p-6 sm:p-8 shadow-xl space-y-6">
      
      <!-- Section Header & Model Selector -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-zinc-800/80 pb-5">
        <div>
          <h2 class="text-lg font-semibold font-display text-white flex items-center gap-2">
            <span class="material-symbols-outlined text-orange-400 text-[22px]">tune</span>
            <span>Simulate Transition Policy (Adjust Sector Contributions)</span>
          </h2>
          <p class="text-sm text-zinc-400 mt-1">
            Move any slider to model an emissions shift. The remaining sectors will automatically rebalance to total 100%.
          </p>
        </div>

        <!-- Mode Toggle & Reset Button -->
        <div class="flex items-center gap-2.5 flex-wrap">
          <div class="inline-flex rounded-lg bg-zinc-900 p-0.5 border border-zinc-800" id="model-mode-toggle">
            <button id="btn-mode-consensus" class="px-2.5 py-1.5 rounded-md text-xs font-semibold bg-zinc-800 text-orange-400 shadow-sm transition-colors">
              Validated Consensus (k=2)
            </button>
            <button id="btn-mode-detailed" class="px-2.5 py-1.5 rounded-md text-xs font-medium text-zinc-400 hover:text-white transition-colors">
              Detailed Taxonomy (k=4)
            </button>
          </div>

          <button id="reset-baseline-btn" class="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 hover:text-white text-xs font-medium border border-zinc-700 transition-colors shrink-0">
            <span class="material-symbols-outlined text-[16px]">restart_alt</span>
            <span>Reset to Baseline</span>
          </button>
        </div>
      </div>

      <!-- Active Classification Result Banner -->
      <div class="rounded-xl p-4 sm:p-5 border transition-all duration-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-orange-500/10 border-orange-500/30" id="predicted-archetype-card">
        <div class="flex items-center gap-3.5">
          <div class="w-12 h-12 rounded-xl bg-orange-500/20 border border-orange-500/40 flex items-center justify-center text-orange-400 shrink-0" id="predicted-icon-wrap">
            <span class="material-symbols-outlined text-[28px]" id="predicted-icon">bolt</span>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="text-xs uppercase font-medium tracking-wider text-orange-300 font-mono">Consensus Classification</span>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-zinc-800 text-zinc-300" id="predicted-model-tag">K-Means (k=2)</span>
            </div>
            <h3 class="text-lg sm:text-xl font-bold font-display text-white mt-0.5" id="predicted-archetype-text">
              Predicted Archetype: Energy-Dominant & Industrialized Macro-Economy
            </h3>
          </div>
        </div>

        <div class="flex items-center gap-2 sm:self-center">
          <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
            <span id="predicted-status-badge">100% Balanced Allocation</span>
          </span>
        </div>
      </div>

      <!-- 5 Sector Sliders -->
      <div class="space-y-5 pt-2">

        <!-- Sector 1: Energy -->
        <div class="bg-zinc-900/60 border border-zinc-800/80 rounded-xl p-4 space-y-2 hover:border-zinc-700 transition-colors">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2.5">
              <div class="w-3 h-3 rounded-full bg-orange-500"></div>
              <span class="font-medium text-sm text-white">Power Generation & Energy</span>
            </div>
            <div class="flex items-baseline gap-2">
              <span class="text-xs text-zinc-400" id="energy-mt">7,250 Mt</span>
              <span class="text-lg font-bold font-mono text-orange-400" id="energy-pct">48%</span>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <button class="step-btn w-7 h-7 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 flex items-center justify-center text-xs font-bold transition-colors" data-sector="energy" data-dir="-1">-</button>
            <input type="range" min="0" max="100" value="48" class="w-full accent-orange-500" id="slider-energy" data-sector="energy"/>
            <button class="step-btn w-7 h-7 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 flex items-center justify-center text-xs font-bold transition-colors" data-sector="energy" data-dir="1">+</button>
          </div>
        </div>

        <!-- Sector 2: Industry -->
        <div class="bg-zinc-900/60 border border-zinc-800/80 rounded-xl p-4 space-y-2 hover:border-zinc-700 transition-colors">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2.5">
              <div class="w-3 h-3 rounded-full bg-purple-500"></div>
              <span class="font-medium text-sm text-white">Manufacturing & Heavy Industry</span>
            </div>
            <div class="flex items-baseline gap-2">
              <span class="text-xs text-zinc-400" id="industry-mt">4,230 Mt</span>
              <span class="text-lg font-bold font-mono text-purple-400" id="industry-pct">28%</span>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <button class="step-btn w-7 h-7 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 flex items-center justify-center text-xs font-bold transition-colors" data-sector="industry" data-dir="-1">-</button>
            <input type="range" min="0" max="100" value="28" class="w-full accent-purple-500" id="slider-industry" data-sector="industry"/>
            <button class="step-btn w-7 h-7 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 flex items-center justify-center text-xs font-bold transition-colors" data-sector="industry" data-dir="1">+</button>
          </div>
        </div>

        <!-- Sector 3: Transport -->
        <div class="bg-zinc-900/60 border border-zinc-800/80 rounded-xl p-4 space-y-2 hover:border-zinc-700 transition-colors">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2.5">
              <div class="w-3 h-3 rounded-full bg-cyan-500"></div>
              <span class="font-medium text-sm text-white">Domestic & International Transport</span>
            </div>
            <div class="flex items-baseline gap-2">
              <span class="text-xs text-zinc-400" id="transport-mt">1,210 Mt</span>
              <span class="text-lg font-bold font-mono text-cyan-400" id="transport-pct">8%</span>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <button class="step-btn w-7 h-7 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 flex items-center justify-center text-xs font-bold transition-colors" data-sector="transport" data-dir="-1">-</button>
            <input type="range" min="0" max="100" value="8" class="w-full accent-cyan-500" id="slider-transport" data-sector="transport"/>
            <button class="step-btn w-7 h-7 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 flex items-center justify-center text-xs font-bold transition-colors" data-sector="transport" data-dir="1">+</button>
          </div>
        </div>

        <!-- Sector 4: Agriculture -->
        <div class="bg-zinc-900/60 border border-zinc-800/80 rounded-xl p-4 space-y-2 hover:border-zinc-700 transition-colors">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2.5">
              <div class="w-3 h-3 rounded-full bg-emerald-500"></div>
              <span class="font-medium text-sm text-white">Agriculture, Soil & Land Management</span>
            </div>
            <div class="flex items-baseline gap-2">
              <span class="text-xs text-zinc-400" id="agriculture-mt">1,660 Mt</span>
              <span class="text-lg font-bold font-mono text-emerald-400" id="agriculture-pct">11%</span>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <button class="step-btn w-7 h-7 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 flex items-center justify-center text-xs font-bold transition-colors" data-sector="agriculture" data-dir="-1">-</button>
            <input type="range" min="0" max="100" value="11" class="w-full accent-emerald-500" id="slider-agriculture" data-sector="agriculture"/>
            <button class="step-btn w-7 h-7 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 flex items-center justify-center text-xs font-bold transition-colors" data-sector="agriculture" data-dir="1">+</button>
          </div>
        </div>

        <!-- Sector 5: Buildings -->
        <div class="bg-zinc-900/60 border border-zinc-800/80 rounded-xl p-4 space-y-2 hover:border-zinc-700 transition-colors">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2.5">
              <div class="w-3 h-3 rounded-full bg-amber-500"></div>
              <span class="font-medium text-sm text-white">Residential & Commercial Buildings</span>
            </div>
            <div class="flex items-baseline gap-2">
              <span class="text-xs text-zinc-400" id="buildings-mt">760 Mt</span>
              <span class="text-lg font-bold font-mono text-amber-400" id="buildings-pct">5%</span>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <button class="step-btn w-7 h-7 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 flex items-center justify-center text-xs font-bold transition-colors" data-sector="buildings" data-dir="-1">-</button>
            <input type="range" min="0" max="100" value="5" class="w-full accent-amber-500" id="slider-buildings" data-sector="buildings"/>
            <button class="step-btn w-7 h-7 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 flex items-center justify-center text-xs font-bold transition-colors" data-sector="buildings" data-dir="1">+</button>
          </div>
        </div>

      </div>

      <!-- Sector Composition Proportion Visualizer Bar -->
      <div class="space-y-1.5 pt-1">
        <div class="flex justify-between text-xs text-zinc-400 font-medium">
          <span>Macro-Sector Allocation Balance</span>
          <span class="font-mono text-zinc-300">100% Simplex Normalized</span>
        </div>
        <div class="w-full h-3 rounded-full bg-zinc-800 overflow-hidden flex shadow-inner">
          <div id="bar-energy" class="bg-orange-500 h-full transition-all duration-150" style="width: 48%;"></div>
          <div id="bar-industry" class="bg-purple-500 h-full transition-all duration-150" style="width: 28%;"></div>
          <div id="bar-transport" class="bg-cyan-500 h-full transition-all duration-150" style="width: 8%;"></div>
          <div id="bar-agriculture" class="bg-emerald-500 h-full transition-all duration-150" style="width: 11%;"></div>
          <div id="bar-buildings" class="bg-amber-500 h-full transition-all duration-150" style="width: 5%;"></div>
        </div>
      </div>

      <!-- Policy Presets / Shortcuts -->
      <div class="space-y-2 pt-2 border-t border-zinc-800/80">
        <span class="text-xs uppercase font-medium tracking-wider text-zinc-500">Test Transition Scenarios:</span>
        <div class="flex flex-wrap gap-2">
          <button class="scenario-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800/80 hover:bg-zinc-700 text-zinc-300 border border-zinc-700 transition-colors" data-scenario="energy">
            ⚡ Baseload Heavy (65% Energy)
          </button>
          <button class="scenario-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800/80 hover:bg-zinc-700 text-zinc-300 border border-zinc-700 transition-colors" data-scenario="agrarian">
            🌾 Agrarian Priority (95% Agriculture)
          </button>
          <button class="scenario-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800/80 hover:bg-zinc-700 text-zinc-300 border border-zinc-700 transition-colors" data-scenario="industry">
            🏭 Concentrated Industry (100% Industry)
          </button>
          <button class="scenario-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800/80 hover:bg-zinc-700 text-zinc-300 border border-zinc-700 transition-colors" data-scenario="transit">
            ✈️ Transit Corridor (90% Transport)
          </button>
        </div>
      </div>
    </section>

    <!-- SECTION 3: Policy Insights & Equivalencies (Bottom, Side-by-Side Cards) -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      
      <!-- Card Left: Why This Classification? (Explainable AI) -->
      <section class="bg-[#16161a] border border-zinc-800 rounded-2xl p-6 sm:p-7 shadow-xl space-y-5 flex flex-col justify-between">
        <div class="space-y-4">
          <div class="border-b border-zinc-800/80 pb-4">
            <h2 class="text-base font-semibold font-display text-white flex items-center gap-2">
              <span class="material-symbols-outlined text-orange-400 text-[20px]">psychology</span>
              <span>Why This Classification?</span>
            </h2>
            <p class="text-xs text-zinc-400 mt-0.5">
              Explainable AI (XAI) transparent decision logic based on simplex geometry.
            </p>
          </div>

          <!-- Plain-English Rule -->
          <div class="bg-zinc-900/90 border border-zinc-800 rounded-xl p-4 space-y-1.5">
            <span class="text-xs uppercase font-medium tracking-wider text-zinc-500">Mathematical Boundary Rule</span>
            <p class="text-sm font-mono text-zinc-200 leading-relaxed" id="rule-plain-text">
              Consensus K-Means (k=2): CLR Distance to Energy-Dominant Centroid is Minimal.
            </p>
          </div>

          <!-- Structural Rationale -->
          <div class="bg-zinc-900/90 border border-zinc-800 rounded-xl p-4 space-y-1.5">
            <span class="text-xs uppercase font-medium tracking-wider text-zinc-500">Structural Economic Rationale</span>
            <p class="text-sm text-zinc-300 leading-relaxed" id="rule-rationale-text">
              Baseload fossil power and transportation demand constitute the structural core of national output.
            </p>
          </div>

          <!-- Strategic Policy Recommendation -->
          <div class="bg-orange-500/10 border border-orange-500/20 rounded-xl p-4 space-y-1.5">
            <span class="text-xs uppercase font-medium tracking-wider text-orange-400">Strategic Policy Guidance</span>
            <p class="text-sm text-orange-200 leading-relaxed" id="policy-recommendation-text">
              Accelerate baseload coal retirement with high-capacity renewable contracts, grid battery storage, and smart transmission corridors.
            </p>
          </div>
        </div>

        <div class="text-xs text-zinc-500 pt-2 border-t border-zinc-800/80 flex justify-between items-center">
          <span>Phase-I XAI Methodology</span>
          <span class="text-orange-400 font-medium font-mono">CLR Simplex Calibrated</span>
        </div>
      </section>

      <!-- Card Right: Physical Impact of Target Benchmark Reduction -->
      <section class="bg-[#16161a] border border-zinc-800 rounded-2xl p-6 sm:p-7 shadow-xl space-y-5 flex flex-col justify-between">
        <div class="space-y-5">
          <div class="border-b border-zinc-800/80 pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h2 class="text-base font-semibold font-display text-white flex items-center gap-2">
                <span class="material-symbols-outlined text-emerald-400 text-[20px]">energy_savings_leaf</span>
                <span>Physical Policy Impact</span>
              </h2>
              <p class="text-xs text-zinc-400 mt-0.5">
                Physical sector abatement required to achieve target reduction.
              </p>
            </div>

            <!-- Benchmark Target Selector -->
            <div class="inline-flex rounded-lg bg-zinc-900 p-0.5 border border-zinc-800 text-xs font-medium">
              <button class="target-pct-btn px-2.5 py-1 rounded bg-zinc-800 text-orange-400 font-semibold" data-pct="5">5% Cut</button>
              <button class="target-pct-btn px-2.5 py-1 rounded text-zinc-400 hover:text-white" data-pct="10">10% Cut</button>
              <button class="target-pct-btn px-2.5 py-1 rounded text-zinc-400 hover:text-white" data-pct="15">15% Cut</button>
            </div>
          </div>

          <!-- Hero Physical Impact Numbers -->
          <div class="grid grid-cols-2 gap-4">
            <div class="bg-zinc-900/90 border border-zinc-800 rounded-xl p-4">
              <span class="text-xs uppercase font-medium tracking-wider text-zinc-500 block mb-1">Total Carbon Abated</span>
              <div class="text-2xl sm:text-3xl font-bold font-mono text-emerald-400" id="hero-abatement-mt">
                756 Mt CO₂e
              </div>
              <span class="text-xs text-zinc-400 mt-1 block">National Annual Reduction</span>
            </div>

            <div class="bg-zinc-900/90 border border-zinc-800 rounded-xl p-4">
              <span class="text-xs uppercase font-medium tracking-wider text-zinc-500 block mb-1">Dominant Sector Activity Cut</span>
              <div class="text-2xl sm:text-3xl font-bold font-mono text-orange-400" id="dominant-sector-cut-pct">
                10.4% Cut
              </div>
              <span class="text-xs text-zinc-400 mt-1 block">Focused on Energy Sector</span>
            </div>
          </div>

          <!-- 3 Real-World Physical Equivalencies -->
          <div class="space-y-3 pt-1">
            <span class="text-xs uppercase font-medium tracking-wider text-zinc-500">Real-World Environmental Equivalency</span>

            <!-- Equiv 1: Coal Plants -->
            <div class="flex items-center gap-3.5 bg-zinc-900/60 border border-zinc-800/80 rounded-xl p-3.5">
              <div class="w-10 h-10 rounded-lg bg-orange-500/10 border border-orange-500/20 flex items-center justify-center text-orange-400 shrink-0">
                <span class="material-symbols-outlined text-[20px]">factory</span>
              </div>
              <div class="space-y-0.5">
                <span class="text-xs text-zinc-400">Equivalent Baseload Retirement:</span>
                <p class="text-sm font-semibold text-white font-mono" id="eq-coal-plants">194 Coal Power Plants Retired</p>
              </div>
            </div>

            <!-- Equiv 2: Passenger Flights -->
            <div class="flex items-center gap-3.5 bg-zinc-900/60 border border-zinc-800/80 rounded-xl p-3.5">
              <div class="w-10 h-10 rounded-lg bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400 shrink-0">
                <span class="material-symbols-outlined text-[20px]">flight_takeoff</span>
              </div>
              <div class="space-y-0.5">
                <span class="text-xs text-zinc-400">Avoided Commercial Transit:</span>
                <p class="text-sm font-semibold text-white font-mono" id="eq-flights">820 Million Passenger Flights Avoided</p>
              </div>
            </div>

            <!-- Equiv 3: Tree Sequestration -->
            <div class="flex items-center gap-3.5 bg-zinc-900/60 border border-zinc-800/80 rounded-xl p-3.5">
              <div class="w-10 h-10 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 shrink-0">
                <span class="material-symbols-outlined text-[20px]">forest</span>
              </div>
              <div class="space-y-0.5">
                <span class="text-xs text-zinc-400">Biological Carbon Sink Equivalent:</span>
                <p class="text-sm font-semibold text-white font-mono" id="eq-trees">34.4 Billion Tree-Years Grown</p>
              </div>
            </div>
          </div>
        </div>

        <div class="text-xs text-zinc-500 pt-2 border-t border-zinc-800/80 flex justify-between items-center">
          <span>Calibrated via EPA & IPCC GHG conversion standards</span>
          <span class="text-emerald-400 font-medium">Equivalence Verified</span>
        </div>
      </section>

    </div>

  </div>

  <!-- Real Interactive JavaScript Engine -->
  <script>
    (function initSimulator() {
      const API_BASE = 'http://localhost:5000';

      // Application State
      const state = {
        countryCode: 'CHN',
        countryName: 'China',
        totalEmissionsMt: 15112,
        baselineSectors: { energy: 48, industry: 28, transport: 8, agriculture: 11, buildings: 5 },
        sectors: { energy: 48, industry: 28, transport: 8, agriculture: 11, buildings: 5 },
        targetPct: 5.0,
        modelMode: 'consensus', /* 'consensus' (winning k=2) or 'detailed' (k=4) */
        winningModel: null,
        evaluationData: null,
        countries: [],
        emissions: [],
        rules: [],
        debounceTimer: null
      };

      // DOM Elements: Validation Section
      const consensusWinningAlgo = document.getElementById('consensus-winning-algo');
      const consensusOptimalK = document.getElementById('consensus-optimal-k');
      const consensusCompositeScore = document.getElementById('consensus-composite-score');
      const metricSil = document.getElementById('metric-sil');
      const metricDb = document.getElementById('metric-db');
      const metricCh = document.getElementById('metric-ch');
      const benchmarkTotalRuns = document.getElementById('benchmark-total-runs');
      const benchmarkTableBody = document.getElementById('benchmark-table-body');

      // DOM Elements: Simulator
      const countrySelect = document.getElementById('country-select');
      const selectedNationName = document.getElementById('selected-nation-name');
      const selectedNationCode = document.getElementById('selected-nation-code');
      const selectedNationEmissions = document.getElementById('selected-nation-emissions');
      const baselineProfileText = document.getElementById('baseline-profile-text');
      const baselineProfileIcon = document.getElementById('baseline-profile-icon');
      const predictedArchetypeText = document.getElementById('predicted-archetype-text');
      const predictedModelTag = document.getElementById('predicted-model-tag');
      const predictedIcon = document.getElementById('predicted-icon');
      const predictedIconWrap = document.getElementById('predicted-icon-wrap');
      const predictedCard = document.getElementById('predicted-archetype-card');
      const rulePlainText = document.getElementById('rule-plain-text');
      const ruleRationaleText = document.getElementById('rule-rationale-text');
      const policyRecommendationText = document.getElementById('policy-recommendation-text');

      const heroAbatementMt = document.getElementById('hero-abatement-mt');
      const dominantSectorCutPct = document.getElementById('dominant-sector-cut-pct');
      const eqCoalPlants = document.getElementById('eq-coal-plants');
      const eqFlights = document.getElementById('eq-flights');
      const eqTrees = document.getElementById('eq-trees');

      const btnModeConsensus = document.getElementById('btn-mode-consensus');
      const btnModeDetailed = document.getElementById('btn-mode-detailed');

      const sliders = {
        energy: document.getElementById('slider-energy'),
        industry: document.getElementById('slider-industry'),
        transport: document.getElementById('slider-transport'),
        agriculture: document.getElementById('slider-agriculture'),
        buildings: document.getElementById('slider-buildings')
      };

      const pctDisplays = {
        energy: document.getElementById('energy-pct'),
        industry: document.getElementById('industry-pct'),
        transport: document.getElementById('transport-pct'),
        agriculture: document.getElementById('agriculture-pct'),
        buildings: document.getElementById('buildings-pct')
      };

      const mtDisplays = {
        energy: document.getElementById('energy-mt'),
        industry: document.getElementById('industry-mt'),
        transport: document.getElementById('transport-mt'),
        agriculture: document.getElementById('agriculture-mt'),
        buildings: document.getElementById('buildings-mt')
      };

      const barDisplays = {
        energy: document.getElementById('bar-energy'),
        industry: document.getElementById('bar-industry'),
        transport: document.getElementById('bar-transport'),
        agriculture: document.getElementById('bar-agriculture'),
        buildings: document.getElementById('bar-buildings')
      };

      // 4-Archetype Detailed Taxonomy Design System
      const DETAILED_ARCHETYPES = {
        0: {
          title: "Energy-Dominant Economy",
          icon: "bolt",
          color: "orange",
          border: "border-orange-500/30",
          bg: "bg-orange-500/10",
          text: "text-orange-400",
          rule: "IF Energy > 2.1% AND Industry <= 75.0% -> Energy-Dominant Economy",
          rationale: "Power generation accounts for the largest share of national emissions. Transition policy achieves maximum leverage through rapid baseload power decarbonization.",
          recommendation: "Accelerate baseload coal retirement with high-capacity renewable contracts, grid battery storage, and smart transmission corridors."
        },
        1: {
          title: "Agriculture-Dominant Economy",
          icon: "grass",
          color: "emerald",
          border: "border-emerald-500/30",
          bg: "bg-emerald-500/10",
          text: "text-emerald-400",
          rule: "IF Agriculture > 75.0% (Energy <= 2.1%) -> Agriculture-Dominant Economy",
          rationale: "Livestock enteric fermentation, synthetic nitrogen fertilizer, and soil management represent over 90% of total national warming potential.",
          recommendation: "Deploy precision biochar, livestock feed additives to curb enteric methane, and scalable agroforestry incentives."
        },
        2: {
          title: "Industry-Dominant Micro-Economy",
          icon: "precision_manufacturing",
          color: "purple",
          border: "border-purple-500/30",
          bg: "bg-purple-500/10",
          text: "text-purple-400",
          rule: "IF Industry > 75.0% (Energy <= 2.1%) -> Industry-Dominant Micro-Economy",
          rationale: "Heavy industrial processing, chemical refining, and metals smelting constitute virtually all national emissions.",
          recommendation: "Subsidize green hydrogen for high-heat manufacturing and mandate point-source carbon capture and storage (CCUS)."
        },
        "-1": {
          title: "Specialized Transit Corridor",
          icon: "commute",
          color: "cyan",
          border: "border-cyan-500/30",
          bg: "bg-cyan-500/10",
          text: "text-cyan-400",
          rule: "IF Transport Intensity is Outlier (>40% to 90%) -> Specialized Transit Corridor",
          rationale: "High aviation, maritime bunkering, or specialized freight logistics corridors define this nation's primary emissions flux.",
          recommendation: "Mandate zero-emission fleet corridors, shore-to-ship clean power at maritime ports, and sustainable aviation fuel (SAF) mandates."
        }
      };

      // 1. Boot Application: Fetch /api/evaluate_models, /api/data, and /api/rules
      async function boot() {
        try {
          const [evalRes, dataRes, rulesRes] = await Promise.all([
            fetch(`${API_BASE}/api/evaluate_models`).then(r => r.json()),
            fetch(`${API_BASE}/api/data`).then(r => r.json()),
            fetch(`${API_BASE}/api/rules`).then(r => r.json())
          ]);

          state.evaluationData = evalRes;
          state.winningModel = evalRes.winning_model;
          state.countries = dataRes.clustered_proportions || [];
          state.emissions = dataRes.macro_sector_emissions || [];
          state.rules = rulesRes.xai_rules || [];

          // Render Objective 2 & 3 Validation Section
          renderEvaluationUI(evalRes);

          // Populate Country Dropdown and bind baseline
          populateCountrySelect();
          selectNation('CHN'); // Default: China
        } catch (err) {
          console.error('[Simulator Boot Error]', err);
        }
      }

      // Render Validation Section
      function renderEvaluationUI(evalRes) {
        if (!evalRes || !evalRes.winning_model) return;

        const win = evalRes.winning_model;

        // Scientific Consensus Card
        if (consensusWinningAlgo) {
          consensusWinningAlgo.innerHTML = `
            <span>${win.algorithm}</span>
            <span class="text-xs px-2 py-0.5 rounded bg-orange-500/20 text-orange-400 border border-orange-500/30 font-mono">Consensus Rank 1</span>
          `;
        }

        if (consensusOptimalK) {
          consensusOptimalK.innerHTML = `
            <span>${win.optimal_cluster_count} Archetypes</span>
            <span class="text-xs px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-mono">k = ${win.optimal_cluster_count}</span>
          `;
        }

        if (consensusCompositeScore) {
          consensusCompositeScore.textContent = win.composite_consensus_score.toFixed(4);
        }

        if (benchmarkTotalRuns) {
          benchmarkTotalRuns.textContent = `${evalRes.total_evaluations || 59} Runs Evaluated`;
        }

        // Tri-Index Scores
        if (metricSil) metricSil.textContent = win.silhouette_score.toFixed(4);
        if (metricDb) metricDb.textContent = win.davies_bouldin_score.toFixed(4);
        if (metricCh) metricCh.textContent = win.calinski_harabasz_score.toFixed(2);

        // Leaderboard Table
        if (benchmarkTableBody && evalRes.top_by_algorithm) {
          benchmarkTableBody.innerHTML = '';
          evalRes.top_by_algorithm.forEach(row => {
            const isWinner = row.algorithm === win.algorithm && row.k === win.optimal_cluster_count;
            const tr = document.createElement('tr');
            tr.className = `hover:bg-zinc-800/40 transition-colors ${isWinner ? 'bg-emerald-500/5' : ''}`;
            tr.innerHTML = `
              <td class="py-3 px-4 font-sans font-medium ${isWinner ? 'text-emerald-300 flex items-center gap-2' : 'text-zinc-200'}">
                ${isWinner ? '<span class="w-2 h-2 rounded-full bg-emerald-400"></span>' : ''}
                <span>${row.algorithm}</span>
              </td>
              <td class="py-3 px-4 text-zinc-300">${row.params || `k=${row.k}`}</td>
              <td class="py-3 px-4 text-right ${row.silhouette >= 0.7 ? 'text-emerald-400 font-semibold' : 'text-zinc-300'}">${row.silhouette.toFixed(4)}</td>
              <td class="py-3 px-4 text-right ${row.davies_bouldin <= 0.85 ? 'text-blue-400 font-semibold' : 'text-zinc-300'}">${row.davies_bouldin.toFixed(4)}</td>
              <td class="py-3 px-4 text-right ${row.calinski_harabasz >= 100 ? 'text-purple-400 font-semibold' : 'text-zinc-300'}">${row.calinski_harabasz.toFixed(2)}</td>
              <td class="py-3 px-4 text-right ${isWinner ? 'text-white font-bold' : 'text-zinc-300'}">${row.composite_score.toFixed(4)}</td>
              <td class="py-3 px-4 text-center">
                <span class="px-2 py-0.5 rounded ${isWinner ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-zinc-800 text-zinc-400'} text-[10px]">
                  ${isWinner ? 'Consensus Winner' : (row.composite_score > 0.9 ? 'Tied Consensus' : 'Evaluated')}
                </span>
              </td>
            `;
            benchmarkTableBody.appendChild(tr);
          });
        }
      }

      // Populate Country Selector Dropdown
      function populateCountrySelect() {
        if (!countrySelect) return;
        countrySelect.innerHTML = '';

        // Sort alphabetically by country name
        const sorted = [...state.countries].sort((a, b) => a.Name.localeCompare(b.Name));
        sorted.forEach(c => {
          const opt = document.createElement('option');
          opt.value = c.Country_code_A3;
          opt.textContent = `${c.Name} (${c.Country_code_A3})`;
          countrySelect.appendChild(opt);
        });

        countrySelect.value = state.countryCode;
        countrySelect.addEventListener('change', (e) => {
          selectNation(e.target.value);
        });
      }

      // Select Nation & Bind Real Data
      function selectNation(code) {
        const countryData = state.countries.find(c => c.Country_code_A3 === code);
        const emissionData = state.emissions.find(e => e.Country_code_A3 === code);
        if (!countryData) return;

        state.countryCode = code;
        state.countryName = countryData.Name;

        // Calculate total emissions in Mt
        if (emissionData) {
          const sectors = ['Energy', 'Industry', 'Transport', 'Agriculture', 'Buildings'];
          const totalGg = sectors.reduce((sum, s) => sum + (emissionData[s] || 0), 0);
          state.totalEmissionsMt = Math.max(1, Math.round(totalGg / 1000));
        }

        // Convert decimal proportions to integer % summing to 100
        const sectors = ['Energy', 'Industry', 'Transport', 'Agriculture', 'Buildings'];
        let rawPcts = sectors.map(s => Math.round((countryData[s] || 0) * 100));
        let sum = rawPcts.reduce((a, b) => a + b, 0);
        if (sum !== 100) {
          rawPcts[0] += (100 - sum); // Adjust residual on Energy
        }

        const baseline = {
          energy: Math.max(0, rawPcts[0]),
          industry: Math.max(0, rawPcts[1]),
          transport: Math.max(0, rawPcts[2]),
          agriculture: Math.max(0, rawPcts[3]),
          buildings: Math.max(0, rawPcts[4])
        };

        state.baselineSectors = { ...baseline };
        state.sectors = { ...baseline };

        // Update Section 1 DOM
        if (selectedNationName) selectedNationName.textContent = state.countryName;
        if (selectedNationCode) selectedNationCode.textContent = state.countryCode;
        if (selectedNationEmissions) selectedNationEmissions.textContent = `${state.totalEmissionsMt.toLocaleString()} Mt CO₂e / yr`;
        if (countrySelect) countrySelect.value = state.countryCode;

        // Highlight preset pill if matching
        document.querySelectorAll('.preset-pill').forEach(pill => {
          if (pill.dataset.code === code) {
            pill.className = 'preset-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-orange-500/20 text-orange-400 border border-orange-500/40 transition-colors';
          } else {
            pill.className = 'preset-pill px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 transition-colors';
          }
        });

        // Determine baseline profile
        const maxSector = Object.keys(baseline).reduce((a, b) => baseline[a] >= baseline[b] ? a : b);
        let profileName = "Energy-Dominant & Industrialized Macro-Economy";
        let profileIcon = "bolt";

        if (maxSector === 'agriculture') {
          profileName = "Agrarian & Non-Grid Micro-Economy";
          profileIcon = "grass";
        } else if (maxSector === 'industry') {
          profileName = "Industry-Dominant Micro-Economy";
          profileIcon = "precision_manufacturing";
        } else if (maxSector === 'transport') {
          profileName = "Specialized Transit Corridor";
          profileIcon = "commute";
        }

        if (baselineProfileText) baselineProfileText.textContent = profileName;
        if (baselineProfileIcon) baselineProfileIcon.textContent = profileIcon;

        // Render sliders and trigger inference
        renderSliders();
        triggerInference();
      }

      // Mathematical Slider Auto-Rebalancing Logic (Proportional Distribution)
      function rebalance(activeSector, newValue) {
        const targetVal = Math.min(100, Math.max(0, Math.round(newValue)));
        const otherSectors = Object.keys(state.sectors).filter(s => s !== activeSector);
        const currentOtherSum = otherSectors.reduce((sum, s) => sum + state.sectors[s], 0);
        const neededOtherSum = 100 - targetVal;

        state.sectors[activeSector] = targetVal;

        if (currentOtherSum === 0) {
          // If all other sectors are 0, distribute remainder equally
          const share = Math.floor(neededOtherSum / otherSectors.length);
          let remainder = neededOtherSum % otherSectors.length;
          otherSectors.forEach((s, idx) => {
            state.sectors[s] = share + (idx < remainder ? 1 : 0);
          });
        } else {
          // Proportional scaling
          let runningSum = 0;
          const scaled = {};
          otherSectors.forEach(s => {
            const proportional = (state.sectors[s] / currentOtherSum) * neededOtherSum;
            scaled[s] = Math.max(0, Math.round(proportional));
            runningSum += scaled[s];
          });

          // Adjust rounding drift on the largest other sector
          const drift = neededOtherSum - runningSum;
          if (drift !== 0) {
            const largestOther = otherSectors.reduce((a, b) => scaled[a] >= scaled[b] ? a : b);
            scaled[largestOther] = Math.max(0, scaled[largestOther] + drift);
          }

          otherSectors.forEach(s => {
            state.sectors[s] = scaled[s];
          });
        }

        renderSliders();
        debouncedInference();
      }

      // Debounce Backend API calls
      function debouncedInference() {
        if (state.debounceTimer) clearTimeout(state.debounceTimer);
        state.debounceTimer = setTimeout(() => {
          triggerInference();
        }, 120);
      }

      // Render Sliders, Percentages, and Mt to DOM
      function renderSliders() {
        Object.keys(state.sectors).forEach(sec => {
          const val = state.sectors[sec];
          if (sliders[sec]) sliders[sec].value = val;
          if (pctDisplays[sec]) pctDisplays[sec].textContent = `${val}%`;
          if (barDisplays[sec]) barDisplays[sec].style.width = `${val}%`;

          // Mt calculation
          const secMt = Math.round((val / 100) * state.totalEmissionsMt);
          if (mtDisplays[sec]) mtDisplays[sec].textContent = `${secMt.toLocaleString()} Mt`;
        });
      }

      // Trigger Backend Inference (/api/nearest_archetype and /api/calculate_equivalence)
      async function triggerInference() {
        try {
          const payload = {
            sectors: state.sectors,
            country: state.countryCode,
            baselineMt: state.totalEmissionsMt,
            benchmark_reduction_pct: state.targetPct,
            mode: state.modelMode
          };

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

          // Update Section 2 & 3 DOM from live API response
          updatePredictionUI(archRes);
          updateEquivalenceUI(equivRes);
        } catch (err) {
          console.error('[Inference Error]', err);
        }
      }

      // Update Section 2 (Predicted Archetype) & Section 3 Left Card
      function updatePredictionUI(archRes) {
        if (!archRes || archRes.error) return;

        const clusterId = archRes.nearest_cluster_id;
        const mode = archRes.mode || state.modelMode;

        let archetypeTitle = archRes.nearest_archetype;
        let iconName = "bolt";
        let bgStyle = "bg-orange-500/10";
        let borderStyle = "border-orange-500/30";
        let textStyle = "text-orange-400";
        let ruleText = "Consensus Distance Minimal";
        let rationaleText = "National profile classified via CLR Euclidean distance projection.";
        let recommendationText = "Pursue sectoral mitigation targeting high-intensity emissions sources.";

        if (mode === 'consensus') {
          // Consensus Mode (Objective 2 & 3 Winning Configuration)
          if (predictedModelTag) {
            predictedModelTag.textContent = `${archRes.winning_model || 'K-Means'} (Consensus k=${archRes.optimal_cluster_count || 2})`;
          }
          if (archRes.archetype) {
            archetypeTitle = archRes.archetype.title;
            iconName = archRes.archetype.icon || (clusterId === 0 ? "bolt" : "grass");
            ruleText = archRes.archetype.ruleIf;
            rationaleText = archRes.archetype.ruleRationale;
            recommendationText = archRes.archetype.recommendation;
            
            if (clusterId === 1) {
              bgStyle = "bg-emerald-500/10";
              borderStyle = "border-emerald-500/30";
              textStyle = "text-emerald-400";
            } else {
              bgStyle = "bg-orange-500/10";
              borderStyle = "border-orange-500/30";
              textStyle = "text-orange-400";
            }
          }
        } else {
          // Detailed Taxonomy Mode (k=4)
          if (predictedModelTag) {
            predictedModelTag.textContent = "Decision Tree (k=4 Taxonomy)";
          }
          const config = DETAILED_ARCHETYPES[clusterId] || DETAILED_ARCHETYPES[0];
          archetypeTitle = config.title;
          iconName = config.icon;
          bgStyle = config.bg;
          borderStyle = config.border;
          textStyle = config.text;
          ruleText = config.rule;
          rationaleText = config.rationale;
          recommendationText = config.recommendation;
        }

        // Section 2 Banner
        if (predictedArchetypeText) {
          predictedArchetypeText.textContent = `Predicted Archetype: ${archetypeTitle}`;
        }
        if (predictedIcon) {
          predictedIcon.textContent = iconName;
        }

        // Dynamic theme styling on predicted banner
        if (predictedCard && predictedIconWrap) {
          predictedCard.className = `rounded-xl p-4 sm:p-5 border transition-all duration-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${bgStyle} ${borderStyle}`;
          predictedIconWrap.className = `w-12 h-12 rounded-xl flex items-center justify-center shrink-0 ${bgStyle} ${borderStyle} ${textStyle}`;
        }

        // Section 3 Left Card ("Why This Classification?")
        if (rulePlainText) {
          rulePlainText.textContent = ruleText;
        }
        if (ruleRationaleText) {
          ruleRationaleText.textContent = rationaleText;
        }
        if (policyRecommendationText) {
          policyRecommendationText.textContent = recommendationText;
        }
      }

      // Update Section 3 Right Card ("Physical Impact")
      function updateEquivalenceUI(equivRes) {
        const item = (equivRes && equivRes.results && equivRes.results.length > 0) ? equivRes.results[0] : null;

        // Target reduction in Mt
        const deltaMt = Math.round(state.totalEmissionsMt * (state.targetPct / 100.0));
        if (heroAbatementMt) heroAbatementMt.textContent = `${deltaMt.toLocaleString()} Mt CO₂e`;

        // Dominant sector cut %
        let cutPct = 0;
        if (item && item.sector_activity_cut_pct) {
          cutPct = item.sector_activity_cut_pct;
        } else {
          const maxSector = Object.keys(state.sectors).reduce((a, b) => state.sectors[a] >= state.sectors[b] ? a : b);
          const dominantShare = state.sectors[maxSector] / 100.0;
          cutPct = dominantShare > 0 ? (state.targetPct / dominantShare) : state.targetPct;
        }

        if (dominantSectorCutPct) dominantSectorCutPct.textContent = `${cutPct.toFixed(1)}% Cut`;

        // 1. Equivalent Coal Plants Retired: 1 plant (500MW) = 3.89 Mt CO2/yr
        const coalPlants = Math.round(deltaMt / 3.89);
        if (eqCoalPlants) eqCoalPlants.textContent = `${coalPlants.toLocaleString()} Coal Power Plants`;

        // 2. Equivalent Passenger Flights: 1 Mt CO2 = ~1.085 million transatlantic passenger flights
        const flightsMillion = Math.round(deltaMt * 1.085);
        if (eqFlights) eqFlights.textContent = `${flightsMillion.toLocaleString()} Million Passenger Flights`;

        // 3. Forest Sequestration: 1 Mt CO2 = 45.45 million tree seedlings grown for 10 years (EPA standard)
        const treesBillion = ((deltaMt * 45.45) / 1000.0).toFixed(1);
        if (eqTrees) eqTrees.textContent = `${treesBillion} Billion Tree-Years`;
      }

      // Event Listeners: Sliders & Step Buttons
      Object.keys(sliders).forEach(sec => {
        const slider = sliders[sec];
        if (slider) {
          slider.addEventListener('input', (e) => {
            rebalance(sec, parseFloat(e.target.value));
          });
        }
      });

      document.querySelectorAll('.step-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          const sec = btn.dataset.sector;
          const dir = parseInt(btn.dataset.dir, 10);
          rebalance(sec, state.sectors[sec] + dir);
        });
      });

      // Quick Preset Pills Click
      document.querySelectorAll('.preset-pill').forEach(btn => {
        btn.addEventListener('click', () => {
          selectNation(btn.dataset.code);
        });
      });

      // Reset Button
      const resetBtn = document.getElementById('reset-baseline-btn');
      if (resetBtn) {
        resetBtn.addEventListener('click', () => {
          state.sectors = { ...state.baselineSectors };
          renderSliders();
          triggerInference();
        });
      }

      // Mode Switcher Buttons (Consensus k=2 vs Detailed k=4)
      if (btnModeConsensus && btnModeDetailed) {
        btnModeConsensus.addEventListener('click', () => {
          state.modelMode = 'consensus';
          btnModeConsensus.className = 'px-2.5 py-1.5 rounded-md text-xs font-semibold bg-zinc-800 text-orange-400 shadow-sm transition-colors';
          btnModeDetailed.className = 'px-2.5 py-1.5 rounded-md text-xs font-medium text-zinc-400 hover:text-white transition-colors';
          triggerInference();
        });

        btnModeDetailed.addEventListener('click', () => {
          state.modelMode = 'detailed';
          btnModeDetailed.className = 'px-2.5 py-1.5 rounded-md text-xs font-semibold bg-zinc-800 text-orange-400 shadow-sm transition-colors';
          btnModeConsensus.className = 'px-2.5 py-1.5 rounded-md text-xs font-medium text-zinc-400 hover:text-white transition-colors';
          triggerInference();
        });
      }

      // Policy Scenario Shortcuts
      const SCENARIOS = {
        energy:   { energy: 65, industry: 15, transport: 10, agriculture: 5, buildings: 5 },
        agrarian: { energy: 0, industry: 5, transport: 0, agriculture: 95, buildings: 0 },
        industry: { energy: 0, industry: 100, transport: 0, agriculture: 0, buildings: 0 },
        transit:  { energy: 5, industry: 3, transport: 90, agriculture: 0, buildings: 2 }
      };

      document.querySelectorAll('.scenario-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          const sc = SCENARIOS[btn.dataset.scenario];
          if (sc) {
            state.sectors = { ...sc };
            renderSliders();
            triggerInference();
          }
        });
      });

      // Target Reduction Selector Buttons (5%, 10%, 15%)
      document.querySelectorAll('.target-pct-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          document.querySelectorAll('.target-pct-btn').forEach(b => {
            b.className = 'target-pct-btn px-2.5 py-1 rounded text-zinc-400 hover:text-white';
          });
          btn.className = 'target-pct-btn px-2.5 py-1 rounded bg-zinc-800 text-orange-400 font-semibold';
          state.targetPct = parseFloat(btn.dataset.pct);
          triggerInference();
        });
      });

      // Initialize
      boot();
    })();
  </script>
</body>
</html>
'''

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(HTML_CONTENT)

print("[✓] Successfully written frontend/index.html with Section 0 and consensus dynamic adaptation.")
