import subprocess
import json

voice = "en-US-AndrewNeural"

segments = [
    {
        "id": "scene1",
        "file": "brag-output/composition/assets/voice/scene1.mp3",
        "text": "Welcome to our university major project: Discovering Global Carbon Emission Archetypes Through Unsupervised Learning. For decades, international climate agreements have evaluated countries based on gross carbon tonnage. But raw emissions lie. Comparing total volume punishes emerging economies while completely masking their structural industrial bottlenecks."
    },
    {
        "id": "scene2",
        "file": "brag-output/composition/assets/voice/scene2.mp3",
        "text": "To fix this, we analyze emissions across five essential macro-sectors: Energy, Industry, Transport, Agriculture, and Buildings. Because these proportions must sum to exactly one hundred percent, standard Euclidean distance produces false geometric distortions. We apply a Centered Log-Ratio, or CLR transformation, mapping the five-dimensional simplex into unconstrained real space."
    },
    {
        "id": "scene3",
        "file": "brag-output/composition/assets/voice/scene3.mp3",
        "text": "Through unsupervised machine learning across over two hundred sovereign nations, our model discovers five distinct economic archetypes: Energy-Heavy economies dominated by power grids; Agriculture-Heavy nations with high livestock and crop emissions; Industry-Heavy economies bound to steel and cement; Transport-Heavy freight corridors; and Buildings-Heavy urban centres. Each group faces a fundamentally different decarbonization pathway."
    },
    {
        "id": "scene4",
        "file": "brag-output/composition/assets/voice/scene4.mp3",
        "text": "Here is the model functioning in real time. In Section One, selecting a sovereign nation immediately renders its five-axis radar footprint and empirical classification. Along with the classification, an Explainable AI card translates the mathematical centroid distance into an actionable, plain-English decarbonization roadmap cataloged for that exact archetype."
    },
    {
        "id": "scene5",
        "file": "brag-output/composition/assets/voice/scene5.mp3",
        "text": "Next, we test the What-If policy simulator. When a policy maker adjusts the Energy slider downwards, our algorithm automatically and proportionally rebalances the other four sectors in real time, strictly preserving the one hundred percent compositional closure. As the emissions mix changes, the model recalculates the nearest centroid and dynamically predicts the country's future archetype."
    },
    {
        "id": "scene6",
        "file": "brag-output/composition/assets/voice/scene6.mp3",
        "text": "In Section Four, we conducted a rigorous benchmark across four clustering paradigms: K-Means, Gaussian Mixture Models, Hierarchical Clustering, and DBSCAN. While DBSCAN collapsed into a single grey mass and discarded forty-nine sovereign nations as unclassifiable noise, K-Means achieved clean two-dimensional cluster separation, winning with a decisive Silhouette Score of zero point four seven nine."
    },
    {
        "id": "scene7",
        "file": "brag-output/composition/assets/voice/scene7.mp3",
        "text": "By uniting compositional geometry, unsupervised machine learning, and explainable AI, our system transforms raw emission statistics into transparent sovereign climate policy. Thank you for watching our major project demonstration."
    }
]

print("Generating voiceover audio segments with edge-tts...")
durations = {}

for s in segments:
    cmd = [
        r".\.venv\Scripts\edge-tts.exe",
        "--voice", voice,
        "--text", s["text"],
        "--write-media", s["file"]
    ]
    subprocess.run(cmd, check=True)
    
    # Probe duration
    probe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", s["file"]
    ]
    res = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
    dur = float(res.stdout.strip())
    durations[s["id"]] = dur
    print(f"Segment {s['id']}: {dur:.2f}s -> {s['file']}")

total_voice_dur = sum(durations.values())
print(f"Total voiceover duration: {total_voice_dur:.2f}s ({total_voice_dur/60:.2f} minutes)")

with open("brag-output/voice_durations.json", "w", encoding="utf-8") as f:
    json.dump(durations, f, indent=2)

