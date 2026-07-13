#!/usr/bin/env python3
"""Generate narration, then render each scene in high quality (1080p) with audio."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCENES = [
    "Intro",
    "QubitCollision",
    "ComplexNumbers",
]


def main():
    print("Generating narration audio…\n")
    result = subprocess.run([sys.executable, "generate_audio.py"], cwd=ROOT)
    if result.returncode != 0:
        sys.exit(result.returncode)

    # -qh = 1080p60 · --disable_caching keeps TTS reliably muxed into the mp4
    for i, scene in enumerate(SCENES, 1):
        print(f"\n[{i}/{len(SCENES)}] Rendering {scene} (1080p + narration)…\n")
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "manim",
                "-pqh",
                "--disable_caching",
                "scenes.py",
                scene,
            ],
            cwd=ROOT,
        )
        if result.returncode != 0:
            print(f"Failed on {scene} (exit {result.returncode})")
            sys.exit(result.returncode)

    print("\nAll scenes done (1080p + narration).")
    print("Videos: media/videos/scenes/1080p60/")


if __name__ == "__main__":
    main()
