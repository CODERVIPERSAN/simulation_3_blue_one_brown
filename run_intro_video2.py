#!/usr/bin/env python3
"""Enhance Standard recording 22 + render intro_video2 (project defaults)."""

import subprocess
import sys
from pathlib import Path

import video_settings as vs
from intro_video2_script import SOURCE_RECORDING, VOICE_FILE

ROOT = Path(__file__).resolve().parent


def enhance() -> None:
    if not SOURCE_RECORDING.exists():
        print(f"Missing recording: {SOURCE_RECORDING}")
        sys.exit(1)
    print(f"Enhancing: {SOURCE_RECORDING.name} → {VOICE_FILE.name}")
    r = subprocess.run(vs.enhance_voice_ffmpeg(SOURCE_RECORDING, VOICE_FILE), cwd=ROOT)
    if r.returncode:
        sys.exit(r.returncode)


def main():
    enhance()
    print("\nRendering IntroVideo2 (project settings: 1080p60)…")
    cmd = [sys.executable, "-m", "manim", *vs.manim_cmd("intro_video2.py", "IntroVideo2", preview=True)]
    print(" ", " ".join(cmd))
    r = subprocess.run(cmd, cwd=ROOT)
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
