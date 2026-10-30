import re
import os

# 1. Patch shared.css: Change .scene-canvas to #root
with open('brag-output/composition/shared.css', 'r', encoding='utf-8') as f:
    css = f.read()
css = css.replace('.scene-canvas', '#root')
with open('brag-output/composition/shared.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("Updated shared.css")

# 2. Patch index.html
font_links = '''    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700;800&display=swap"
      rel="stylesheet"
    />'''

with open('brag-output/composition/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace slots to have stable id and data-composition-id
slots = [
    ('scene1', 'scene1-intro.html', 0, 22.5),
    ('scene2', 'scene2-clr.html', 22.5, 26.5),
    ('scene3', 'scene3-archetypes.html', 49.0, 28.0),
    ('scene4', 'scene4-baseline.html', 77.0, 23.0),
    ('scene5', 'scene5-whatif.html', 100.0, 25.0),
    ('scene6', 'scene6-benchmark.html', 125.0, 26.5),
    ('scene7', 'scene7-conclusion.html', 151.5, 15.0),
]

for s_id, s_file, s_start, s_dur in slots:
    old_slot_pattern = rf'<div\s+class="scene-slot"\s+data-composition-src="compositions/{s_file}"\s+data-start="{s_start}"\s+data-duration="{s_dur}"\s+data-track-index="9"\s*></div>'
    new_slot = f'<div id="slot-{s_id}" class="scene-slot" data-composition-id="{s_id}" data-composition-src="compositions/{s_file}" data-start="{s_start}" data-duration="{s_dur}" data-track-index="9"></div>'
    html = re.sub(old_slot_pattern, new_slot, html)

with open('brag-output/composition/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html")

# 3. Patch each subcomposition
comp_dir = 'brag-output/composition/compositions'
for fname in os.listdir(comp_dir):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(comp_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add Google Fonts link if missing
    if 'fonts.googleapis.com' not in content:
        content = content.replace('<head>', f'<head>\n{font_links}')
    
    # Replace root class="scene-canvas" with id="root"
    content = re.sub(r'<div data-composition-id="(\w+)" class="scene-canvas"([^>]*)>', r'<div id="root" data-composition-id="\1"\2>', content)
    content = re.sub(r'<div data-composition-id="(\w+)" class="scene-canvas">', r'<div id="root" data-composition-id="\1">', content)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {fname}")

print("All patches applied successfully!")

