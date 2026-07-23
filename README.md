# Science Community — Manim videos

3Blue1Brown-style math animations for the **Science Community** channel.

All videos share one settings pack so quality, colors, voice, and stage hygiene stay consistent.

---

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Needs: `ffmpeg`, LaTeX (`pdflatex`).

---

## Project settings (use for every video)

| File | Role |
|------|------|
| [`video_settings.py`](video_settings.py) | Colors, 1080p60 flags, voice ffmpeg filter, padding |
| [`manim.cfg`](manim.cfg) | Manim defaults (1080×1920 @ 60fps, no cache) |
| [`project_scene.py`](project_scene.py) | Base scene: brand, `wipe()` / `show()` / `sync()` |

### Defaults locked in

- **Resolution:** 1080p @ 60fps (`-qh`)
- **Caching:** off (`--disable_caching`) — keeps voice reliably muxed
- **Background:** `#0B1020`
- **Palette:** blue / yellow / teal / orange / purple
- **Brand:** “Science Community” (top-left)
- **Voice:** enhance recordings with denoise + EQ + loudnorm (see `VOICE_AF`)
- **Stage rule:** wipe all non-brand mobjects between beats (no ghost layers)
- **Layout:** captions use shared bottom/top buffs so graphs never sit on text

### New video checklist

1. Subclass `ProjectScene` from `project_scene.py`
2. Import colors / buffs from `video_settings`
3. Call `setup_project()`, then `wipe()` / `show()` / `sync()` each beat
4. Prefer a real recording → enhance with `vs.enhance_voice_ffmpeg(...)`
5. Render with `vs.manim_cmd("your_file.py", "YourScene")` or just `manim` (reads `manim.cfg`)

```python
from project_scene import ProjectScene
import video_settings as vs

class MyVideo(ProjectScene):
    def construct(self):
        self.setup_project()
        self.add_voice(vs.AUDIO_DIR / "intro_video2" / "voice_enhanced.mp3")
        self.sync(1.0)
        self.show(Text("Hello", color=vs.YELLOW))
        self.wipe()
```

---

## Channel intro (`IntroVideo2`)

Timestamp-synced channel pitch using **Standard recording 22** (enhanced).

```bash
source .venv/bin/activate
python run_intro_video2.py
```

Output: `media/videos/intro_video2/1080p60/IntroVideo2.mp4`

| File | Purpose |
|------|---------|
| `intro_video2.py` | Animation |
| `intro_video2_script.py` | Transcript timestamps + voice paths |
| `audio/Standard recording 22.mp3` | Raw voice |
| `audio/intro_video2/voice_enhanced.mp3` | Enhanced voice (auto-built) |

---

## Qubit scenes

```bash
source .venv/bin/activate
python run.py
```

| Scene | Content |
|-------|---------|
| `Intro` | Classical bit vs qubit · complex amplitudes |
| `QubitCollision` | Approach · entanglement · Bell state |
| `ComplexNumbers` | Complex plane · polar form · ×i rotation |

Videos: `media/videos/scenes/1080p60/`

Narration lines (TTS): `narration.py` → `python generate_audio.py --force`

---

## Manual render

```bash
# Uses manim.cfg + same flags as runners
manim -pqh --disable_caching intro_video2.py IntroVideo2
manim -pqh --disable_caching scenes.py FullSimulation
```

Preview-only (faster): `manim -pql --disable_caching ...`
