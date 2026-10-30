with open('brag-output/composition/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove transition
html = html.replace('transition: width 0.1s linear;', '')

# 2. Fix SFX paths to existing files
html = html.replace('assets/sfx/impact/card-place-1.ogg', 'assets/sfx/impactPlate_heavy_000.ogg')
html = html.replace('assets/sfx/interface/switch1.ogg', 'assets/sfx/switch1.ogg')
html = html.replace('assets/sfx/interface/switch2.ogg', 'assets/sfx/switch2.ogg')
html = html.replace('assets/sfx/ui/switch3.ogg', 'assets/sfx/switch3.ogg')
html = html.replace('assets/sfx/impact/card-shove-1.ogg', 'assets/sfx/impactBell_heavy_000.ogg')

# 3. Ensure distinct track indices for each audio
audio_block_old = '''      <!-- SFX Track -->
      <audio
        id="sfx-hit1"
        data-start="0.1"
        data-duration="1.5"
        data-track-index="2"
        data-volume="0.6"
        src="assets/sfx/impactPlate_heavy_000.ogg"
      ></audio>
      <audio
        id="sfx-card1"
        data-start="2.6"
        data-duration="0.8"
        data-track-index="2"
        data-volume="0.5"
        src="assets/sfx/switch1.ogg"
      ></audio>
      <audio
        id="sfx-card2"
        data-start="3.1"
        data-duration="0.8"
        data-track-index="2"
        data-volume="0.5"
        src="assets/sfx/switch2.ogg"
      ></audio>
      <audio
        id="sfx-slider"
        data-start="7.6"
        data-duration="1.0"
        data-track-index="2"
        data-volume="0.5"
        src="assets/sfx/switch3.ogg"
      ></audio>
      <audio
        id="sfx-winner"
        data-start="13.2"
        data-duration="1.5"
        data-track-index="2"
        data-volume="0.7"
        src="assets/sfx/impactBell_heavy_000.ogg"
      ></audio>'''

audio_block_new = '''      <!-- SFX Tracks -->
      <audio
        id="sfx-hit1"
        data-start="0.1"
        data-duration="1.5"
        data-track-index="2"
        data-volume="0.6"
        src="assets/sfx/impactPlate_heavy_000.ogg"
      ></audio>
      <audio
        id="sfx-card1"
        data-start="2.6"
        data-duration="0.8"
        data-track-index="3"
        data-volume="0.5"
        src="assets/sfx/switch1.ogg"
      ></audio>
      <audio
        id="sfx-card2"
        data-start="3.1"
        data-duration="0.8"
        data-track-index="4"
        data-volume="0.5"
        src="assets/sfx/switch2.ogg"
      ></audio>
      <audio
        id="sfx-slider"
        data-start="7.6"
        data-duration="1.0"
        data-track-index="5"
        data-volume="0.5"
        src="assets/sfx/switch3.ogg"
      ></audio>
      <audio
        id="sfx-winner"
        data-start="13.2"
        data-duration="1.5"
        data-track-index="6"
        data-volume="0.7"
        src="assets/sfx/impactBell_heavy_000.ogg"
      ></audio>'''

if audio_block_old in html:
    html = html.replace(audio_block_old, audio_block_new)

with open('brag-output/composition/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Successfully patched composition index.html')

