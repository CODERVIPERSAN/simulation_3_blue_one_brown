# 3Blue1Brown-style Manim Simulation

Visual intro covering **qubits**, **qubit–qubit collision**, and **complex amplitudes** — with TTS narration — animated with [Manim Community](https://www.manim.community/).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Needs: `ffmpeg`, LaTeX (`pdflatex`), and internet once (for `edge-tts` voices).

## Render (high quality + narration)

```bash
source .venv/bin/activate
python run.py
```

This will:
1. Generate voiceover clips into `audio/`
2. Render each scene at **1080p** with narration muxed in
3. Open the player after each scene

Videos: `media/videos/scenes/1080p60/`

### Other options

```bash
# Regenerate TTS only
python generate_audio.py --force

# One continuous film
manim -pqh --disable_caching scenes.py FullSimulation

# Preview quality (faster)
manim -pql --disable_caching scenes.py Intro
```

## Scenes

| Scene | Content |
|-------|---------|
| `Intro` | Classical bit vs qubit · complex amplitudes |
| `QubitCollision` | Approach · entanglement · Bell state |
| `ComplexNumbers` | Complex plane · polar form · ×i rotation |

Narration lines live in `narration.py` (edit text → `python generate_audio.py --force`).
