import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Add selectedDiscardedModel to state
if 'selectedDiscardedModel' not in js:
    js = js.replace('reductionTargetPct: 5', 'reductionTargetPct: 5,\n  selectedDiscardedModel: "dbscan"')

# 2. Add setupDiscardedModelToggles() call to DOMContentLoaded
if 'setupDiscardedModelToggles();' not in js:
    js = js.replace('setupAboutTabs();', 'setupAboutTabs();\n  setupDiscardedModelToggles();')

# 3. Add setupDiscardedModelToggles definition
setup_toggles_fn = '''
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
'''
if 'function setupDiscardedModelToggles()' not in js:
    js = js.replace('function setupNavigation()', setup_toggles_fn + '\nfunction setupNavigation()')

# 4. Update getClusterMapPoints fallback
old_fallback = '''      clusters: {
        kmeans: c.archetype,
        dbscan: i % 5 === 0 ? 'Noise Outlier (Discarded)' : 'Single Undivided Mass'
      },
      cluster_indices: {
        kmeans: i % 5,
        dbscan: i % 5 === 0 ? -1 : 0
      }'''

new_fallback = '''      clusters: {
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
      }'''

if old_fallback in js:
    js = js.replace(old_fallback, new_fallback)

# 5. New render2DClusterMaps, renderDiscardedModelMap, and renderSilhouetteBarChart
new_render_section = '''/**
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
      pointHoverRadius: 8,
      pointHoverBorderWidth: 2,
      pointHoverBorderColor: '#ffffff'
    };
  });

  if (state.kmeans2DChart) {
    state.kmeans2DChart.destroy();
  }

  const commonScales = {
    x: {
      grid: { color: 'rgba(255, 255, 255, 0.05)', borderColor: 'rgba(255, 255, 255, 0.1)' },
      ticks: { color: '#71717a', font: { size: 10, family: 'monospace' } },
      title: { display: true, text: 'Component 1 (Variance Driver)', color: '#a1a1aa', font: { size: 11, weight: '600' } }
    },
    y: {
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
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#181824',
          borderColor: 'rgba(16, 185, 129, 0.4)',
          borderWidth: 1,
          titleFont: { weight: 'bold', size: 12 },
          bodyFont: { size: 11.5 },
          padding: 10,
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
      grid: { color: 'rgba(255, 255, 255, 0.05)', borderColor: 'rgba(255, 255, 255, 0.1)' },
      ticks: { color: '#71717a', font: { size: 10, family: 'monospace' } },
      title: { display: true, text: 'Component 1 (Variance Driver)', color: '#a1a1aa', font: { size: 11, weight: '600' } }
    },
    y: {
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
        pointRadius: 4.8,
        pointHoverRadius: 7
      },
      {
        label: 'Unclassifiable Noise (Discarded)',
        data: noisePoints,
        backgroundColor: 'rgba(239, 68, 68, 0.85)',
        borderColor: '#dc2626',
        borderWidth: 2,
        pointStyle: 'crossRot',
        pointRadius: 6.5,
        pointHoverRadius: 8.5
      }
    ];
  } else if (model === 'hierarchical') {
    if (titleEl) titleEl.textContent = 'Hierarchical: Sub-optimal Separation';
    if (descEl) descEl.textContent = 'Agglomerative hierarchical clustering produced elongated dendrogram chaining, resulting in overlapping clusters that failed to delineate clear economic corridors.';
    if (badgeEl) badgeEl.textContent = 'Discarded Model · Sub-optimal Chaining';

    const hPalettes = [
      { label: 'Hierarchical Cluster 1', color: '#4338ca', bg: 'rgba(67, 56, 202, 0.65)' },
      { label: 'Hierarchical Cluster 2', color: '#047857', bg: 'rgba(4, 120, 87, 0.65)' },
      { label: 'Hierarchical Cluster 3', color: '#c2410c', bg: 'rgba(194, 65, 12, 0.65)' },
      { label: 'Hierarchical Cluster 4', color: '#b91c1c', bg: 'rgba(185, 28, 28, 0.65)' },
      { label: 'Hierarchical Cluster 5', color: '#6b21a8', bg: 'rgba(107, 33, 168, 0.65)' }
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
        pointRadius: 5.2,
        pointHoverRadius: 7.5
      };
    });
  } else if (model === 'gmm') {
    if (titleEl) titleEl.textContent = 'GMM: High Variance Overlap';
    if (descEl) descEl.textContent = 'Gaussian Mixture Models suffered from severe covariance overlap and high component variance, causing cross-assignment ambiguity across cluster boundaries.';
    if (badgeEl) badgeEl.textContent = 'Discarded Model · High Variance Overlap';

    const gPalettes = [
      { label: 'Gaussian Component 1', color: '#3730a3', bg: 'rgba(55, 48, 163, 0.55)' },
      { label: 'Gaussian Component 2', color: '#059669', bg: 'rgba(5, 150, 105, 0.55)' },
      { label: 'Gaussian Component 3', color: '#ea580c', bg: 'rgba(234, 88, 12, 0.55)' },
      { label: 'Gaussian Component 4', color: '#be123c', bg: 'rgba(190, 18, 60, 0.55)' },
      { label: 'Gaussian Component 5', color: '#7e22ce', bg: 'rgba(126, 34, 206, 0.55)' }
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
        pointHoverRadius: 8
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
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#181824',
          borderColor: 'rgba(239, 68, 68, 0.4)',
          borderWidth: 1,
          titleFont: { weight: 'bold', size: 12 },
          bodyFont: { size: 11.5 },
          padding: 10,
          callbacks: {
            title: (items) => {
              const p = items[0]?.raw?.countryData;
              return p ? `${p.name} (${p.code})` : '';
            },
            label: (item) => {
              const p = item.raw?.countryData;
              if (!p) return '';
              const assigned = (p.clusters && p.clusters[model]) ? p.clusters[model] : item.dataset.label;
              return [
                `Evaluated Model: ${model.toUpperCase()}`,
                `Assigned Cluster: ${assigned}`,
                `Dominant Sector: ${p.dominant_sector} (${p.dominant_percentage}%)`,
                `True Archetype: ${p.archetype}`
              ];
            }
          }
        }
      },
      scales: commonScales
    }
  });
}

/**
 * Renders the Silhouette Score Comparison Horizontal Bar Chart:
 * - K-Means: 0.479 (Winner) - Thick, Forest Green (#059669)
 * - GMM: 0.412 - Muted slate grey (#94A3B8)
 * - Hierarchical: 0.385 - Muted slate grey (#94A3B8)
 * - DBSCAN: 0.158 - Muted slate grey (#94A3B8)
 */
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
'''

# Find the start of render2DClusterMaps to the end of renderSilhouetteBarChart
start_marker = "/**\n * Renders side-by-side 2D cluster maps:"
end_marker = "function renderScoreboard() {"

start_idx = js.find(start_marker)
end_idx = js.find(end_marker)

assert start_idx != -1, f"Could not find start_marker '{start_marker}'"
assert end_idx != -1, f"Could not find end_marker '{end_marker}'"

js = js[:start_idx] + new_render_section + "\n\n" + js[end_idx:]

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)
with open('frontend/script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Successfully replaced render logic in script.js and frontend/script.js!")

