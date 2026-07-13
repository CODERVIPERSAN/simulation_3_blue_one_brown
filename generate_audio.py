"""Generate TTS narration clips with edge-tts.

  python generate_audio.py
  python generate_audio.py --force
"""

from __future__ import annotations

import asyncio
import json
import subprocess

from narration import AUDIO_DIR, LINES, VOICE


def duration_seconds(path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


async def _synthesize(text: str, out) -> None:
    import edge_tts

    communicate = edge_tts.Communicate(text, VOICE, rate="-5%")
    await communicate.save(str(out))


async def generate_all(force: bool = False) -> dict[str, float]:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    durations: dict[str, float] = {}

    for key, text in LINES.items():
        path = AUDIO_DIR / f"{key}.mp3"
        if force or not path.exists():
            print(f"  TTS  {key} …")
            await _synthesize(text, path)
        else:
            print(f"  skip {key}")
        durations[key] = duration_seconds(path)

    meta = AUDIO_DIR / "durations.json"
    meta.write_text(json.dumps(durations, indent=2))
    print(f"Wrote {meta}")
    return durations


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Generate narration TTS clips")
    parser.add_argument("--force", action="store_true", help="Regenerate all clips")
    args = parser.parse_args()
    print(f"Voice: {VOICE}\nOutput: {AUDIO_DIR}")
    asyncio.run(generate_all(force=args.force))
    print("Done.")


if __name__ == "__main__":
    main()
