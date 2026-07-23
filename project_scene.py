"""
Reusable Manim scene helpers — stage wipe, brand, sync clock.

Use for every new video so leftovers never stack and timing stays consistent.
"""

from __future__ import annotations

from manim import *
import video_settings as vs


class ProjectScene(Scene):
    """Base scene: brand strip, wipe hygiene, timestamp sync."""

    def setup_project(self, *, brand: bool = True) -> None:
        self.camera.background_color = vs.BG
        self._t = 0.0
        self._extra: list = []
        self.brand = None
        if brand:
            self.brand = Text(
                vs.BRAND_NAME,
                font_size=vs.BRAND_FONT_SIZE,
                color=GREY_B,
            )
            self.brand.to_corner(UL, buff=vs.BRAND_CORNER_BUFF)
            self.add(self.brand)

    def wipe(self, run_time: float = 0.35, keep_brand: bool = True) -> None:
        """Fade + remove everything except brand (no ghost layers)."""
        keep = {id(self.brand)} if (keep_brand and self.brand is not None) else set()
        extras = getattr(self, "_extra", [])
        victims = [m for m in list(self.mobjects) if id(m) not in keep]
        for m in extras:
            if m not in victims and id(m) not in keep:
                victims.append(m)
        if victims:
            self.play(*[FadeOut(m) for m in victims], run_time=run_time)
            self.remove(*victims)
            self._t += run_time
        self._extra = []

    def show(self, *mobjects, run_time: float = 1.0, anims=None) -> VGroup:
        """Add a clean group and animate it in."""
        group = VGroup(*mobjects)
        self.add(group)
        self._extra = [group]
        if anims is None:
            self.play(FadeIn(group), run_time=run_time)
        else:
            self.play(*anims, run_time=run_time)
        self._t += run_time
        return group

    def sync(self, target: float) -> None:
        """Wait until scene clock reaches target seconds."""
        dt = target - self._t
        if dt > 0.05:
            self.wait(dt)
            self._t = target
        elif dt < -0.35:
            self._t = max(self._t, target)

    def add_voice(self, path) -> None:
        from pathlib import Path

        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Missing voice file: {p}")
        self.add_sound(str(p))
