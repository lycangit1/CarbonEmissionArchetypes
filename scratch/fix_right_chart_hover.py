import re

# 1. Update style.css & frontend/style.css for mascot
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace .mascot-container
old_mascot_container = """.mascot-container {
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 15px;
}"""

new_mascot_container = """.mascot-container {
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 15px;
    pointer-events: none;
}

.mascot-icon {
    pointer-events: auto;
}

.mascot-bubble {
    pointer-events: auto;
}"""

if old_mascot_container in css:
    css = css.replace(old_mascot_container, new_mascot_container)

old_bubble_hidden = """.mascot-bubble.hidden {
    opacity: 0;
    transform: translateY(20px) scale(0.9);
    pointer-events: none;
}"""

new_bubble_hidden = """.mascot-bubble.hidden {
    display: none !important;
    opacity: 0;
    transform: translateY(20px) scale(0.9);
    pointer-events: none !important;
}"""

if old_bubble_hidden in css:
    css = css.replace(old_bubble_hidden, new_bubble_hidden)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)
with open('frontend/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("style.css updated!")

# 2. Update index.html cache-buster
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
html = re.sub(r'script\.js\?v=[^"]+', 'script.js?v=20261030_v3', html)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("index.html cache-buster updated!")

# 3. Update script.js & frontend/script.js
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Let's rebuild the entire render2DClusterMaps and renderDiscardedModelMap cleanly with full parity to Image 4
new_render_code = '''/**
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
      pointHitRadius: 20,
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
        pointHitRadius: 20,
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
        pointHitRadius: 20,
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
        pointHitRadius: 20,
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
        pointHitRadius: 20,
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
}'''

# Replace block in script.js
start_marker = "/**\n * Renders side-by-side 2D cluster maps:"
end_marker = "function renderSilhouetteBarChart() {"

start_idx = js.find(start_marker)
end_idx = js.find(end_marker)

assert start_idx != -1, f"Could not find start_marker '{start_marker}'"
assert end_idx != -1, f"Could not find end_marker '{end_marker}'"

js = js[:start_idx] + new_render_code + "\n\n" + js[end_idx:]

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)
with open('frontend/script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("script.js updated with exact Image 4 tooltip formatting and full parity!")

