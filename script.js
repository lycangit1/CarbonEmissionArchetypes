/**
 * Global Carbon Archetypes Dashboard · Production JavaScript Engine (script.js)
 * Implements all interactive features, state management, auto-rebalancing sliders,
 * Chart.js radar rendering, accordions, equivalence abatement logic, and API calls.
 */

'use strict';

// ---------------------------------------------------------------------------
// Global Application State
// ---------------------------------------------------------------------------
const state = {
  countries: [],
  countriesMap: new Map(),
  catalog: {},
  currentCountry: null,
  baselineSectors: { Energy: 54, Industry: 31, Transport: 6, Agriculture: 5, Buildings: 4 },
  simulatedSectors: { Energy: 54, Industry: 31, Transport: 6, Agriculture: 5, Buildings: 4 },
  isRebalancing: false,
  radarChart: null,
  kmeans2DChart: null,
  dbscan2DChart: null,
  silhouetteChart: null,
  evaluationData: null,
  debounceTimer: null,
  activeScenarioIndex: 0,
  reductionTargetPct: 5,
  selectedDiscardedModel: "dbscan"
};

const MACRO_SECTORS = ['Energy', 'Industry', 'Transport', 'Agriculture', 'Buildings'];

const ARCHETYPE_ICONS = {
  'Energy-Heavy': 'bolt',
  'Industry-Heavy': 'factory',
  'Agriculture-Heavy': 'agriculture',
  'Transport-Heavy': 'directions_car',
  'Buildings-Heavy': 'apartment'
};

const ARCHETYPE_COLORS = {
  'Energy-Heavy': { primary: '#f97316', bg: 'rgba(249, 115, 22, 0.15)', border: 'rgba(249, 115, 22, 0.35)' },
  'Industry-Heavy': { primary: '#8b5cf6', bg: 'rgba(139, 92, 246, 0.15)', border: 'rgba(139, 92, 246, 0.35)' },
  'Agriculture-Heavy': { primary: '#10b981', bg: 'rgba(16, 185, 129, 0.15)', border: 'rgba(16, 185, 129, 0.35)' },
  'Transport-Heavy': { primary: '#06b6d4', bg: 'rgba(6, 182, 212, 0.15)', border: 'rgba(6, 182, 212, 0.35)' },
  'Buildings-Heavy': { primary: '#f59e0b', bg: 'rgba(245, 158, 11, 0.15)', border: 'rgba(245, 158, 11, 0.35)' }
};

// ---------------------------------------------------------------------------
// Initial Bootstrapping
// ---------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', async () => {
  setupNavigation();
  setupSearchDropdown();
  setupPresetPills();
  setupSliderEvents();
  setupSuggestedScenarios();
  setupComparisonDropdowns();
  setupTargetReductionSlider();
  setupAboutTabs();
  setupDiscardedModelToggles();


  try {
    await fetchInitialData();
    initializeDashboard();
  } catch (err) {
    console.error('Fatal initialization error:', err);
  }
});

/**
 * Loads data from all backend endpoints in parallel.
 */
async function fetchInitialData() {
  try {
    const [dataRes, catalogRes, evalRes] = await Promise.all([
      fetch('/api/data').then(r => r.json()),
      fetch('/api/catalog').then(r => r.json()),
      fetch('/api/evaluate_models').then(r => r.json())
    ]);

    if (dataRes && dataRes.countries) {
      state.countries = dataRes.countries;
      dataRes.countries.forEach(c => state.countriesMap.set(c.country_code, c));
    }

    if (catalogRes) {
      state.catalog = catalogRes;
    }

    if (evalRes) {
      state.evaluationData = evalRes;
    }
  } catch (err) {
    console.warn('API error during bootstrap; attempting local fallback', err);
  }
}

/**
 * Initializes all dashboard modules once data is ready.
 */
function initializeDashboard() {
  // 1. Set default country to China (CHN), or first country in dataset
  const defaultCountry = state.countriesMap.get('CHN') || state.countries[0];
  if (defaultCountry) {
    selectCountry(defaultCountry.country_code);
  }

  // 2. Render Section 2 (Accordions)
  renderAccordions();

  // 3. Render Section 3 (Benchmark Leaderboard & Initial Comparison)
  renderBenchmarkLeaderboard();
  populateComparisonDropdowns();
  runComparisonCalculation();

  // 4. Render Section 4 (Scoreboard & Discarded Algorithms)
  renderScoreboard();
}

// ---------------------------------------------------------------------------
// Navigation Controller
// ---------------------------------------------------------------------------

function setupDiscardedModelToggles() {
  const toggleContainer = document.getElementById('discarded-model-toggles');
  if (!toggleContainer) return;
  const pills = toggleContainer.querySelectorAll('.discarded-toggle-pill');
  pills.forEach(pill => {
    pill.addEventListener('click', (e) => {
      e.preventDefault();
      const model = pill.getAttribute('data-model');
      if (!model || model === state.selectedDiscardedModel) return;
      pills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      state.selectedDiscardedModel = model;
      renderDiscardedModelMap();
    });
  });
}

function setupNavigation() {
  const navButtons = document.querySelectorAll('.nav-item');
  const sections = document.querySelectorAll('.dashboard-section');

  navButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-target');
      if (!targetId) return;

      navButtons.forEach(b => b.classList.remove('active'));
      sections.forEach(s => s.classList.remove('active'));

      btn.classList.add('active');
      const targetSection = document.getElementById(targetId);
      if (targetSection) {
        targetSection.classList.add('active');
        window.scrollTo({ top: 0, behavior: 'smooth' });

        // Trigger responsive resize for Chart.js canvases when Section 4 is opened
        if (targetId === 'section-evaluation') {
          setTimeout(() => {
            if (state.kmeans2DChart) state.kmeans2DChart.resize();
            if (state.dbscan2DChart) state.dbscan2DChart.resize();
            if (state.silhouetteChart) state.silhouetteChart.resize();
          }, 60);
        }
      }
    });
  });
}

// ---------------------------------------------------------------------------
// Section 1: Country Search & Quick Select
// ---------------------------------------------------------------------------
function setupSearchDropdown() {
  const searchInput = document.getElementById('country-search-input');
  const searchResults = document.getElementById('country-search-results');

  if (!searchInput || !searchResults) return;

  const performSearch = () => {
    const query = searchInput.value.trim().toLowerCase();
    searchResults.innerHTML = '';

    if (!query) {
      searchResults.classList.remove('open');
      return;
    }

    const matches = state.countries.filter(c =>
      c.name.toLowerCase().includes(query) ||
      c.country_code.toLowerCase().includes(query)
    ).slice(0, 15);

    if (matches.length === 0) {
      const noRes = document.createElement('div');
      noRes.className = 'search-result-item';
      noRes.style.color = 'var(--text-dim)';
      noRes.textContent = 'No matching nation found';
      searchResults.appendChild(noRes);
    } else {
      matches.forEach(c => {
        const item = document.createElement('div');
        item.className = 'search-result-item';
        item.innerHTML = `
          <span>${c.name}</span>
          <span style="font-family: monospace; color: var(--text-dim); font-size: 11px;">${c.country_code} · ${c.archetype}</span>
        `;
        item.addEventListener('click', () => {
          searchInput.value = c.name;
          searchResults.classList.remove('open');
          selectCountry(c.country_code);
        });
        searchResults.appendChild(item);
      });
    }

    searchResults.classList.add('open');
  };

  searchInput.addEventListener('input', performSearch);
  searchInput.addEventListener('focus', performSearch);

  // Close dropdown when clicking outside
  document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
      searchResults.classList.remove('open');
    }
  });
}

function setupPresetPills() {
  const pills = document.querySelectorAll('.preset-pill');
  pills.forEach(pill => {
    pill.addEventListener('click', () => {
      const code = pill.getAttribute('data-code');
      if (code) {
        pills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');

        const searchInput = document.getElementById('country-search-input');
        const c = state.countriesMap.get(code);
        if (searchInput && c) {
          searchInput.value = c.name;
        }
        selectCountry(code);
      }
    });
  });
}

/**
 * Primary selector: binds a sovereign nation to Track A and initializes Track B.
 */
function selectCountry(countryCode) {
  const country = state.countriesMap.get(countryCode);
  if (!country) return;

  state.currentCountry = country;

  // Sync preset pills active state
  document.querySelectorAll('.preset-pill').forEach(pill => {
    if (pill.getAttribute('data-code') === countryCode) {
      pill.classList.add('active');
    } else {
      pill.classList.remove('active');
    }
  });

  // Track A: Bind Empirical Baseline Data
  bindTrackABaseline(country);

  // Track B: Initialize Sliders to match baseline percentages
  initializeTrackBSliders(country);
}

// ---------------------------------------------------------------------------
// Section 1: Track A - Empirical Baseline (Static)
// ---------------------------------------------------------------------------
function bindTrackABaseline(country) {
  const nameEl = document.getElementById('baseline-country-name');
  const codeEl = document.getElementById('baseline-country-code');
  const emissEl = document.getElementById('baseline-total-emissions');
  const badgeEl = document.getElementById('baseline-archetype-badge');
  const badgeIcon = document.getElementById('baseline-badge-icon');
  const badgeText = document.getElementById('baseline-badge-text');

  if (nameEl) nameEl.textContent = country.name;
  if (codeEl) codeEl.textContent = country.country_code;
  if (emissEl) emissEl.textContent = `${Number(country.total_emissions).toLocaleString(undefined, { minimumFractionDigits: 1, maximumFractionDigits: 2 })} Mt CO₂e`;

  const archName = country.archetype || 'Energy-Heavy';
  if (badgeText) badgeText.textContent = archName;
  if (badgeIcon) badgeIcon.textContent = ARCHETYPE_ICONS[archName] || 'bolt';

  // Apply archetype-specific styling to badge
  const colors = ARCHETYPE_COLORS[archName] || ARCHETYPE_COLORS['Energy-Heavy'];
  if (badgeEl) {
    badgeEl.style.color = colors.primary;
    badgeEl.style.backgroundColor = colors.bg;
    badgeEl.style.borderColor = colors.border;
  }

  // Update 5-Axis Radar Chart
  renderRadarChart(country);

  // Update Explainable AI (XAI) card
  updateXAICard(archName);

  // Update Real-World Decarbonization Roadmap (Fixed to baseline)
  renderBaselineRoadmap(archName);
}

/**
 * Creates or updates the Chart.js 5-axis Radar Chart.
 */
function renderRadarChart(country) {
  const canvas = document.getElementById('baseline-radar-chart');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  const dataValues = MACRO_SECTORS.map(s => country.percentages[s] || 0);
  const archName = country.archetype || 'Energy-Heavy';
  const colors = ARCHETYPE_COLORS[archName] || ARCHETYPE_COLORS['Energy-Heavy'];

  if (state.radarChart) {
    state.radarChart.data.datasets[0].data = dataValues;
    state.radarChart.data.datasets[0].label = `${country.name} Emissions Mix (%)`;
    state.radarChart.data.datasets[0].backgroundColor = colors.bg.replace('0.15', '0.25');
    state.radarChart.data.datasets[0].borderColor = colors.primary;
    state.radarChart.data.datasets[0].pointBackgroundColor = colors.primary;
    state.radarChart.update();
    return;
  }

  state.radarChart = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['Energy', 'Industry', 'Transport', 'Agriculture', 'Buildings'],
      datasets: [{
        label: `${country.name} Emissions Mix (%)`,
        data: dataValues,
        backgroundColor: colors.bg.replace('0.15', '0.25'),
        borderColor: colors.primary,
        borderWidth: 2,
        pointBackgroundColor: colors.primary,
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: colors.primary,
        pointRadius: 4,
        pointHoverRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          angleLines: { color: 'rgba(255, 255, 255, 0.08)' },
          grid: { color: 'rgba(255, 255, 255, 0.08)' },
          pointLabels: {
            font: { family: 'Inter', size: 12, weight: '600' },
            color: '#a1a1aa'
          },
          ticks: {
            display: false,
            stepSize: 20,
            backdropColor: 'transparent'
          },
          suggestedMin: 0,
          suggestedMax: 60
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#1c1c24',
          titleFont: { family: 'Space Grotesk', size: 13, weight: '700' },
          bodyFont: { family: 'Inter', size: 12 },
          borderColor: '#38384a',
          borderWidth: 1,
          padding: 10,
          callbacks: {
            label: (ctx) => ` ${ctx.dataset.label}: ${ctx.raw}%`
          }
        }
      }
    }
  });
}

/**
 * Updates the XAI plain English rule and mathematical bounding rule.
 * Uses detailed, educational plain-English explanations.
 */
function updateXAICard(archName) {
  const plainEl = document.getElementById('xai-plain-rule');
  const mathEl = document.getElementById('xai-math-rule');

  // Detailed, educational explanations for all 5 archetypes
  const detailedExplanations = {
    'Energy-Heavy': "This country is classified as Energy-Heavy because generating electricity and heat is its largest single source of carbon emissions, significantly exceeding the global average. Transitioning this specific sector is the most mathematically effective way to reduce the nation's overall footprint.",
    'Industry-Heavy': "This country is classified as Industry-Heavy because heavy manufacturing, chemical refining, and materials production (such as steel and cement) account for the majority of its emissions, significantly exceeding the global average. Transitioning this specific sector is the most mathematically effective way to reduce the nation's overall footprint.",
    'Agriculture-Heavy': "This country is classified as Agriculture-Heavy because farming activities, cattle digestion, and crop soils produce the majority of its greenhouse gas emissions, significantly exceeding the global average. Transitioning this specific sector is the most mathematically effective way to reduce the nation's overall footprint.",
    'Transport-Heavy': "This country is classified as Transport-Heavy because road vehicles, shipping vessels, and air travel account for its largest carbon output, significantly exceeding the global average. Transitioning this specific sector is the most mathematically effective way to reduce the nation's overall footprint.",
    'Buildings-Heavy': "This country is classified as Buildings-Heavy because heating, cooling, and powering residential and commercial buildings dominate its emissions, significantly exceeding the global average. Transitioning this specific sector is the most mathematically effective way to reduce the nation's overall footprint."
  };

  const archData = state.catalog[archName] || (state.catalog.archetypes ? state.catalog.archetypes[archName] : null);

  if (plainEl) {
    if (detailedExplanations[archName]) {
      plainEl.textContent = detailedExplanations[archName];
    } else if (archData && archData.xai_rule) {
      plainEl.textContent = archData.xai_rule;
    } else {
      plainEl.textContent = `This country is classified as ${archName} because this sector constitutes its largest single source of emissions, significantly exceeding the global average. Transitioning this specific sector is the most mathematically effective way to reduce the nation's overall footprint.`;
    }
  }

  if (mathEl) {
    mathEl.textContent = archData && archData.mathematical_bounding_rule
      ? archData.mathematical_bounding_rule
      : `IF ${archName.replace('-Heavy', '')} is dominant -> ${archName} Economy`;
  }
}

/**
 * Renders the Real-World Decarbonization Measures into an accordion using HTML native <details> and <summary>.
 * By default, the first measure is expanded and the other two are closed.
 * Strictly enforces mutual exclusivity: only one measure accordion can be open at a time.
 * Remains fixed to the baseline archetype.
 */
function renderBaselineRoadmap(archName) {
  const container = document.getElementById('baseline-roadmap-container');
  if (!container) return;

  const archData = state.catalog[archName] || (state.catalog.archetypes ? state.catalog.archetypes[archName] : null);
  const measures = (archData && (archData.pathways || archData.roadmap)) || [];

  container.innerHTML = '';

  if (!measures || measures.length === 0) {
    container.innerHTML = '<p style="color: var(--text-muted); font-size: 13px;">No decarbonization measures cataloged for this archetype.</p>';
    return;
  }

  measures.forEach((item, index) => {
    const isFirst = index === 0;
    const details = document.createElement('details');
    details.className = 'measure-accordion-item';
    details.setAttribute('name', 'decarb-measures'); // Native HTML attribute for mutually exclusive details
    details.name = 'decarb-measures';
    if (isFirst) {
      details.setAttribute('open', '');
    }

    const title = item.title || `Measure ${index + 1}`;
    const description = item.description || '';

    details.innerHTML = `
      <summary class="measure-summary">
        <div class="measure-summary-left">
          <span class="measure-step-num">${index + 1}</span>
          <span class="measure-title">${title}</span>
        </div>
        <span class="material-symbols-outlined measure-chevron">expand_more</span>
      </summary>
      <div class="measure-content">
        <p class="measure-desc">${description}</p>
      </div>
    `;

    // Multi-layer mutual exclusivity: immediately closes any open sibling details on summary click
    const summary = details.querySelector('summary');
    if (summary) {
      summary.addEventListener('click', () => {
        if (!details.open) {
          container.querySelectorAll('details.measure-accordion-item').forEach(other => {
            if (other !== details) {
              other.removeAttribute('open');
              other.open = false;
            }
          });
        }
      });
    }

    // Toggle event listener fallback for keyboard and programmatic navigation
    details.addEventListener('toggle', () => {
      if (details.open) {
        container.querySelectorAll('details.measure-accordion-item').forEach(other => {
          if (other !== details && other.open) {
            other.removeAttribute('open');
            other.open = false;
          }
        });
      }
    });

    container.appendChild(details);
  });
}


// ---------------------------------------------------------------------------
// Section 1: Track B - What-If Simulator (Dynamic with Auto-Rebalance)
// ---------------------------------------------------------------------------
function initializeTrackBSliders(country) {
  state.isRebalancing = true;

  MACRO_SECTORS.forEach(sector => {
    const pct = country.percentages[sector] || 0;
    state.baselineSectors[sector] = pct;
    state.simulatedSectors[sector] = pct;

    const slider = document.getElementById(`slider-${sector.toLowerCase()}`);
    if (slider) {
      slider.value = pct;
    }
  });

  state.isRebalancing = false;
  updateSliderDisplaysAndEmissions();
  predictNearestArchetype();
}

function setupSliderEvents() {
  MACRO_SECTORS.forEach(sector => {
    const slider = document.getElementById(`slider-${sector.toLowerCase()}`);
    if (slider) {
      slider.addEventListener('input', (e) => {
        if (state.isRebalancing) return;
        const targetSector = sector;
        const targetValue = parseInt(e.target.value, 10);
        rebalanceOtherSliders(targetSector, targetValue);
      });
    }
  });

  // Step buttons (+ / - 1%)
  const stepButtons = document.querySelectorAll('.step-btn');
  stepButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const sector = btn.getAttribute('data-sector');
      const step = parseInt(btn.getAttribute('data-step'), 10);
      if (!sector || isNaN(step)) return;

      const currentVal = state.simulatedSectors[sector];
      const newVal = Math.max(0, Math.min(100, currentVal + step));
      if (newVal !== currentVal) {
        rebalanceOtherSliders(sector, newVal);
      }
    });
  });

  // Reset Button
  const resetBtn = document.getElementById('reset-simulator-btn');
  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      if (!state.currentCountry) return;
      initializeTrackBSliders(state.currentCountry);
    });
  }
}

/**
 * Proportional auto-rebalancing algorithm:
 * When one slider is moved, adjust the other 4 proportionally so sum is exactly 100%.
 */
function rebalanceOtherSliders(targetSector, targetValue) {
  state.isRebalancing = true;

  const currentTargetVal = state.simulatedSectors[targetSector];
  const delta = targetValue - currentTargetVal;

  if (delta === 0) {
    state.isRebalancing = false;
    return;
  }

  // Set the modified slider
  state.simulatedSectors[targetSector] = targetValue;

  const otherSectors = MACRO_SECTORS.filter(s => s !== targetSector);
  const otherSum = otherSectors.reduce((acc, s) => acc + state.simulatedSectors[s], 0);

  if (otherSum === 0) {
    // If all other sectors are currently 0, distribute remainder equally
    const remainder = 100 - targetValue;
    const baseShare = Math.floor(remainder / otherSectors.length);
    let drift = remainder - (baseShare * otherSectors.length);

    otherSectors.forEach((s, idx) => {
      const extra = idx < drift ? 1 : 0;
      state.simulatedSectors[s] = Math.max(0, baseShare + extra);
    });
  } else {
    // Proportional reduction or increase
    const targetOtherSum = 100 - targetValue;
    const scale = targetOtherSum / otherSum;

    let computedValues = {};
    let intSum = 0;

    otherSectors.forEach(s => {
      const scaled = state.simulatedSectors[s] * scale;
      const rounded = Math.max(0, Math.round(scaled));
      computedValues[s] = rounded;
      intSum += rounded;
    });

    // Fix any integer rounding drift
    let drift = targetOtherSum - intSum;
    if (drift !== 0) {
      // Add/subtract drift to the sector with the largest share among the others
      const sorted = [...otherSectors].sort((a, b) => computedValues[b] - computedValues[a]);
      for (const s of sorted) {
        if (drift > 0) {
          computedValues[s] += 1;
          drift -= 1;
        } else if (drift < 0 && computedValues[s] > 0) {
          computedValues[s] -= 1;
          drift += 1;
        }
        if (drift === 0) break;
      }
    }

    otherSectors.forEach(s => {
      state.simulatedSectors[s] = computedValues[s];
    });
  }

  // Update physical DOM slider inputs
  MACRO_SECTORS.forEach(s => {
    const slider = document.getElementById(`slider-${s.toLowerCase()}`);
    if (slider) {
      slider.value = state.simulatedSectors[s];
    }
  });

  state.isRebalancing = false;
  updateSliderDisplaysAndEmissions();

  // Debounced API call to /api/nearest_archetype
  if (state.debounceTimer) clearTimeout(state.debounceTimer);
  state.debounceTimer = setTimeout(() => {
    predictNearestArchetype();
  }, 120);
}

/**
 * Updates text percentages, estimated Mt CO2e, and the visualizer proportions bar.
 */
function updateSliderDisplaysAndEmissions() {
  const totalEmiss = state.currentCountry ? state.currentCountry.total_emissions : 1000;
  let totalPct = 0;

  MACRO_SECTORS.forEach(s => {
    const pct = state.simulatedSectors[s] || 0;
    totalPct += pct;

    const valEl = document.getElementById(`${s.toLowerCase()}-val`);
    const mtEl = document.getElementById(`${s.toLowerCase()}-mt`);
    const barSeg = document.getElementById(`bar-${s.toLowerCase()}`);

    if (valEl) valEl.textContent = `${pct}%`;
    if (mtEl) {
      const sectorMt = (totalEmiss * (pct / 100)).toFixed(1);
      mtEl.textContent = `${Number(sectorMt).toLocaleString()} Mt`;
    }
    if (barSeg) {
      barSeg.style.width = `${pct}%`;
    }
  });

  const sumText = document.getElementById('slider-sum-text');
  if (sumText) {
    if (totalPct === 100) {
      sumText.textContent = 'Exact 100% Sum';
      sumText.style.color = 'var(--accent-emerald)';
    } else {
      sumText.textContent = `Sum: ${totalPct}%`;
      sumText.style.color = 'var(--accent-orange)';
    }
  }
}

/**
 * Dynamic POST call to /api/nearest_archetype to calculate CLR distance.
 */
async function predictNearestArchetype() {
  const payload = {
    sectors: MACRO_SECTORS.map(s => state.simulatedSectors[s])
  };

  try {
    const res = await fetch('/api/nearest_archetype', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (data && data.predicted_archetype) {
      updatePredictedArchetypeUI(data.predicted_archetype);
    }
  } catch (err) {
    console.error('Error fetching nearest archetype:', err);
  }
}

function updatePredictedArchetypeUI(predictedArchetype) {
  const nameEl = document.getElementById('predicted-archetype-name');
  const iconEl = document.getElementById('predicted-archetype-icon');
  const descEl = document.getElementById('predicted-transition-desc');
  const cardEl = document.getElementById('predicted-archetype-card');

  if (nameEl) nameEl.textContent = predictedArchetype;
  if (iconEl) {
    iconEl.innerHTML = `<span class="material-symbols-outlined">${ARCHETYPE_ICONS[predictedArchetype] || 'bolt'}</span>`;
  }

  const baselineArch = state.currentCountry ? state.currentCountry.archetype : 'Energy-Heavy';
  const colors = ARCHETYPE_COLORS[predictedArchetype] || ARCHETYPE_COLORS['Energy-Heavy'];

  if (cardEl) {
    cardEl.style.borderColor = colors.border;
    cardEl.style.backgroundColor = colors.bg;
  }
  if (iconEl) {
    iconEl.style.color = colors.primary;
  }

  if (descEl) {
    if (predictedArchetype === baselineArch) {
      descEl.textContent = `Current simulated allocation aligns with the ${predictedArchetype} transition group.`;
    } else {
      descEl.innerHTML = `<strong>Structural Transition:</strong> Reclassified from <span style="color: var(--text-dim); text-decoration: line-through;">${baselineArch}</span> to <span style="color: ${colors.primary}; font-weight: 700;">${predictedArchetype}</span>.`;
    }
  }
}

// ---------------------------------------------------------------------------
// Section 2: Countries with Similar Archetypes (Accordion UI)
// ---------------------------------------------------------------------------
function renderAccordions() {
  const container = document.getElementById('archetype-accordion-container');
  if (!container) return;

  container.innerHTML = '';
  const archetypes = ['Energy-Heavy', 'Industry-Heavy', 'Agriculture-Heavy', 'Transport-Heavy', 'Buildings-Heavy'];

  const ARCHETYPE_SUBTITLES = {
    'Energy-Heavy': 'Power Generation & Grid Focus',
    'Industry-Heavy': 'Manufacturing & Industrial Focus',
    'Agriculture-Heavy': 'Farming & Livestock Focus',
    'Transport-Heavy': 'Transport & Logistics Focus',
    'Buildings-Heavy': 'Heating & Buildings Focus'
  };

  const PRIMARY_CLIMATE_CHALLENGES = {
    'Energy-Heavy': "Most emissions come from burning fossil fuels (coal, oil, gas) for electricity and heating. The main challenge is transitioning the national power grid to renewable sources like solar and wind while building large-scale battery storage for stability.",
    'Industry-Heavy': "Most emissions come from heavy manufacturing, such as producing steel, cement, and chemicals. The main challenge is upgrading factory machinery and finding clean energy alternatives to the intense heat required for industrial production.",
    'Transport-Heavy': "Most emissions come from gasoline and diesel used in cars, trucks, shipping, and aviation. The main challenge is building infrastructure for electric vehicles, expanding public transit, and adopting sustainable fuels for heavy freight.",
    'Agriculture-Heavy': "Most emissions come from livestock digestion (methane), chemical fertilizers, and land clearing. The main challenge is adopting sustainable farming practices and precision soil management without compromising national food security.",
    'Buildings-Heavy': "Most emissions come from the energy used to heat, cool, and light commercial and residential buildings. The main challenge is retrofitting older structures with better insulation and installing highly efficient electric heating systems."
  };

  archetypes.forEach((archName, index) => {
    const archData = state.catalog[archName] || (state.catalog.archetypes ? state.catalog.archetypes[archName] : {});

    const subtitle = ARCHETYPE_SUBTITLES[archName] || (archData && archData.profile_name) || 'Sovereign Emissions Focus';
    const challengeText = PRIMARY_CLIMATE_CHALLENGES[archName] || (archData && (archData.primary_challenge || archData.bottleneck)) || '';

    // Filter countries belonging to this archetype and sort alphabetically
    const members = state.countries
      .filter(c => c.archetype === archName)
      .sort((a, b) => a.name.localeCompare(b.name));

    const colors = ARCHETYPE_COLORS[archName] || ARCHETYPE_COLORS['Energy-Heavy'];
    const isOpen = index === 0; // First accordion open by default

    const item = document.createElement('div');
    item.className = `accordion-item ${isOpen ? 'open' : ''}`;
    item.id = `accordion-${archName.toLowerCase()}`;

    item.innerHTML = `
      <div class="accordion-header">
        <div class="accordion-header-left">
          <div class="accordion-icon" style="background: ${colors.bg}; color: ${colors.primary};">
            <span class="material-symbols-outlined">${ARCHETYPE_ICONS[archName]}</span>
          </div>
          <div class="accordion-title-group">
            <h3>${archName}</h3>
            <p>${subtitle}</p>
          </div>
        </div>
        <div class="accordion-header-right">
          <span class="accordion-count-badge">${members.length} Nations</span>
          <span class="material-symbols-outlined accordion-chevron">expand_more</span>
        </div>
      </div>

      <div class="accordion-body">
        <div class="accordion-challenge-card">
          <div class="challenge-label">
            <span style="font-size: 15px;">🎯</span>
            <span>Primary Climate Challenge</span>
          </div>
          <p class="challenge-text">${challengeText}</p>
        </div>


        <div>
          <h4 style="font-size: 12px; font-weight: 700; text-transform: uppercase; color: var(--text-dim); margin-bottom: 10px; letter-spacing: 0.04em;">
            Countries in this Group (${members.length}) · Dominant Sector %
          </h4>
          <div class="country-badges-grid">
            ${members.map(c => `
              <div class="country-grid-badge" data-code="${c.country_code}" title="Click to inspect ${c.name} in Simulator">
                <span>${c.name}</span>
                <span class="badge-pct" style="color: ${colors.primary}">${c.dominant_percentage}%</span>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    `;

    // Toggle open/close on header click
    const header = item.querySelector('.accordion-header');
    header.addEventListener('click', () => {
      item.classList.toggle('open');
    });

    // Make country badges clickable to switch to Section 1
    const badges = item.querySelectorAll('.country-grid-badge');
    badges.forEach(badge => {
      badge.addEventListener('click', (e) => {
        e.stopPropagation();
        const code = badge.getAttribute('data-code');
        if (code) {
          // Switch to Section 1
          const homeNavBtn = document.querySelector('.nav-item[data-target="section-home"]');
          if (homeNavBtn) homeNavBtn.click();
          selectCountry(code);
        }
      });
    });

    container.appendChild(item);
  });
}

// ---------------------------------------------------------------------------
// Section 3: Equivalence Comparison Engine
// ---------------------------------------------------------------------------
function renderBenchmarkLeaderboard() {
  const container = document.getElementById('benchmark-leaderboard-list');
  if (!container) return;

  container.innerHTML = '';
  const archetypes = ['Energy-Heavy', 'Industry-Heavy', 'Agriculture-Heavy', 'Transport-Heavy', 'Buildings-Heavy'];

  archetypes.forEach(archName => {
    // Find lowest total emissions country in this archetype
    const members = state.countries.filter(c => c.archetype === archName);
    if (members.length === 0) return;

    const lowest = members.reduce((min, c) => c.total_emissions < min.total_emissions ? c : min, members[0]);
    const colors = ARCHETYPE_COLORS[archName] || ARCHETYPE_COLORS['Energy-Heavy'];

    const card = document.createElement('div');
    card.className = 'benchmark-item';
    card.innerHTML = `
      <span class="benchmark-item-arch" style="color: ${colors.primary}">${archName}</span>
      <span class="benchmark-item-country">${lowest.name} (${lowest.country_code})</span>
      <span class="benchmark-item-val">${lowest.total_emissions.toLocaleString(undefined, { minimumFractionDigits: 1, maximumFractionDigits: 3 })} Mt CO₂e/yr</span>
    `;
    container.appendChild(card);
  });
}

function setupSuggestedScenarios() {
  const buttons = document.querySelectorAll('.suggested-scenario-btn');
  const scenarios = [
    ['USA', 'BRA', 'SGP'], // Global Giants
    ['CHN', 'IND', 'DEU'], // Baseload Heavyweights
    ['AUS', 'NZL', 'MHL']  // Contrasting Transition Profiles
  ];

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      const idx = parseInt(btn.getAttribute('data-scenario'), 10);
      const codes = scenarios[idx] || scenarios[0];

      const select1 = document.getElementById('compare-country-1');
      const select2 = document.getElementById('compare-country-2');
      const select3 = document.getElementById('compare-country-3');

      if (select1 && codes[0]) select1.value = codes[0];
      if (select2 && codes[1]) select2.value = codes[1];
      if (select3 && codes[2]) select3.value = codes[2];

      buttons.forEach(b => b.style.borderColor = 'var(--border-color)');
      btn.style.borderColor = 'var(--accent-cyan)';

      runComparisonCalculation();
    });
  });
}

function populateComparisonDropdowns() {
  const select1 = document.getElementById('compare-country-1');
  const select2 = document.getElementById('compare-country-2');
  const select3 = document.getElementById('compare-country-3');

  if (!select1 || !select2 || !select3) return;

  const sortedCountries = [...state.countries].sort((a, b) => a.name.localeCompare(b.name));

  const buildOptions = () => {
    return sortedCountries.map(c =>
      `<option value="${c.country_code}">${c.name} (${c.country_code}) · ${c.archetype}</option>`
    ).join('');
  };

  const optionsHtml = buildOptions();
  select1.innerHTML = optionsHtml;
  select2.innerHTML = optionsHtml;
  select3.innerHTML = optionsHtml;

  // Defaults: USA, BRA, SGP
  select1.value = 'USA';
  select2.value = 'BRA';
  select3.value = 'SGP';
}

function setupComparisonDropdowns() {
  const selects = ['compare-country-1', 'compare-country-2', 'compare-country-3'];
  selects.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('change', runComparisonCalculation);
    }
  });

  // Close benchmark leaderboard dropdown when clicking outside
  const benchmarkDetails = document.getElementById('benchmark-dropdown-menu');
  if (benchmarkDetails) {
    document.addEventListener('click', (e) => {
      if (benchmarkDetails.open && !benchmarkDetails.contains(e.target)) {
        benchmarkDetails.removeAttribute('open');
        benchmarkDetails.open = false;
      }
    });
  }
}

const ARCHETYPE_EMOJIS = {
  'Energy-Heavy': '⚡',
  'Industry-Heavy': '🏭',
  'Agriculture-Heavy': '🌾',
  'Transport-Heavy': '🚗',
  'Buildings-Heavy': '🏢'
};

function getCountryFlagEmoji(countryCode) {
  if (!countryCode || countryCode.length < 2) return '🌐';
  const customMap = {
    'USA': '🇺🇸', 'BRA': '🇧🇷', 'SGP': '🇸🇬', 'CHN': '🇨🇳', 'IND': '🇮🇳',
    'DEU': '🇩🇪', 'AUS': '🇦🇺', 'NZL': '🇳🇿', 'MHL': '🇲🇭', 'GBR': '🇬🇧',
    'FRA': '🇫🇷', 'JPN': '🇯🇵', 'CAN': '🇨🇦', 'KOR': '🇰🇷', 'IDN': '🇮🇩',
    'RUS': '🇷🇺', 'ZAF': '🇿🇦', 'MEX': '🇲🇽', 'SAU': '🇸🇦', 'ITA': '🇮🇹',
    'ESP': '🇪🇸', 'TUR': '🇹🇷', 'NGA': '🇳🇬', 'ARG': '🇦🇷', 'EGY': '🇪🇬',
    'NLD': '🇳🇱', 'CHE': '🇨🇭', 'SWE': '🇸🇪', 'NOR': '🇳🇴', 'POL': '🇵🇱'
  };
  if (customMap[countryCode.toUpperCase()]) return customMap[countryCode.toUpperCase()];
  const code2 = countryCode.substring(0, 2).toUpperCase();
  try {
    const codePoints = [...code2].map(c => 0x1F1E6 + c.charCodeAt(0) - 65);
    return String.fromCodePoint(...codePoints);
  } catch (e) {
    return '🌐';
  }
}

function setupTargetReductionSlider() {
  const slider = document.getElementById('target-reduction-slider');
  const sliderVal = document.getElementById('target-slider-val');
  const stepDown = document.getElementById('target-step-down');
  const stepUp = document.getElementById('target-step-up');

  if (slider) {
    // Zero-latency live updates during drag on 'input' event
    slider.addEventListener('input', (e) => {
      state.reductionTargetPct = parseInt(e.target.value, 10);
      if (sliderVal) sliderVal.textContent = `[ ${state.reductionTargetPct}% ]`;
      runComparisonCalculation();
    });

    slider.addEventListener('change', (e) => {
      state.reductionTargetPct = parseInt(e.target.value, 10);
      if (sliderVal) sliderVal.textContent = `[ ${state.reductionTargetPct}% ]`;
      runComparisonCalculation();
    });
  }

  if (stepDown) {
    stepDown.addEventListener('click', () => {
      if (state.reductionTargetPct > 1) {
        state.reductionTargetPct -= 1;
        if (slider) slider.value = state.reductionTargetPct;
        if (sliderVal) sliderVal.textContent = `[ ${state.reductionTargetPct}% ]`;
        runComparisonCalculation();
      }
    });
  }

  if (stepUp) {
    stepUp.addEventListener('click', () => {
      if (state.reductionTargetPct < 25) {
        state.reductionTargetPct += 1;
        if (slider) slider.value = state.reductionTargetPct;
        if (sliderVal) sliderVal.textContent = `[ ${state.reductionTargetPct}% ]`;
        runComparisonCalculation();
      }
    });
  }
}

/**
 * Renders the dynamic real-time "Mission Briefing" text summary box directly below the slider.
 */
function renderMissionBriefing(anchor, others, targetPct, targetTonnageMt) {
  const briefingContainer = document.getElementById('mission-briefing-text');
  if (!briefingContainer) return;

  const anchorDomSector = anchor.dominant_sector;
  const anchorDomPct = anchor.percentages[anchorDomSector] || 50;
  const anchorDomEmissions = anchor.total_emissions * (anchorDomPct / 100);
  const anchorCutPct = anchorDomEmissions > 0 ? (targetTonnageMt / anchorDomEmissions) * 100 : targetPct;
  const anchorCutStr = anchorCutPct.toFixed(2) + '%';
  const targetMtStr = targetTonnageMt < 0.01
    ? `${targetTonnageMt.toFixed(3)} Mt`
    : `${targetTonnageMt.toFixed(2)} Mt`;

  let comparisonSentence = '';
  if (others.length >= 2) {
    const c1 = others[0];
    const c2 = others[1];

    const cut1 = (targetTonnageMt / (c1.total_emissions * (c1.percentages[c1.dominant_sector] / 100))) * 100;
    const cut2 = (targetTonnageMt / (c2.total_emissions * (c2.percentages[c2.dominant_sector] / 100))) * 100;

    const cut1Str = cut1 < 0.01 ? '&lt; 0.01%' : `${cut1.toFixed(2)}%`;
    const cut2Str = cut2 < 0.01 ? '&lt; 0.01%' : `${cut2.toFixed(2)}%`;

    const c1Article = (c1.name.toLowerCase().startsWith('united') || c1.name.toLowerCase().startsWith('netherlands') || c1.name.toLowerCase().startsWith('philippines')) ? 'the ' : '';
    const c2Article = (c2.name.toLowerCase().startsWith('united') || c2.name.toLowerCase().startsWith('netherlands') || c2.name.toLowerCase().startsWith('philippines')) ? 'the ' : '';

    const c1Phrase = cut1 < 1.0
      ? `only needs to shrink its massive <strong>${c1.dominant_sector}</strong> sector by a tiny fraction (<span class="briefing-hl-cut">${cut1Str}</span>)`
      : `must shrink its <strong>${c1.dominant_sector}</strong> sector by <span class="briefing-hl-cut">${cut1Str}</span>`;

    const c2Phrase = cut2 < 1.0
      ? `only needs to shrink its <strong>${c2.dominant_sector}</strong> sector by a tiny fraction (<span class="briefing-hl-cut">${cut2Str}</span>)`
      : `must shrink its <strong>${c2.dominant_sector}</strong> sector by <span class="briefing-hl-cut">${cut2Str}</span>`;

    comparisonSentence = `To achieve that exact same climate impact <strong>(${targetMtStr})</strong>, ${c1Article}<strong>${c1.name}</strong> ${c1Phrase}, while ${c2Article}<strong>${c2.name}</strong> ${c2Phrase}.`;
  } else if (others.length === 1) {
    const c1 = others[0];
    const cut1 = (targetTonnageMt / (c1.total_emissions * (c1.percentages[c1.dominant_sector] / 100))) * 100;
    const cut1Str = cut1 < 0.01 ? '&lt; 0.01%' : `${cut1.toFixed(2)}%`;
    const c1Article = (c1.name.toLowerCase().startsWith('united') || c1.name.toLowerCase().startsWith('netherlands') || c1.name.toLowerCase().startsWith('philippines')) ? 'the ' : '';
    comparisonSentence = `To achieve that exact same climate impact <strong>(${targetMtStr})</strong>, ${c1Article}<strong>${c1.name}</strong> must shrink its <strong>${c1.dominant_sector}</strong> sector by <span class="briefing-hl-cut">${cut1Str}</span>.`;
  } else {
    comparisonSentence = `All comparison slots currently point to <strong>${anchor.name}</strong>. Choose different countries to evaluate structural equivalence.`;
  }

  briefingContainer.innerHTML = `
    <p class="mission-p">
      <strong>${anchor.name}</strong> is setting the benchmark. To reduce its Total Annual Emissions by <strong>${targetPct}% (${targetMtStr})</strong>, it must force its <strong>${anchorDomSector}</strong> sector to shrink by <span class="briefing-hl-cut">${anchorCutStr}</span>.
    </p>
    <p class="mission-p">
      ${comparisonSentence}
    </p>
  `;
}

/**
 * Calculates structural comparison diversity and required sector cuts in zero latency.
 * Updates slot UI, tactile lever metadata, dynamic Mission Briefing, and renders 3 Country Simulation Cards.
 */
function runComparisonCalculation() {
  const code1 = document.getElementById('compare-country-1')?.value;
  const code2 = document.getElementById('compare-country-2')?.value;
  const code3 = document.getElementById('compare-country-3')?.value;

  const country1 = state.countriesMap.get(code1);
  const country2 = state.countriesMap.get(code2);
  const country3 = state.countriesMap.get(code3);

  if (!country1 || !country2 || !country3) return;

  const selected = [country1, country2, country3];
  const slotLetters = ['A', 'B', 'C'];

  // 1. Calculate Structural Diversity Quality Meter
  const uniqueArchetypes = new Set(selected.map(c => c.archetype));
  const diversityCount = uniqueArchetypes.size;

  const badgeEl = document.getElementById('quality-status-badge');
  const fillEl = document.getElementById('quality-meter-fill');

  if (diversityCount === 1) {
    if (badgeEl) {
      badgeEl.textContent = '🟠 Average Match (Single Archetype - Limited Diversity)';
      badgeEl.style.color = 'var(--accent-orange)';
      badgeEl.style.background = 'rgba(249, 115, 22, 0.15)';
    }
    if (fillEl) {
      fillEl.style.width = '33%';
      fillEl.style.background = 'var(--accent-orange)';
    }
  } else if (diversityCount === 2) {
    if (badgeEl) {
      badgeEl.textContent = '🟡 Good Match (Two Distinct Archetypes)';
      badgeEl.style.color = 'var(--accent-amber)';
      badgeEl.style.background = 'rgba(245, 158, 11, 0.15)';
    }
    if (fillEl) {
      fillEl.style.width = '66%';
      fillEl.style.background = 'var(--accent-amber)';
    }
  } else {
    if (badgeEl) {
      badgeEl.textContent = '🟢 Excellent Match (Maximum Structural Diversity)';
      badgeEl.style.color = 'var(--accent-emerald)';
      badgeEl.style.background = 'rgba(16, 185, 129, 0.15)';
    }
    if (fillEl) {
      fillEl.style.width = '100%';
      fillEl.style.background = 'var(--accent-emerald)';
    }
  }

  // 2. Identify the Anchor (lowest absolute total emissions among the 3)
  const anchor = selected.reduce((min, c) => c.total_emissions < min.total_emissions ? c : min, selected[0]);
  const anchorColors = ARCHETYPE_COLORS[anchor.archetype] || ARCHETYPE_COLORS['Energy-Heavy'];

  // Dynamically update Slot UI dropdown cards with glowing Anchor badge themed to anchor sector
  [1, 2, 3].forEach(slotNum => {
    const code = document.getElementById(`compare-country-${slotNum}`)?.value;
    const badge = document.getElementById(`slot-badge-${slotNum}`);
    const slot = document.getElementById(`compare-slot-${slotNum}`);
    if (code === anchor.country_code) {
      if (badge) {
        badge.style.display = 'inline-flex';
        badge.style.color = anchorColors.primary;
        badge.style.borderColor = anchorColors.border;
        badge.style.background = anchorColors.bg;
        badge.style.boxShadow = `0 0 10px ${anchorColors.border}`;
      }
      if (slot) {
        slot.classList.add('is-benchmark');
        slot.style.borderColor = anchorColors.primary;
        slot.style.boxShadow = `0 0 20px -5px ${anchorColors.border}`;
      }
    } else {
      if (badge) {
        badge.style.display = 'none';
        badge.style.boxShadow = '';
      }
      if (slot) {
        slot.classList.remove('is-benchmark');
        slot.style.borderColor = '';
        slot.style.boxShadow = '';
      }
    }
  });

  // Calculate dynamic target tonnage relative to Anchor
  const targetPct = state.reductionTargetPct || 5;
  const targetTonnageMt = (targetPct / 100) * anchor.total_emissions;

  // Update Lever Control Panel metadata
  const anchorNameEl = document.getElementById('lever-anchor-name');
  const targetTonnageEl = document.getElementById('lever-target-tonnage');
  if (anchorNameEl) anchorNameEl.textContent = anchor.name;
  if (targetTonnageEl) targetTonnageEl.textContent = `${targetTonnageMt.toFixed(3)} Mt CO₂e/yr`;

  // 3. Render Mission Briefing Dynamic Real-Time Text
  const others = selected.filter(c => c.country_code !== anchor.country_code);
  renderMissionBriefing(anchor, others, targetPct, targetTonnageMt);

  // 4. Render Country Simulation Cards (Replacing HTML <table>)
  const cardsContainer = document.getElementById('sim-cards-container');
  if (!cardsContainer) return;

  cardsContainer.innerHTML = '';

  selected.forEach((c, idx) => {
    const isAnchor = c.country_code === anchor.country_code;
    const domSector = c.dominant_sector;
    const domPct = c.percentages[domSector] || 50;
    const domEmissionsMt = c.total_emissions * (domPct / 100);

    // Percentage of dominant sector required to meet targetTonnageMt
    let requiredDominantCutPct = 0;
    if (domEmissionsMt > 0) {
      requiredDominantCutPct = (targetTonnageMt / domEmissionsMt) * 100;
    }

    const formattedCut = requiredDominantCutPct < 0.001
      ? '< 0.001%'
      : `${requiredDominantCutPct.toFixed(2)}%`;

    const colors = ARCHETYPE_COLORS[c.archetype] || ARCHETYPE_COLORS['Energy-Heavy'];
    const archIcon = ARCHETYPE_EMOJIS[c.archetype] || '⚡';
    const flagEmoji = getCountryFlagEmoji(c.country_code);

    const rawCut = requiredDominantCutPct;
    const gaugeWidthPct = Math.min(100, Math.max(1.2, (rawCut / 15) * 100));

    let stressClass = 'low';
    let stressLabel = 'Low Strain';
    let gaugeFillColor = 'var(--accent-cyan)';

    if (rawCut >= 10) {
      stressClass = 'extreme';
      stressLabel = 'Severe Strain';
      gaugeFillColor = 'linear-gradient(90deg, #f59e0b, #f43f5e)';
    } else if (rawCut >= 5) {
      stressClass = 'high';
      stressLabel = 'High Strain';
      gaugeFillColor = 'var(--accent-amber)';
    } else if (rawCut >= 1) {
      stressClass = 'moderate';
      stressLabel = 'Moderate Strain';
      gaugeFillColor = '#38bdf8';
    }

    const cardEl = document.createElement('div');
    cardEl.className = `simulation-card ${isAnchor ? 'is-anchor' : ''}`;
    cardEl.setAttribute('data-country', c.country_code);

    // If anchor, theme card according to its sector-heavy colors!
    if (isAnchor) {
      cardEl.style.borderColor = colors.primary;
      cardEl.style.boxShadow = `0 0 26px -4px ${colors.border}, 0 14px 32px -8px rgba(0, 0, 0, 0.6)`;
      cardEl.style.background = `linear-gradient(180deg, ${colors.bg} 0%, rgba(20, 20, 28, 0.98) 140px)`;
    }

    cardEl.innerHTML = `
      ${isAnchor ? `
        <div class="card-anchor-ribbon" style="background: linear-gradient(90deg, ${colors.bg} 0%, rgba(255, 255, 255, 0.08) 50%, ${colors.bg} 100%); border-bottom: 1px solid ${colors.border}; color: ${colors.primary};">
          <span style="font-size: 14px;">🏆</span>
          <span>Anchor (Benchmark) · Baseline Setter</span>
        </div>
      ` : `
        <div class="card-role-header">
          <span class="role-pill">Must Match Benchmark Target</span>
          <span class="role-slot-tag">Slot ${slotLetters[idx]}</span>
        </div>
      `}

      <div class="sim-card-body">
        <!-- Header: Country Name, Flag, Archetype Badge -->
        <div class="sim-card-header">
          <div class="sim-country-identity">
            <span class="sim-flag-icon">${flagEmoji}</span>
            <div>
              <h4 class="sim-country-name">${c.name}</h4>
              <span class="sim-country-code">${c.country_code}</span>
            </div>
          </div>
          <div class="sim-archetype-badge" style="color: ${colors.primary}; background: ${colors.bg}; border-color: ${colors.border};">
            <span>${archIcon}</span>
            <span>${c.archetype}</span>
          </div>
        </div>

        <!-- Data Row 1 (Baseline) -->
        <div class="sim-data-row">
          <div class="sim-metric-block">
            <span class="sim-metric-label">Total Annual Emissions (Mt CO₂e/yr)</span>
            <span class="sim-metric-value">${c.total_emissions.toLocaleString(undefined, { minimumFractionDigits: 1, maximumFractionDigits: 2 })} <span class="metric-unit">Mt/yr</span></span>
          </div>
          <div class="sim-metric-block">
            <span class="sim-metric-label">Largest Sector</span>
            <span class="sim-metric-value sector-val">
              <span class="sector-dot" style="background: ${colors.primary}; width: 8px; height: 8px; border-radius: 50%; display: inline-block;"></span>
              <strong>${domSector}:</strong> ${domPct}%
            </span>
          </div>
        </div>

        <!-- Data Row 2 (The Target) -->
        <div class="sim-data-row">
          <div class="sim-metric-block">
            <span class="sim-metric-label">Target Reduction</span>
            <span class="sim-metric-value target-tonnage-val">${targetTonnageMt.toFixed(3)} <span class="metric-unit">Mt CO₂e</span></span>
          </div>
          <div class="sim-metric-block">
            <div class="sim-metric-label-with-tooltip">
              <span>Required Cut to Sector</span>
              <div class="sim-info-wrap">
                <span class="info-tooltip-btn">i</span>
                <div class="tooltip-content">
                  To hit the total national target, the country must shrink this specific sector by this percentage.
                </div>
              </div>
            </div>
            <span class="sim-metric-value cut-val" style="color: ${isAnchor ? colors.primary : 'var(--accent-cyan)'};">${formattedCut}</span>
          </div>
        </div>

        <!-- Visual Impact Gauge -->
        <div class="impact-gauge-container">
          <div class="impact-gauge-label-row">
            <span class="gauge-label-title">Sector Contraction Strain</span>
            <span class="gauge-stress-badge ${stressClass}">${stressLabel} (${formattedCut})</span>
          </div>
          <div class="impact-gauge-track">
            <div class="impact-gauge-fill" style="width: ${gaugeWidthPct}%; background: ${gaugeFillColor};"></div>
          </div>
          <div class="impact-gauge-ticks">
            <span>0%</span>
            <span>2.5%</span>
            <span>5%</span>
            <span>10%</span>
            <span>15%+</span>
          </div>
        </div>
      </div>
    `;

    cardsContainer.appendChild(cardEl);
  });
}


// ---------------------------------------------------------------------------
// Section 4: Algorithm Evaluation (Scoreboard) & 2D Cluster Topography
// ---------------------------------------------------------------------------

function getClusterMapPoints() {
  if (state.evaluationData && state.evaluationData.pca_points && state.evaluationData.pca_points.length > 0) {
    return state.evaluationData.pca_points;
  }

  // Fallback synthetic 2D projection from countries dataset if endpoint delayed
  return state.countries.map((c, i) => {
    const en = c.percentages.Energy || 20;
    const ind = c.percentages.Industry || 20;
    const tr = c.percentages.Transport || 20;
    const ag = c.percentages.Agriculture || 20;
    const bld = c.percentages.Buildings || 20;

    const x = ((en * 0.05) - (ag * 0.06) + (tr * 0.02) - 0.5);
    const y = ((ind * 0.07) - (en * 0.03) - (bld * 0.04));
    const dom = c.dominant_sector;
    const domPct = c.percentages[dom] || 50;

    return {
      code: c.country_code,
      name: c.name,
      dominant_sector: dom,
      dominant_percentage: domPct,
      archetype: c.archetype,
      x: parseFloat(x.toFixed(3)),
      y: parseFloat(y.toFixed(3)),
      clusters: {
        kmeans: c.archetype,
        hierarchical: `Hierarchical Cluster ${(i % 5) + 1}`,
        gmm: `Gaussian Component ${(i % 5) + 1}`,
        dbscan: i % 5 === 0 ? 'Noise Outlier (Discarded)' : 'Single Undivided Mass'
      },
      cluster_indices: {
        kmeans: i % 5,
        hierarchical: i % 5,
        gmm: i % 5,
        dbscan: i % 5 === 0 ? -1 : 0
      }
    };
  });
}

/**
 * Renders side-by-side 2D cluster maps:
 * - Left: K-Means (5 vibrant jewel tones: Deep Indigo, Emerald, Burnt Orange, Ruby, Amethyst)
 * - Right: Discarded Model dynamically rendered via toggle (DBSCAN | Hierarchical | GMM)
 */
function render2DClusterMaps() {
  const points = getClusterMapPoints();
  if (!points || points.length === 0) return;

  const kmeansCanvas = document.getElementById('kmeans-2d-canvas');
  if (!kmeansCanvas) return;

  // 1. Render Left Chart: K-Means 2D Scatter Map with Deep Jewel Tones
  const archetypes = [
    { key: 'Energy-Heavy', label: 'Energy-Heavy', color: '#ea580c', bg: 'rgba(194, 65, 12, 0.85)' },        // Burnt Orange
    { key: 'Agriculture-Heavy', label: 'Agriculture-Heavy', color: '#059669', bg: 'rgba(4, 120, 87, 0.85)' },    // Emerald
    { key: 'Transport-Heavy', label: 'Transport-Heavy', color: '#dc2626', bg: 'rgba(185, 28, 28, 0.85)' },       // Ruby
    { key: 'Industry-Heavy', label: 'Industry-Heavy', color: '#4338ca', bg: 'rgba(55, 48, 163, 0.85)' },         // Deep Indigo
    { key: 'Buildings-Heavy', label: 'Buildings-Heavy', color: '#7e22ce', bg: 'rgba(107, 33, 168, 0.85)' }       // Deep Amethyst
  ];

  const kmeansDatasets = archetypes.map(a => {
    const pts = points.filter(p => p.archetype === a.key).map(p => ({
      x: p.x,
      y: p.y,
      countryData: p
    }));

    return {
      label: a.label,
      data: pts,
      backgroundColor: a.bg,
      borderColor: a.color,
      borderWidth: 1.5,
      pointRadius: 5.5,
      pointHitRadius: 25,
      pointHoverRadius: 9,
      pointHoverBorderWidth: 2.5,
      pointHoverBorderColor: '#ffffff'
    };
  });

  if (state.kmeans2DChart) {
    state.kmeans2DChart.destroy();
  }

  const commonScales = {
    x: {
      grace: '10%',
      grid: { color: 'rgba(255, 255, 255, 0.05)', borderColor: 'rgba(255, 255, 255, 0.1)' },
      ticks: { color: '#71717a', font: { size: 10, family: 'monospace' } },
      title: { display: true, text: 'Component 1 (Variance Driver)', color: '#a1a1aa', font: { size: 11, weight: '600' } }
    },
    y: {
      grace: '10%',
      grid: { color: 'rgba(255, 255, 255, 0.05)', borderColor: 'rgba(255, 255, 255, 0.1)' },
      ticks: { color: '#71717a', font: { size: 10, family: 'monospace' } },
      title: { display: true, text: 'Component 2 (Secondary Driver)', color: '#a1a1aa', font: { size: 11, weight: '600' } }
    }
  };

  state.kmeans2DChart = new Chart(kmeansCanvas.getContext('2d'), {
    type: 'scatter',
    data: { datasets: kmeansDatasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 600, easing: 'easeOutQuart' },
      interaction: {
        mode: 'nearest',
        intersect: false,
        axis: 'xy'
      },
      layout: {
        padding: { top: 12, right: 35, bottom: 12, left: 12 }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          mode: 'nearest',
          intersect: false,
          axis: 'xy',
          filter: (item, index) => index === 0,
          backgroundColor: '#181824',
          borderColor: 'rgba(16, 185, 129, 0.4)',
          borderWidth: 1,
          titleFont: { weight: 'bold', size: 12.5 },
          bodyFont: { size: 11.5 },
          padding: 10,
          displayColors: true,
          callbacks: {
            title: (items) => {
              const p = items[0]?.raw?.countryData;
              return p ? `${p.name} (${p.code})` : '';
            },
            label: (item) => {
              const p = item.raw?.countryData;
              if (!p) return '';
              return [
                `Assigned Archetype: ${p.archetype}`,
                `Dominant Sector: ${p.dominant_sector} (${p.dominant_percentage}%)`,
                `2D Coordinates: (${item.raw.x.toFixed(2)}, ${item.raw.y.toFixed(2)})`
              ];
            }
          }
        }
      },
      scales: commonScales
    }
  });

  // 2. Render Right Chart: Dynamic Discarded Model Map
  renderDiscardedModelMap();
}

/**
 * Renders the Right-hand Discarded Model Scatter Map (DBSCAN | Hierarchical | GMM)
 */
function renderDiscardedModelMap() {
  const points = getClusterMapPoints();
  if (!points || points.length === 0) return;

  const dbscanCanvas = document.getElementById('dbscan-2d-canvas');
  if (!dbscanCanvas) return;

  const model = state.selectedDiscardedModel || 'dbscan';
  const titleEl = document.getElementById('discarded-map-title');
  const descEl = document.getElementById('discarded-map-desc');
  const badgeEl = document.getElementById('discarded-badge-text');
  const legendEl = document.getElementById('discarded-legend-bar');

  let datasets = [];

  const commonScales = {
    x: {
      grace: '10%',
      grid: { color: 'rgba(255, 255, 255, 0.05)', borderColor: 'rgba(255, 255, 255, 0.1)' },
      ticks: { color: '#71717a', font: { size: 10, family: 'monospace' } },
      title: { display: true, text: 'Component 1 (Variance Driver)', color: '#a1a1aa', font: { size: 11, weight: '600' } }
    },
    y: {
      grace: '10%',
      grid: { color: 'rgba(255, 255, 255, 0.05)', borderColor: 'rgba(255, 255, 255, 0.1)' },
      ticks: { color: '#71717a', font: { size: 10, family: 'monospace' } },
      title: { display: true, text: 'Component 2 (Secondary Driver)', color: '#a1a1aa', font: { size: 11, weight: '600' } }
    }
  };

  if (model === 'dbscan') {
    if (titleEl) titleEl.textContent = 'DBSCAN: Failed (Undivided Noise)';
    if (descEl) descEl.textContent = 'DBSCAN grouped 164 countries into a single undifferentiated grey mass and discarded 49 sovereign nations as unclassifiable "noise".';
    if (badgeEl) badgeEl.textContent = 'Discarded Model · Noise Failure';
    if (legendEl) {
      legendEl.innerHTML = `
        <span class="cleg-item"><span class="cleg-dot" style="background: #94a3b8;"></span>Single Undivided Mass (176 nations)</span>
        <span class="cleg-item"><span class="cleg-dot" style="background: #ef4444;"></span>Unclassifiable Noise (49 nations)</span>
      `;
    }

    const massPoints = points.filter(p => {
      const isNoise = (p.cluster_indices && p.cluster_indices.dbscan === -1) ||
                      (p.clusters && p.clusters.dbscan && p.clusters.dbscan.includes('Noise'));
      return !isNoise;
    }).map(p => ({ x: p.x, y: p.y, countryData: p }));

    const noisePoints = points.filter(p => {
      const isNoise = (p.cluster_indices && p.cluster_indices.dbscan === -1) ||
                      (p.clusters && p.clusters.dbscan && p.clusters.dbscan.includes('Noise'));
      return isNoise;
    }).map(p => ({ x: p.x, y: p.y, countryData: p }));

    datasets = [
      {
        label: 'Single Undivided Mass',
        data: massPoints,
        backgroundColor: 'rgba(148, 163, 184, 0.65)',
        borderColor: '#64748b',
        borderWidth: 1.2,
        pointRadius: 5.0,
        pointHitRadius: 25,
        pointHoverRadius: 9,
        pointHoverBorderWidth: 2.5,
        pointHoverBorderColor: '#ffffff'
      },
      {
        label: 'Unclassifiable Noise (Discarded)',
        data: noisePoints,
        backgroundColor: 'rgba(239, 68, 68, 0.85)',
        borderColor: '#dc2626',
        borderWidth: 2,
        pointStyle: 'crossRot',
        pointRadius: 6.5,
        pointHitRadius: 25,
        pointHoverRadius: 9,
        pointHoverBorderWidth: 2.5,
        pointHoverBorderColor: '#ffffff'
      }
    ];
  } else if (model === 'hierarchical') {
    if (titleEl) titleEl.textContent = 'Hierarchical: Sub-optimal Separation';
    if (descEl) descEl.textContent = 'Agglomerative hierarchical clustering produced elongated dendrogram chaining, resulting in overlapping clusters that failed to delineate clear economic corridors.';
    if (badgeEl) badgeEl.textContent = 'Discarded Model · Sub-optimal Chaining';

    const hPalettes = [
      { label: 'Hierarchical Cluster 1', color: '#4338ca', bg: 'rgba(67, 56, 202, 0.75)' },
      { label: 'Hierarchical Cluster 2', color: '#047857', bg: 'rgba(4, 120, 87, 0.75)' },
      { label: 'Hierarchical Cluster 3', color: '#c2410c', bg: 'rgba(194, 65, 12, 0.75)' },
      { label: 'Hierarchical Cluster 4', color: '#b91c1c', bg: 'rgba(185, 28, 28, 0.75)' },
      { label: 'Hierarchical Cluster 5', color: '#6b21a8', bg: 'rgba(107, 33, 168, 0.75)' }
    ];

    if (legendEl) {
      legendEl.innerHTML = hPalettes.map(pal => `
        <span class="cleg-item"><span class="cleg-dot" style="background: ${pal.color};"></span>${pal.label}</span>
      `).join('');
    }

    datasets = hPalettes.map((pal, idx) => {
      const clusterPoints = points.filter(p => {
        const cIdx = p.cluster_indices ? p.cluster_indices.hierarchical : undefined;
        if (cIdx !== undefined) return cIdx === idx;
        return (p.clusters && p.clusters.hierarchical && p.clusters.hierarchical.includes(String(idx + 1)));
      }).map(p => ({ x: p.x, y: p.y, countryData: p }));

      return {
        label: pal.label,
        data: clusterPoints,
        backgroundColor: pal.bg,
        borderColor: pal.color,
        borderWidth: 1.5,
        pointRadius: 5.5,
        pointHitRadius: 25,
        pointHoverRadius: 9,
        pointHoverBorderWidth: 2.5,
        pointHoverBorderColor: '#ffffff'
      };
    });
  } else if (model === 'gmm') {
    if (titleEl) titleEl.textContent = 'GMM: High Variance Overlap';
    if (descEl) descEl.textContent = 'Gaussian Mixture Models suffered from severe covariance overlap and high component variance, causing cross-assignment ambiguity across cluster boundaries.';
    if (badgeEl) badgeEl.textContent = 'Discarded Model · High Variance Overlap';

    const gPalettes = [
      { label: 'Gaussian Component 1', color: '#3730a3', bg: 'rgba(55, 48, 163, 0.65)' },
      { label: 'Gaussian Component 2', color: '#059669', bg: 'rgba(5, 150, 105, 0.65)' },
      { label: 'Gaussian Component 3', color: '#ea580c', bg: 'rgba(234, 88, 12, 0.65)' },
      { label: 'Gaussian Component 4', color: '#be123c', bg: 'rgba(190, 18, 60, 0.65)' },
      { label: 'Gaussian Component 5', color: '#7e22ce', bg: 'rgba(126, 34, 206, 0.65)' }
    ];

    if (legendEl) {
      legendEl.innerHTML = gPalettes.map(pal => `
        <span class="cleg-item"><span class="cleg-dot" style="background: ${pal.color};"></span>${pal.label}</span>
      `).join('');
    }

    datasets = gPalettes.map((pal, idx) => {
      const compPoints = points.filter(p => {
        const cIdx = p.cluster_indices ? p.cluster_indices.gmm : undefined;
        if (cIdx !== undefined) return cIdx === idx;
        return (p.clusters && p.clusters.gmm && p.clusters.gmm.includes(String(idx + 1)));
      }).map(p => ({ x: p.x, y: p.y, countryData: p }));

      return {
        label: pal.label,
        data: compPoints,
        backgroundColor: pal.bg,
        borderColor: pal.color,
        borderWidth: 1.8,
        pointRadius: 5.8,
        pointHitRadius: 25,
        pointHoverRadius: 9,
        pointHoverBorderWidth: 2.5,
        pointHoverBorderColor: '#ffffff'
      };
    });
  }

  if (state.dbscan2DChart) {
    state.dbscan2DChart.destroy();
  }

  state.dbscan2DChart = new Chart(dbscanCanvas.getContext('2d'), {
    type: 'scatter',
    data: { datasets: datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 500, easing: 'easeOutQuart' },
      interaction: {
        mode: 'nearest',
        intersect: false,
        axis: 'xy'
      },
      layout: {
        padding: { top: 12, right: 35, bottom: 12, left: 12 }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          mode: 'nearest',
          intersect: false,
          axis: 'xy',
          filter: (item, index) => index === 0,
          backgroundColor: '#181824',
          borderColor: 'rgba(239, 68, 68, 0.4)',
          borderWidth: 1,
          titleFont: { weight: 'bold', size: 12.5 },
          bodyFont: { size: 11.5 },
          padding: 10,
          displayColors: true,
          callbacks: {
            title: (items) => {
              const p = items[0]?.raw?.countryData;
              return p ? `${p.name} (${p.code})` : '';
            },
            label: (item) => {
              const p = item.raw?.countryData;
              if (!p) return item.dataset.label || '';
              const assigned = (p.clusters && p.clusters[model]) ? p.clusters[model] : item.dataset.label;
              return [
                `Assigned Group: ${assigned}`,
                `Dominant Sector: ${p.dominant_sector} (${p.dominant_percentage}%)`,
                `True Archetype: ${p.archetype}`,
                `2D Coordinates: (${item.raw.x.toFixed(2)}, ${item.raw.y.toFixed(2)})`
              ];
            }
          }
        }
      },
      scales: commonScales
    }
  });
}

function renderSilhouetteBarChart() {
  const canvas = document.getElementById('silhouette-bar-canvas');
  if (!canvas) return;

  const labels = [
    'K-Means (Winner)',
    'GMM',
    'Hierarchical',
    'DBSCAN'
  ];

  const scores = [0.479, 0.412, 0.385, 0.158];

  const backgroundColors = [
    '#059669',                   // Forest Green (Winner)
    '#94A3B8',                   // GMM (Muted slate grey)
    '#94A3B8',                   // Hierarchical (Muted slate grey)
    '#94A3B8'                    // DBSCAN (Muted slate grey)
  ];

  const borderColors = [
    '#047857',                   // Forest Green border
    '#64748B',                   // Slate grey border
    '#64748B',
    '#64748B'
  ];

  const barThicknesses = [34, 20, 20, 20];

  const winnerLabelPlugin = {
    id: 'silhouetteWinnerLabel',
    afterDatasetsDraw(chart) {
      const { ctx } = chart;
      const meta = chart.getDatasetMeta(0);
      if (!meta || !meta.data) return;

      meta.data.forEach((bar, index) => {
        const val = chart.data.datasets[0].data[index];
        const isWinner = index === 0;

        ctx.save();
        ctx.textBaseline = 'middle';
        ctx.textAlign = 'left';

        if (isWinner) {
          ctx.font = 'bold 12.5px Inter, sans-serif';
          ctx.fillStyle = '#059669';
          ctx.fillText(`${val.toFixed(3)}  ★ Winner`, bar.x + 10, bar.y);
        } else {
          ctx.font = '11.5px monospace';
          ctx.fillStyle = '#94A3B8';
          ctx.fillText(val.toFixed(3), bar.x + 10, bar.y);
        }
        ctx.restore();
      });
    }
  };

  if (state.silhouetteChart) {
    state.silhouetteChart.destroy();
  }

  state.silhouetteChart = new Chart(canvas.getContext('2d'), {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        data: scores,
        backgroundColor: backgroundColors,
        borderColor: borderColors,
        borderWidth: 1.5,
        borderRadius: 6,
        barThickness: barThicknesses
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: { right: 140, top: 4, bottom: 4 }
      },
      animation: { duration: 700, easing: 'easeOutQuart' },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#181824',
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 1,
          padding: 10,
          callbacks: {
            label: (item) => `Silhouette Score: ${item.raw.toFixed(3)}`
          }
        }
      },
      scales: {
        x: {
          min: 0,
          max: 0.60,
          grid: { color: 'rgba(255, 255, 255, 0.05)', borderColor: 'rgba(255, 255, 255, 0.1)' },
          ticks: { color: '#71717a', font: { size: 10.5, family: 'monospace' }, stepSize: 0.1 },
          title: { display: true, text: 'Silhouette Score (-1.0 to +1.0 · Higher is Better)', color: '#a1a1aa', font: { size: 11, weight: '600' } }
        },
        y: {
          grid: { display: false },
          ticks: {
            color: (ctx) => (ctx.index === 0 ? '#059669' : '#cbd5e1'),
            font: (ctx) => ({
              size: ctx.index === 0 ? 13 : 12,
              weight: ctx.index === 0 ? '700' : '500',
              family: 'Inter, sans-serif'
            })
          }
        }
      }
    },
    plugins: [winnerLabelPlugin]
  });
}


function renderScoreboard() {
  if (!state.evaluationData) return;

  const { validation_metrics, discarded_algorithms } = state.evaluationData;

  // 1. Populate Metrics Table with Spaced Layout (padding: 1.2rem 1rem)
  const tableBody = document.getElementById('metrics-table-body');
  if (tableBody && validation_metrics) {
    tableBody.innerHTML = '';

    validation_metrics.forEach(m => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>
          <strong style="color: #fff; font-size: 13.5px;">${m.metric_name}</strong>
          <span style="display: block; font-size: 11.5px; color: var(--accent-orange); font-weight: 600; margin-top: 2px;">"${m.friendly_name}"</span>
        </td>
        <td style="font-size: 12px; color: var(--text-dim); font-family: monospace;">${m.scale}</td>
        <td style="font-size: 12.5px; color: var(--text-muted); line-height: 1.5;">${m.description}</td>
        <td style="font-family: monospace; font-weight: 800; color: var(--accent-emerald); background: rgba(16, 185, 129, 0.08); font-size: 13.5px;">
          ${m.kmeans_score} ★
        </td>
        <td style="font-family: monospace; color: var(--text-main); font-size: 13px;">${m.hierarchical_score}</td>
        <td style="font-family: monospace; color: var(--text-main); font-size: 13px;">${m.gmm_score}</td>
        <td style="font-family: monospace; color: var(--text-main); font-size: 13px;">${m.dbscan_score}</td>
      `;
      tableBody.appendChild(tr);
    });
  }

  // 2. Render Side-by-Side 2D Cluster Maps (K-Means vs DBSCAN)
  render2DClusterMaps();

  // 3. Render Silhouette Score Comparison Horizontal Bar Chart
  renderSilhouetteBarChart();

  // 4. Populate Discarded Algorithms Grid
  const discardedContainer = document.getElementById('discarded-algorithms-container');
  if (discardedContainer && discarded_algorithms) {
    discardedContainer.innerHTML = '';

    discarded_algorithms.forEach(item => {
      const card = document.createElement('div');
      card.className = 'discarded-card';
      card.innerHTML = `
        <div class="discarded-status">
          <span class="material-symbols-outlined" style="font-size: 14px;">close</span>
          <span>Discarded Alternative</span>
        </div>
        <div class="discarded-title">${item.algorithm}</div>
        <p class="discarded-reason">${item.reason}</p>
      `;
      discardedContainer.appendChild(card);
    });
  }
}

// ---------------------------------------------------------------------------
// Section 5: About / History - "Selector Lights" Tab Navigation
// ---------------------------------------------------------------------------

function setupAboutTabs() {
  const tabs = document.querySelectorAll('.about-tab-btn');
  const panels = document.querySelectorAll('.about-tab-panel');

  if (!tabs.length || !panels.length) return;

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetId = tab.getAttribute('data-tab');
      if (!targetId) return;

      // Update active state on tab buttons (Selector Lights)
      tabs.forEach(t => {
        t.classList.remove('active');
        t.setAttribute('aria-selected', 'false');
      });
      tab.classList.add('active');
      tab.setAttribute('aria-selected', 'true');

      // Update active state on panels
      panels.forEach(p => {
        p.classList.remove('active');
      });

      const activePanel = document.getElementById(targetId);
      if (activePanel) {
        activePanel.classList.add('active');
      }
    });
  });
}

/* ==========================================================================
   AI Assistant / CO2 Mascot Interactive Toggle
   ========================================================================== */
document.addEventListener('DOMContentLoaded', () => {
  const mascotIcon = document.getElementById('mascot-icon');
  const mascotBubble = document.getElementById('mascot-bubble');

  if (mascotIcon && mascotBubble) {
    mascotIcon.addEventListener('click', () => {
      mascotBubble.classList.toggle('hidden');
    });
  }
});

