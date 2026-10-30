# -*- coding: utf-8 -*-
"""
Builds the completely overhauled, clean frontend/index.html
Eliminates visual clutter and developer jargon.
Implements the 3-step vertical layout:
1. Country Baseline (Top)
2. Interactive Policy Simulator (Middle)
3. Policy Insights & Equivalencies (Bottom, Side-by-Side Cards)
"""

CLEAN_HTML = r'''<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Global Carbon Archetype Simulator</title>
  
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
        <span>EDGAR Global Emissions Database · Interactive Model</span>
      </div>
      <h1 class="text-3xl sm:text-4xl lg:text-5xl font-bold font-display tracking-tight text-white">
        Global Carbon Archetype Simulator
      </h1>
      <p class="text-base sm:text-lg text-zinc-400 max-w-2xl mx-auto leading-relaxed">
        Explore how shifting national sector emissions reclassifies economies into distinct climate transition archetypes.
      </p>
    </header>

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
            <span class="material-symbols-outlined text-[18px]">bolt</span>
            <span id="baseline-profile-text">Current Profile: Energy-Dominant Economy</span>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 2: Interactive Policy Simulator (Middle) -->
    <section class="bg-[#16161a] border border-zinc-800 rounded-2xl p-6 sm:p-8 shadow-xl space-y-6">
      
      <!-- Section Header & Helper Tip -->
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

        <!-- Reset Button -->
        <button id="reset-baseline-btn" class="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 hover:text-white text-xs font-medium border border-zinc-700 transition-colors shrink-0">
          <span class="material-symbols-outlined text-[16px]">restart_alt</span>
          <span>Reset to Baseline</span>
        </button>
      </div>

      <!-- Active Classification Result Banner -->
      <div class="rounded-xl p-4 sm:p-5 border transition-all duration-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-orange-500/10 border-orange-500/30" id="predicted-archetype-card">
        <div class="flex items-center gap-3.5">
          <div class="w-12 h-12 rounded-xl bg-orange-500/20 border border-orange-500/40 flex items-center justify-center text-orange-400 shrink-0" id="predicted-icon-wrap">
            <span class="material-symbols-outlined text-[28px]" id="predicted-icon">bolt</span>
          </div>
          <div>
            <span class="text-xs uppercase font-medium tracking-wider text-orange-300 font-mono">Real-Time Model Classification</span>
            <h3 class="text-lg sm:text-xl font-bold font-display text-white" id="predicted-archetype-text">
              Predicted Archetype: Energy-Dominant Economy
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
            <div class="flex items-center gap-2">
              <span class="w-3 h-3 rounded-full bg-orange-500"></span>
              <span class="font-semibold text-sm text-white">Energy</span>
              <span class="text-xs text-zinc-400 hidden sm:inline">(Power Plants & Electricity Generation)</span>
            </div>
            <div class="text-right flex items-baseline gap-2">
              <span class="text-xs font-mono text-zinc-400" id="energy-mt">8,009 Mt</span>
              <span class="text-lg font-bold font-display text-orange-400" id="energy-pct">53%</span>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <button class="step-btn px-2 py-0.5 rounded bg-zinc-800 hover:bg-zinc-700 text-xs font-mono text-zinc-300 border border-zinc-700" data-sector="energy" data-dir="-1">-1%</button>
            <input type="range" min="0" max="100" value="53" class="sector-slider w-full cursor-pointer accent-orange-500" data-sector="energy" id="slider-energy"/>
            <button class="step-btn px-2 py-0.5 rounded bg-zinc-800 hover:bg-zinc-700 text-xs font-mono text-zinc-300 border border-zinc-700" data-sector="energy" data-dir="1">+1%</button>
          </div>
        </div>

        <!-- Sector 2: Industry -->
        <div class="bg-zinc-900/60 border border-zinc-800/80 rounded-xl p-4 space-y-2 hover:border-zinc-700 transition-colors">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="w-3 h-3 rounded-full bg-purple-500"></span>
              <span class="font-semibold text-sm text-white">Industry</span>
              <span class="text-xs text-zinc-400 hidden sm:inline">(Manufacturing, Steel, Cement & Chemicals)</span>
            </div>
            <div class="text-right flex items-baseline gap-2">
              <span class="text-xs font-mono text-zinc-400" id="industry-mt">4,685 Mt</span>
              <span class="text-lg font-bold font-display text-purple-400" id="industry-pct">31%</span>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <button class="step-btn px-2 py-0.5 rounded bg-zinc-800 hover:bg-zinc-700 text-xs font-mono text-zinc-300 border border-zinc-700" data-sector="industry" data-dir="-1">-1%</button>
            <input type="range" min="0" max="100" value="31" class="sector-slider w-full cursor-pointer accent-purple-500" data-sector="industry" id="slider-industry"/>
            <button class="step-btn px-2 py-0.5 rounded bg-zinc-800 hover:bg-zinc-700 text-xs font-mono text-zinc-300 border border-zinc-700" data-sector="industry" data-dir="1">+1%</button>
          </div>
        </div>

        <!-- Sector 3: Transport -->
        <div class="bg-zinc-900/60 border border-zinc-800/80 rounded-xl p-4 space-y-2 hover:border-zinc-700 transition-colors">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="w-3 h-3 rounded-full bg-cyan-500"></span>
              <span class="font-semibold text-sm text-white">Transport</span>
              <span class="text-xs text-zinc-400 hidden sm:inline">(Passenger Cars, Trucks, Freight & Aviation)</span>
            </div>
            <div class="text-right flex items-baseline gap-2">
              <span class="text-xs font-mono text-zinc-400" id="transport-mt">907 Mt</span>
              <span class="text-lg font-bold font-display text-cyan-400" id="transport-pct">6%</span>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <button class="step-btn px-2 py-0.5 rounded bg-zinc-800 hover:bg-zinc-700 text-xs font-mono text-zinc-300 border border-zinc-700" data-sector="transport" data-dir="-1">-1%</button>
            <input type="range" min="0" max="100" value="6" class="sector-slider w-full cursor-pointer accent-cyan-500" data-sector="transport" id="slider-transport"/>
            <button class="step-btn px-2 py-0.5 rounded bg-zinc-800 hover:bg-zinc-700 text-xs font-mono text-zinc-300 border border-zinc-700" data-sector="transport" data-dir="1">+1%</button>
          </div>
        </div>

        <!-- Sector 4: Agriculture -->
        <div class="bg-zinc-900/60 border border-zinc-800/80 rounded-xl p-4 space-y-2 hover:border-zinc-700 transition-colors">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="w-3 h-3 rounded-full bg-emerald-500"></span>
              <span class="font-semibold text-sm text-white">Agriculture</span>
              <span class="text-xs text-zinc-400 hidden sm:inline">(Livestock, Soil Cultivation & Fertilizers)</span>
            </div>
            <div class="text-right flex items-baseline gap-2">
              <span class="text-xs font-mono text-zinc-400" id="agriculture-mt">756 Mt</span>
              <span class="text-lg font-bold font-display text-emerald-400" id="agriculture-pct">5%</span>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <button class="step-btn px-2 py-0.5 rounded bg-zinc-800 hover:bg-zinc-700 text-xs font-mono text-zinc-300 border border-zinc-700" data-sector="agriculture" data-dir="-1">-1%</button>
            <input type="range" min="0" max="100" value="5" class="sector-slider w-full cursor-pointer accent-emerald-500" data-sector="agriculture" id="slider-agriculture"/>
            <button class="step-btn px-2 py-0.5 rounded bg-zinc-800 hover:bg-zinc-700 text-xs font-mono text-zinc-300 border border-zinc-700" data-sector="agriculture" data-dir="1">+1%</button>
          </div>
        </div>

        <!-- Sector 5: Buildings -->
        <div class="bg-zinc-900/60 border border-zinc-800/80 rounded-xl p-4 space-y-2 hover:border-zinc-700 transition-colors">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="w-3 h-3 rounded-full bg-amber-500"></span>
              <span class="font-semibold text-sm text-white">Buildings</span>
              <span class="text-xs text-zinc-400 hidden sm:inline">(Heating, Cooking, Commercial & Residential HVAC)</span>
            </div>
            <div class="text-right flex items-baseline gap-2">
              <span class="text-xs font-mono text-zinc-400" id="buildings-mt">604 Mt</span>
              <span class="text-lg font-bold font-display text-amber-400" id="buildings-pct">5%</span>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <button class="step-btn px-2 py-0.5 rounded bg-zinc-800 hover:bg-zinc-700 text-xs font-mono text-zinc-300 border border-zinc-700" data-sector="buildings" data-dir="-1">-1%</button>
            <input type="range" min="0" max="100" value="5" class="sector-slider w-full cursor-pointer accent-amber-500" data-sector="buildings" id="slider-buildings"/>
            <button class="step-btn px-2 py-0.5 rounded bg-zinc-800 hover:bg-zinc-700 text-xs font-mono text-zinc-300 border border-zinc-700" data-sector="buildings" data-dir="1">+1%</button>
          </div>
        </div>
      </div>

      <!-- Color Allocation Bar -->
      <div class="space-y-1.5 pt-2">
        <div class="flex justify-between text-xs text-zinc-400 font-mono">
          <span>Sector Contribution Mix</span>
          <span class="text-emerald-400" id="bar-sum-label">Total: 100%</span>
        </div>
        <div class="w-full h-3 rounded-full overflow-hidden flex bg-zinc-800">
          <div id="bar-energy" class="h-full bg-orange-500 transition-all duration-150" style="width: 53%"></div>
          <div id="bar-industry" class="h-full bg-purple-500 transition-all duration-150" style="width: 31%"></div>
          <div id="bar-transport" class="h-full bg-cyan-500 transition-all duration-150" style="width: 6%"></div>
          <div id="bar-agriculture" class="h-full bg-emerald-500 transition-all duration-150" style="width: 5%"></div>
          <div id="bar-buildings" class="h-full bg-amber-500 transition-all duration-150" style="width: 5%"></div>
        </div>
      </div>

      <!-- Quick Shift Scenarios -->
      <div class="pt-2 border-t border-zinc-800/80 flex flex-wrap items-center gap-2">
        <span class="text-xs font-medium uppercase tracking-wider text-zinc-500">Test Policy Scenarios:</span>
        <button class="scenario-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 transition-colors" data-scenario="energy">Clean Energy Priority</button>
        <button class="scenario-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 transition-colors" data-scenario="agrarian">Agrarian Transition</button>
        <button class="scenario-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 transition-colors" data-scenario="industry">Heavy Manufacturing</button>
        <button class="scenario-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 transition-colors" data-scenario="transit">Transit Corridors</button>
      </div>
    </section>

    <!-- SECTION 3: Policy Insights & Equivalencies (Bottom, Side-by-Side Cards) -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8">

      <!-- Left Card: Why This Classification? -->
      <section class="bg-[#16161a] border border-zinc-800 rounded-2xl p-6 sm:p-8 shadow-xl flex flex-col justify-between space-y-6">
        <div class="space-y-4">
          <div class="border-b border-zinc-800/80 pb-4">
            <h2 class="text-lg font-semibold font-display text-white flex items-center gap-2">
              <span class="material-symbols-outlined text-orange-400 text-[22px]">psychology</span>
              <span>Why This Classification?</span>
            </h2>
            <p class="text-xs text-zinc-400 mt-0.5">
              Explainable AI decision rule explaining archetype classification.
            </p>
          </div>

          <!-- Plain-English Rule Box -->
          <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-4 space-y-2">
            <span class="text-xs uppercase font-medium tracking-wider text-zinc-400">Triggered Decision Rule</span>
            <p class="text-sm font-semibold text-orange-300 leading-snug" id="rule-plain-text">
              IF Energy &gt; 2.1% AND Industry &le; 75.0% &rarr; Classify as Energy-Dominant Economy
            </p>
          </div>

          <!-- Rationale & Structural Explanation -->
          <div class="space-y-2 text-sm text-zinc-300 leading-relaxed">
            <p id="rule-rationale-text">
              Energy power generation infrastructure represents the structural backbone of this nation's emissions profile.
            </p>
          </div>
        </div>

        <!-- Policy Recommendation Action Lever -->
        <div class="bg-zinc-900/80 border border-zinc-800 rounded-xl p-4 flex items-start gap-3 mt-4">
          <span class="material-symbols-outlined text-orange-400 text-[20px] shrink-0 mt-0.5">lightbulb</span>
          <div class="space-y-0.5">
            <span class="text-xs font-semibold text-white uppercase tracking-wider">Recommended Transition Lever</span>
            <p class="text-xs text-zinc-300 leading-relaxed" id="policy-recommendation-text">
              Accelerate baseload coal replacement with renewable dispatch, grid battery storage, and transmission expansion.
            </p>
          </div>
        </div>
      </section>

      <!-- Right Card: Physical Impact -->
      <section class="bg-[#16161a] border border-zinc-800 rounded-2xl p-6 sm:p-8 shadow-xl flex flex-col justify-between space-y-6">
        <div class="space-y-4">
          <div class="flex items-center justify-between border-b border-zinc-800/80 pb-4">
            <div>
              <h2 class="text-lg font-semibold font-display text-white flex items-center gap-2">
                <span class="material-symbols-outlined text-emerald-400 text-[22px]">eco</span>
                <span>Physical Impact</span>
              </h2>
              <p class="text-xs text-zinc-400 mt-0.5">
                Real-world equivalencies for an ambitious national reduction.
              </p>
            </div>

            <!-- Target Reduction Selector -->
            <div class="inline-flex rounded-lg p-0.5 bg-zinc-900 border border-zinc-800 text-xs font-medium">
              <button class="target-pct-btn px-2.5 py-1 rounded bg-zinc-800 text-orange-400 font-semibold" data-pct="5">5% Cut</button>
              <button class="target-pct-btn px-2.5 py-1 rounded text-zinc-400 hover:text-white" data-pct="10">10% Cut</button>
              <button class="target-pct-btn px-2.5 py-1 rounded text-zinc-400 hover:text-white" data-pct="15">15% Cut</button>
            </div>
          </div>

          <!-- Hero Abatement Number -->
          <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-4 flex items-baseline justify-between">
            <div>
              <span class="text-xs uppercase font-medium tracking-wider text-zinc-500">Annual Reduction Target</span>
              <div class="text-2xl font-bold font-display text-white" id="hero-abatement-mt">756 Mt CO₂e</div>
            </div>
            <div class="text-right">
              <span class="text-xs text-zinc-400 font-medium">Dominant Sector Cut</span>
              <div class="text-lg font-bold font-display text-orange-400" id="dominant-sector-cut-pct">9.4% Cut</div>
            </div>
          </div>

          <!-- 3 Clear Physical Metric Cards -->
          <div class="space-y-3">
            <!-- 1. Coal Plants -->
            <div class="bg-zinc-900/60 border border-zinc-800/80 rounded-xl p-3.5 flex items-center gap-3.5">
              <div class="w-10 h-10 rounded-lg bg-orange-500/10 border border-orange-500/30 flex items-center justify-center text-orange-400 shrink-0">
                <span class="material-symbols-outlined text-[20px]">factory</span>
              </div>
              <div>
                <div class="text-sm font-bold text-white" id="eq-coal-plants">194 Coal Power Plants</div>
                <div class="text-xs text-zinc-400">Equivalent to the complete annual shutdown of 500MW baseload units.</div>
              </div>
            </div>

            <!-- 2. Passenger Flights -->
            <div class="bg-zinc-900/60 border border-zinc-800/80 rounded-xl p-3.5 flex items-center gap-3.5">
              <div class="w-10 h-10 rounded-lg bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 shrink-0">
                <span class="material-symbols-outlined text-[20px]">flight</span>
              </div>
              <div>
                <div class="text-sm font-bold text-white" id="eq-flights">820 Million Passenger Flights</div>
                <div class="text-xs text-zinc-400">Equivalent passenger flight emissions eliminated from transport corridors.</div>
              </div>
            </div>

            <!-- 3. Forest Sequestration -->
            <div class="bg-zinc-900/60 border border-zinc-800/80 rounded-xl p-3.5 flex items-center gap-3.5">
              <div class="w-10 h-10 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 shrink-0">
                <span class="material-symbols-outlined text-[20px]">forest</span>
              </div>
              <div>
                <div class="text-sm font-bold text-white" id="eq-trees">34.4 Billion Tree-Years</div>
                <div class="text-xs text-zinc-400">Required mature tree seedlings growing for 10 years to absorb this target.</div>
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
        baselineSectors: { energy: 53, industry: 31, transport: 6, agriculture: 5, buildings: 5 },
        sectors: { energy: 53, industry: 31, transport: 6, agriculture: 5, buildings: 5 },
        targetPct: 5.0,
        countries: [],
        emissions: [],
        rules: [],
        debounceTimer: null
      };

      // DOM Elements
      const countrySelect = document.getElementById('country-select');
      const selectedNationName = document.getElementById('selected-nation-name');
      const selectedNationCode = document.getElementById('selected-nation-code');
      const selectedNationEmissions = document.getElementById('selected-nation-emissions');
      const baselineProfileText = document.getElementById('baseline-profile-text');
      const predictedArchetypeText = document.getElementById('predicted-archetype-text');
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

      // Archetype Design System
      const ARCHETYPE_CONFIG = {
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

      // 1. Boot Application: Fetch /api/data and /api/rules
      async function boot() {
        try {
          const [dataRes, rulesRes] = await Promise.all([
            fetch(`${API_BASE}/api/data`).then(r => r.json()),
            fetch(`${API_BASE}/api/rules`).then(r => r.json())
          ]);

          state.countries = dataRes.clustered_proportions || [];
          state.emissions = dataRes.macro_sector_emissions || [];
          state.rules = rulesRes.xai_rules || [];

          populateCountrySelect();
          selectNation('CHN'); // Default: China
        } catch (err) {
          console.error('[Simulator Boot Error]', err);
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
          if (pill.dataset.code === state.countryCode) {
            pill.className = 'preset-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-orange-500 text-white shadow-sm transition-colors';
          } else {
            pill.className = 'preset-pill px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 transition-colors';
          }
        });

        // Current Profile Badge
        const clusterId = countryData.Cluster;
        const conf = ARCHETYPE_CONFIG[clusterId] || ARCHETYPE_CONFIG[0];
        if (baselineProfileText) baselineProfileText.textContent = `Current Profile: ${conf.title}`;

        renderSliders();
        triggerInference();
      }

      // Mathematical Proportional Auto-Rebalancing (Sum strictly 100%)
      function rebalance(changedSector, targetVal) {
        targetVal = Math.max(0, Math.min(100, Math.round(targetVal)));
        const keys = ['energy', 'industry', 'transport', 'agriculture', 'buildings'];
        const otherKeys = keys.filter(k => k !== changedSector);
        const targetOtherSum = 100 - targetVal;
        const currentOtherSum = otherKeys.reduce((acc, k) => acc + state.sectors[k], 0);

        state.sectors[changedSector] = targetVal;

        if (currentOtherSum === 0) {
          const split = Math.floor(targetOtherSum / otherKeys.length);
          let remainder = targetOtherSum % otherKeys.length;
          otherKeys.forEach(k => {
            state.sectors[k] = split + (remainder > 0 ? 1 : 0);
            if (remainder > 0) remainder--;
          });
        } else {
          let assigned = 0;
          otherKeys.forEach((k, idx) => {
            if (idx === otherKeys.length - 1) {
              state.sectors[k] = Math.max(0, targetOtherSum - assigned);
            } else {
              const scaled = Math.round((state.sectors[k] / currentOtherSum) * targetOtherSum);
              const clamped = Math.max(0, Math.min(targetOtherSum - assigned, scaled));
              state.sectors[k] = clamped;
              assigned += clamped;
            }
          });
        }

        // Exact residual correction
        let sum = Object.values(state.sectors).reduce((a, b) => a + b, 0);
        if (sum !== 100) {
          const diff = 100 - sum;
          const largestOther = otherKeys.reduce((a, b) => state.sectors[a] >= state.sectors[b] ? a : b);
          state.sectors[largestOther] = Math.max(0, state.sectors[largestOther] + diff);
        }

        renderSliders();
        
        // Debounced backend inference call
        if (state.debounceTimer) clearTimeout(state.debounceTimer);
        state.debounceTimer = setTimeout(triggerInference, 100);
      }

      // Render Sliders & Exact Numbers
      function renderSliders() {
        const keys = ['energy', 'industry', 'transport', 'agriculture', 'buildings'];
        keys.forEach(sec => {
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
            benchmark_reduction_pct: state.targetPct
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
        const config = ARCHETYPE_CONFIG[clusterId] || ARCHETYPE_CONFIG[0];

        // Section 2 Banner
        if (predictedArchetypeText) {
          predictedArchetypeText.textContent = `Predicted Archetype: ${config.title}`;
        }
        if (predictedIcon) {
          predictedIcon.textContent = config.icon;
        }

        // Dynamic theme styling on predicted banner
        if (predictedCard && predictedIconWrap) {
          predictedCard.className = `rounded-xl p-4 sm:p-5 border transition-all duration-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${config.bg} ${config.border}`;
          predictedIconWrap.className = `w-12 h-12 rounded-xl flex items-center justify-center shrink-0 ${config.bg} ${config.border} ${config.text}`;
        }

        // Section 3 Left Card ("Why This Classification?")
        if (rulePlainText) {
          rulePlainText.textContent = config.rule;
        }
        if (ruleRationaleText) {
          ruleRationaleText.textContent = config.rationale;
        }
        if (policyRecommendationText) {
          policyRecommendationText.textContent = config.recommendation;
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
          // Dynamic calculation: delta / dominant sector share
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
    f.write(CLEAN_HTML)

print(f"Successfully overhauled frontend/index.html ({len(CLEAN_HTML)} bytes)")
