#!/usr/bin/env python3
"""Render qubit scenes one by one using project-wide settings."""

import subprocess
import sys
from pathlib import Path

import video_settings as vs

ROOT = Path(__file__).resolve().parent
SCENES = [
    "Intro",
    "QubitCollision",
    "ComplexNumbers",
]


def main():
    # Optional TTS (legacy); skip if you only use recordings
    print("Generating narration audio (if needed)…\n")
    subprocess.run([sys.executable, "generate_audio.py"], cwd=ROOT)

    for i, scene in enumerate(SCENES, 1):
        print(f"\n[{i}/{len(SCENES)}] Rendering {scene}…\n")
        cmd = [
            sys.executable,
            "-m",
            "manim",
            *vs.manim_cmd("scenes.py", scene, preview=True),
        ]
        print(" ", " ".join(cmd))
        result = subprocess.run(cmd, cwd=ROOT)
        if result.returncode != 0:
            print(f"Failed on {scene} (exit {result.returncode})")
            sys.exit(result.returncode)

    print("\nAll scenes done.")
    print("Videos: media/videos/scenes/1080p60/")


if __name__ == "__main__":
    main()
