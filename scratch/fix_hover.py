import re

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Let's inspect render2DClusterMaps and renderDiscardedModelMap
# We will enhance:
# 1. commonScales with grace: '8%'
# 2. pointHitRadius: 15 on all scatter datasets
# 3. interaction: { mode: 'nearest', intersect: false, axis: 'xy' }
# 4. layout: { padding: { top: 12, right: 30, bottom: 12, left: 12 } }

old_common_scales = """  const commonScales = {
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
  };"""

new_common_scales = """  const commonScales = {
    x: {
      grace: '8%',
      grid: { color: 'rgba(255, 255, 255, 0.05)', borderColor: 'rgba(255, 255, 255, 0.1)' },
      ticks: { color: '#71717a', font: { size: 10, family: 'monospace' } },
      title: { display: true, text: 'Component 1 (Variance Driver)', color: '#a1a1aa', font: { size: 11, weight: '600' } }
    },
    y: {
      grace: '8%',
      grid: { color: 'rgba(255, 255, 255, 0.05)', borderColor: 'rgba(255, 255, 255, 0.1)' },
      ticks: { color: '#71717a', font: { size: 10, family: 'monospace' } },
      title: { display: true, text: 'Component 2 (Secondary Driver)', color: '#a1a1aa', font: { size: 11, weight: '600' } }
    }
  };"""

js = js.replace(old_common_scales, new_common_scales)

# Add pointHitRadius: 15 to pointRadius definitions
js = js.replace('pointRadius: 5.5,', 'pointRadius: 5.5,\n      pointHitRadius: 15,')
js = js.replace('pointRadius: 4.8,', 'pointRadius: 4.8,\n        pointHitRadius: 15,')
js = js.replace('pointRadius: 6.5,', 'pointRadius: 6.5,\n        pointHitRadius: 15,')
js = js.replace('pointRadius: 5.2,', 'pointRadius: 5.2,\n        pointHitRadius: 15,')
js = js.replace('pointRadius: 5.8,', 'pointRadius: 5.8,\n        pointHitRadius: 15,')

# Add interaction and layout padding to kmeans2DChart options
kmeans_old_options = """    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 600, easing: 'easeOutQuart' },"""

kmeans_new_options = """    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 600, easing: 'easeOutQuart' },
      interaction: {
        mode: 'nearest',
        intersect: false,
        axis: 'xy'
      },
      layout: {
        padding: { top: 12, right: 30, bottom: 12, left: 12 }
      },"""

js = js.replace(kmeans_old_options, kmeans_new_options)

# Add interaction and layout padding to dbscan2DChart options
dbscan_old_options = """    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 500, easing: 'easeOutQuart' },"""

dbscan_new_options = """    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 500, easing: 'easeOutQuart' },
      interaction: {
        mode: 'nearest',
        intersect: false,
        axis: 'xy'
      },
      layout: {
        padding: { top: 12, right: 30, bottom: 12, left: 12 }
      },"""

js = js.replace(dbscan_old_options, dbscan_new_options)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)
with open('frontend/script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Hover and scale padding enhancements applied successfully!")

