"""Generate timestamp-padded TTS for intro_video2.

  python generate_intro_video2_audio.py
  python generate_intro_video2_audio.py --force
"""

from __future__ import annotations

import asyncio
import json
import subprocess
from pathlib import Path

from pydub import AudioSegment

from intro_video2_script import AUDIO_DIR, BEATS, CLOSING, END, VOICE


def _ffprobe_duration(path: Path) -> float:
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


async def _tts(text: str, out: Path, retries: int = 5) -> None:
    import edge_tts

    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            communicate = edge_tts.Communicate(text, VOICE, rate="-8%")
            await communicate.save(str(out))
            return
        except Exception as err:  # network blips
            last_err = err
            wait = 1.5 * (attempt + 1)
            print(f"    retry {attempt + 1}/{retries} in {wait:.1f}s ({err.__class__.__name__})")
            await asyncio.sleep(wait)
    raise RuntimeError(f"TTS failed for {out.name}") from last_err


def _slot_ends() -> list[float]:
    ends = [BEATS[i + 1][0] for i in range(len(BEATS) - 1)]
    ends.append(CLOSING)
    return ends


async def generate(force: bool = False) -> Path:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    ends = _slot_ends()
    pieces: list[AudioSegment] = []

    # Silence from 0:00 → first beat (0:01)
    pieces.append(AudioSegment.silent(duration=int(BEATS[0][0] * 1000)))

    meta = []
    for i, ((start, text), end) in enumerate(zip(BEATS, ends)):
        raw = AUDIO_DIR / f"beat_{i:02d}_raw.mp3"
        need = force or not raw.exists() or raw.stat().st_size < 500
        if need:
            if raw.exists():
                raw.unlink()
            print(f"  TTS  [{start:6.1f}s] beat_{i:02d}")
            await _tts(text, raw)
        else:
            print(f"  skip [{start:6.1f}s] beat_{i:02d}")

        seg = AudioSegment.from_file(raw)
        slot_ms = int(round((end - start) * 1000))
        # Fit voice into the timestamp slot (trim or pad)
        if len(seg) > slot_ms:
            seg = seg[:slot_ms]
        else:
            seg = seg + AudioSegment.silent(duration=slot_ms - len(seg))

        fitted = AUDIO_DIR / f"beat_{i:02d}.mp3"
        seg.export(fitted, format="mp3")
        pieces.append(seg)
        meta.append(
            {
                "i": i,
                "start": start,
                "end": end,
                "text": text,
                "voice_ms": len(AudioSegment.from_file(raw)),
                "slot_ms": slot_ms,
            }
        )

    full = sum(pieces[1:], pieces[0])
    out = AUDIO_DIR / "full.mp3"
    full.export(out, format="mp3")
    (AUDIO_DIR / "timeline.json").write_text(json.dumps(meta, indent=2))
    print(f"Wrote {out} ({len(full) / 1000:.1f}s)")
    return out


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    print(f"Voice: {VOICE}\nDir: {AUDIO_DIR}")
    asyncio.run(generate(force=args.force))


if __name__ == "__main__":
    main()
