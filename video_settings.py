"""
Shared settings for EVERY video in this project.

Import from here instead of hardcoding colors, quality, or audio filters.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
AUDIO_DIR = ROOT / "audio"

# ── Render (Manim Community) ─────────────────────────────────────────────────
# Default for all videos: 1080p60, no cache (keeps voice mux reliable), preview
QUALITY = "high_quality"  # -qh → 1920×1080 @ 60fps
DISABLE_CACHING = True
PREVIEW = True

MANIM_FLAGS: list[str] = [
    "-qh",  # 1080p60
    "--disable_caching",
]
# Add "-p" in runners when you want autoplay after render

# ── Look ─────────────────────────────────────────────────────────────────────
BG = "#0B1020"
BLUE = "#58C4DD"
YELLOW = "#F0E68C"
TEAL = "#5CD0B3"
ORANGE = "#E8A87C"
PURPLE = "#C77DFF"
# GREY_B comes from manim — use settings.GREY only after manim import in scenes

BRAND_NAME = "Science Community"
BRAND_FONT_SIZE = 22
BRAND_CORNER_BUFF = 0.35

# Caption / layout padding (avoid overlaps)
CAPTION_BOTTOM_BUFF = 0.75
CAPTION_TOP_BUFF = 1.2
PIONEER_TOP_BUFF = 1.4
SKYLINE_BOTTOM_BUFF = 0.9

# ── Voice enhancement (ffmpeg) — use for any real recording ──────────────────
# highpass rumble · lowpass hiss · denoise · speech presence · loudnorm
VOICE_AF = (
    "highpass=f=80,"
    "lowpass=f=10000,"
    "afftdn=nr=12:nf=-25,"
    "equalizer=f=3000:t=q:w=1.2:g=3,"
    "loudnorm=I=-16:TP=-1.5:LRA=11"
)
VOICE_SAMPLE_RATE = "48000"
VOICE_CHANNELS = "2"
VOICE_BITRATE = "192k"

# Prefer real recordings over TTS when both exist
PREFER_RECORDING = True


def manim_cmd(scene_file: str, scene_name: str, *, preview: bool = True) -> list[str]:
    """Build a standard manim CLI invocation (caller prepends python -m)."""
    flags = list(MANIM_FLAGS)
    if preview:
        flags = ["-p", *flags] if "-p" not in flags else flags
        # -pqh style: merge preview into quality flag
        if "-qh" in flags:
            flags = [("-pqh" if f == "-qh" else f) for f in flags]
            flags = [f for f in flags if f != "-p"]
    return [*flags, scene_file, scene_name]


def enhance_voice_ffmpeg(src: Path, dst: Path) -> list[str]:
    """ffmpeg argv to enhance a raw recording into dst."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    return [
        "ffmpeg",
        "-y",
        "-i",
        str(src),
        "-af",
        VOICE_AF,
        "-ar",
        VOICE_SAMPLE_RATE,
        "-ac",
        VOICE_CHANNELS,
        "-b:a",
        VOICE_BITRATE,
        str(dst),
    ]
