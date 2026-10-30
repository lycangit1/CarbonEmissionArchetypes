import re

# 1. Update style.css and frontend/style.css
for path in ['style.css', 'frontend/style.css']:
    with open(path, 'r', encoding='utf-8') as f:
        css = f.read()
    
    # Ensure .mascot-container has pointer-events: none !important
    css = re.sub(
        r'\.mascot-container\s*\{[^}]*\}',
        '''.mascot-container {
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 15px;
    pointer-events: none !important;
}''',
        css
    )
    
    # Ensure .mascot-bubble.hidden has display: none !important
    css = re.sub(
        r'\.mascot-bubble\.hidden\s*\{[^}]*\}',
        '''.mascot-bubble.hidden {
    display: none !important;
    opacity: 0;
    transform: translateY(20px) scale(0.9);
    pointer-events: none !important;
}''',
        css
    )
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(css)
    print(f'Updated {path}')

# 2. Update index.html and frontend/index.html
for path in ['index.html', 'frontend/index.html']:
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Cache busters
    html = re.sub(r'style\.css\?v=[^"]+', 'style.css?v=20261030_v4', html)
    html = re.sub(r'script\.js\?v=[^"]+', 'script.js?v=20261030_v4', html)
    
    # Fix stray question mark in discarded badge text
    html = re.sub(
        r'<span id="discarded-badge-text">[^<]+</span>',
        '<span id="discarded-badge-text">Discarded Model · Noise Failure</span>',
        html
    )
    
    # Add inline pointer-events: none fail-safe to mascot container
    html = html.replace(
        '<div id="mascot-container" class="mascot-container">',
        '<div id="mascot-container" class="mascot-container" style="pointer-events: none;">'
    )
    html = html.replace(
        '<div id="mascot-bubble" class="mascot-bubble hidden">',
        '<div id="mascot-bubble" class="mascot-bubble hidden" style="display: none;">'
    )
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Updated {path}')

# 3. Update script.js and frontend/script.js to enhance tooltips, pointHitRadius, and filter
for path in ['script.js', 'frontend/script.js']:
    with open(path, 'r', encoding='utf-8') as f:
        js = f.read()
    
    # Increase pointHitRadius: 20 to 25 for even smoother hover response
    js = js.replace('pointHitRadius: 20', 'pointHitRadius: 25')
    
    # In kmeans tooltip options, add filter: (item, index) => index === 0
    old_kmeans_tooltip = '''        tooltip: {
          mode: 'nearest',
          intersect: false,
          axis: 'xy','''
    new_kmeans_tooltip = '''        tooltip: {
          mode: 'nearest',
          intersect: false,
          axis: 'xy',
          filter: (item, index) => index === 0,'''
    if old_kmeans_tooltip in js and 'filter: (item, index) => index === 0' not in js:
        js = js.replace(old_kmeans_tooltip, new_kmeans_tooltip)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(js)
    print(f'Updated {path}')

print("All files updated successfully!")

