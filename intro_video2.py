"""
Channel intro — timestamp-synced Manim animation.

Voice: enhanced Standard recording 22.mp3

  python run_intro_video2.py
  manim -pqh --disable_caching intro_video2.py IntroVideo2
"""

from __future__ import annotations

import numpy as np
from manim import *

import video_settings as vs
from intro_video2_script import CLOSING, VOICE_FILE
from project_scene import ProjectScene

BLUE, YELLOW, TEAL, ORANGE, PURPLE = vs.BLUE, vs.YELLOW, vs.TEAL, vs.ORANGE, vs.PURPLE
GREY = GREY_B


class IntroVideo2(ProjectScene):
    """Visuals locked to transcript timestamps (see intro_video2_script.py)."""

    def construct(self):
        self.setup_project(brand=True)
        self.add_voice(VOICE_FILE)

        # ── 0:01 community / village awareness ───────────────────────────────
        self.sync(1.0)
        net = self._community_graph(n=7, radius=1.7).move_to(UP * 0.15)
        label = Text("awareness · village", font_size=24, color=YELLOW)
        label.to_edge(DOWN, buff=vs.CAPTION_BOTTOM_BUFF)
        self.show(net, label, run_time=1.2)

        # ── 0:11 science as mystery ──────────────────────────────────────────
        self.sync(11.0)
        mystery = MathTex(r"?", font_size=120, color=YELLOW)
        fog = VGroup(
            MathTex(r"E=?", font_size=28, color=GREY).shift(LEFT * 2.2 + UP * 1.1),
            MathTex(r"\nabla\cdot ?", font_size=28, color=GREY).shift(RIGHT * 2.0 + UP * 0.8),
            MathTex(r"\int ?", font_size=28, color=GREY).shift(LEFT * 1.8 + DOWN * 1.0),
        )
        cue = Text("science feels like a mystery", font_size=24, color=GREY)
        cue.to_edge(DOWN, buff=vs.CAPTION_BOTTOM_BUFF)
        self.wipe(run_time=0.45)
        self.show(mystery, fog, cue, run_time=1.4, anims=[Write(mystery), FadeIn(fog, lag_ratio=0.2), FadeIn(cue)])

        # ── 0:18–0:20 school + career track (ONE clean group, then gone) ─────
        self.sync(18.0)
        board = RoundedRectangle(
            width=5.5, height=2.2, corner_radius=0.12, color=BLUE, stroke_width=2
        )
        school = VGroup(
            Text("8th grade", font_size=22, color=GREY),
            MathTex(r"F = ma", font_size=52, color=BLUE),
            MathTex(r"v = u + at", font_size=30, color=TEAL),
        ).arrange(DOWN, buff=0.22)
        school.move_to(UP * 0.55)
        board.move_to(school.get_center())
        self.wipe(run_time=0.35)
        self.show(board, school, run_time=0.9, anims=[Create(board), FadeIn(school)])

        self.sync(20.0)
        track = VGroup(
            Text("study", font_size=22, color=GREY),
            Arrow(LEFT * 0.6, RIGHT * 0.6, color=YELLOW, buff=0.05, stroke_width=3),
            Text("job", font_size=22, color=GREY),
            Arrow(LEFT * 0.6, RIGHT * 0.6, color=YELLOW, buff=0.05, stroke_width=3),
            Text("track", font_size=22, color=TEAL),
        ).arrange(RIGHT, buff=0.2)
        track.to_edge(DOWN, buff=vs.CAPTION_BOTTOM_BUFF)
        # Must be part of wipe set — never FadeIn orphans
        self.play(FadeIn(track, shift=UP * 0.12), run_time=1.0)
        self._t += 1.0
        self._extra = [track]  # tracked for next wipe

        # ── 0:28 innovations ─────────────────────────────────────────────────
        self.sync(28.0)
        innov = MathTex(r"\text{science} \rightarrow \text{innovation}", font_size=40, color=TEAL)
        spark = VGroup(
            *[
                Line(ORIGIN, 0.55 * np.array([np.cos(a), np.sin(a), 0]), color=YELLOW, stroke_width=2)
                for a in np.linspace(0, TAU, 8, endpoint=False)
            ]
        ).next_to(innov, UP, buff=0.45)
        everyone = Text("to everyone", font_size=26, color=YELLOW).to_edge(DOWN, buff=vs.CAPTION_BOTTOM_BUFF)
        self.wipe(run_time=0.4)
        self.show(innov, spark, everyone, run_time=1.5, anims=[Write(innov), Create(spark), FadeIn(everyone)])

        # ── 0:37 country ─────────────────────────────────────────────────────
        self.sync(37.0)
        country = Text("our country", font_size=36, color=ORANGE)
        arrows_in = VGroup(
            Arrow(UP * 2.2, UP * 0.6, color=BLUE, stroke_width=2),
            Arrow(LEFT * 3 + UP * 0.8, LEFT * 1.2, color=TEAL, stroke_width=2),
            Arrow(RIGHT * 3 + UP * 0.8, RIGHT * 1.2, color=PURPLE, stroke_width=2),
        )
        self.wipe(run_time=0.35)
        self.show(
            country,
            arrows_in,
            run_time=1.2,
            anims=[
                FadeIn(country),
                GrowArrow(arrows_in[0]),
                GrowArrow(arrows_in[1]),
                GrowArrow(arrows_in[2]),
            ],
        )

        # ── 0:43 empty slots ─────────────────────────────────────────────────
        self.sync(43.0)
        boxes = VGroup(
            self._empty_slot("places"),
            self._empty_slot("persons"),
            self._empty_slot("community"),
        ).arrange(RIGHT, buff=0.55)
        self.wipe(run_time=0.3)
        self.show(
            boxes,
            run_time=1.6,
            anims=[LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in boxes], lag_ratio=0.25)],
        )

        # ── 0:50 community — caption top, graph centered (no leftovers) ──────
        self.sync(50.0)
        broad = Text("broader science-thinking community", font_size=26, color=YELLOW)
        broad.to_edge(UP, buff=vs.CAPTION_TOP_BUFF)
        big = self._community_graph(n=7, radius=1.45, color=TEAL)
        big.move_to(DOWN * 0.05)  # between title and bottom — no overlap zone
        self.wipe(run_time=0.4)
        self.show(broad, big, run_time=1.5, anims=[FadeIn(broad), Create(big)])

        # ── 0:56 decision ────────────────────────────────────────────────────
        self.sync(56.0)
        decision = Text("our decision", font_size=40, color=YELLOW)
        check = MathTex(r"\checkmark", font_size=72, color=TEAL).next_to(decision, LEFT, buff=0.35)
        self.wipe(run_time=0.3)
        self.show(check, decision, run_time=1.0, anims=[FadeIn(check, scale=0.8), Write(decision)])

        # ── 0:59 plan ────────────────────────────────────────────────────────
        self.sync(59.0)
        plan = Text("What we are going to do", font_size=34, color=WHITE)
        self.wipe(run_time=0.25)
        self.show(plan, run_time=0.9)

        # ── 1:02 not just facts ──────────────────────────────────────────────
        self.sync(62.0)
        facts = VGroup(
            MathTex(r"2+2=4", font_size=28, color=GREY),
            MathTex(r"H_2O", font_size=28, color=GREY),
            MathTex(r"c = 3\times10^8", font_size=28, color=GREY),
        ).arrange(DOWN, buff=0.35)
        crossed = Text("not just telling facts", font_size=26, color=ORANGE).to_edge(DOWN, buff=vs.CAPTION_BOTTOM_BUFF)
        self.wipe(run_time=0.25)
        self.show(facts, crossed, run_time=1.1)

        # ── 1:07 entertaining ────────────────────────────────────────────────
        self.sync(67.0)
        fun = Text("entertaining way", font_size=36, color=TEAL)
        self.wipe(run_time=0.3)
        self.show(fun, run_time=0.8)

        # ── 1:10 mystery box ─────────────────────────────────────────────────
        self.sync(70.0)
        box = RoundedRectangle(width=3.2, height=2.0, corner_radius=0.1, color=YELLOW, stroke_width=3)
        q = MathTex(r"?", font_size=84, color=YELLOW)
        fact_m = Text("every fact → a mystery", font_size=26, color=GREY).to_edge(DOWN, buff=vs.CAPTION_BOTTOM_BUFF)
        self.wipe(run_time=0.25)
        self.show(box, q, fact_m, run_time=1.3, anims=[Create(box), Write(q), FadeIn(fact_m)])

        # ── 1:15 not distant ─────────────────────────────────────────────────
        self.sync(75.0)
        distant = Text("distant subject", font_size=32, color=GREY)
        strike = Line(distant.get_left(), distant.get_right(), color=ORANGE, stroke_width=4)
        not_lbl = Text("not", font_size=28, color=ORANGE).next_to(distant, UP, buff=0.3)
        self.wipe(run_time=0.25)
        self.show(distant, strike, not_lbl, run_time=1.1, anims=[FadeIn(distant), Create(strike), FadeIn(not_lbl)])

        # ── 1:19–1:21 day-to-day + caption (single wipe unit) ────────────────
        self.sync(79.0)
        daily = self._daily_science().move_to(UP * 0.25)
        both = Text("fact  ·  entertaining", font_size=30, color=YELLOW)
        both.to_edge(DOWN, buff=vs.CAPTION_BOTTOM_BUFF)
        self.wipe(run_time=0.25)
        self.show(daily, both, run_time=1.5, anims=[FadeIn(daily, lag_ratio=0.15), FadeIn(both)])
        # hold through 1:21 in same clean frame
        self.sync(81.0)
        self.wait(0.5)
        self._t += 0.5

        # ── 1:24–1:29 science = reality ──────────────────────────────────────
        self.sync(84.0)
        eq = MathTex(r"\text{science} \neq \text{distant}", font_size=36, color=WHITE)
        self.wipe(run_time=0.35)
        self.show(eq, run_time=0.9)

        self.sync(89.0)
        real = MathTex(
            r"\text{science} = \text{reality of existence}",
            font_size=34,
            color=TEAL,
        )
        self.play(ReplacementTransform(eq, real), run_time=1.2)
        self._t += 1.2
        # eq gone; keep real as only content (re-register for wipe)
        self.remove(eq)
        self._extra = [real]

        # ── 1:31 day-to-day life ─────────────────────────────────────────────
        self.sync(91.0)
        life_icons = self._daily_science().scale(0.85).move_to(UP * 0.55)
        life = Text("day-to-day life  =  science", font_size=30, color=YELLOW)
        life.to_edge(DOWN, buff=vs.CAPTION_BOTTOM_BUFF)
        self.wipe(run_time=0.3)
        self.show(life_icons, life, run_time=1.1)

        # ── 1:34 pipeline ────────────────────────────────────────────────────
        self.sync(94.0)
        pipeline = MathTex(
            r"\text{modify} \rightarrow \text{innovate} \rightarrow \text{country}",
            font_size=32,
            color=BLUE,
        )
        future = Text("future", font_size=26, color=GREY).next_to(pipeline, DOWN, buff=0.5)
        self.wipe(run_time=0.3)
        self.show(pipeline, future, run_time=1.4, anims=[Write(pipeline), FadeIn(future)])

        # ── 1:40 civilization skyline ────────────────────────────────────────
        self.sync(100.0)
        civ = self._civilization().move_to(UP * 0.1)
        civ_lbl = Text("future human civilization", font_size=26, color=YELLOW)
        civ_lbl.to_edge(DOWN, buff=vs.CAPTION_BOTTOM_BUFF)
        self.wipe(run_time=0.3)
        self.show(civ, civ_lbl, run_time=1.4)

        # ── 1:45 path above skyline (same frame, still clean) ────────────────
        self.sync(105.0)
        path = Arrow(LEFT * 2.6, RIGHT * 2.6, color=TEAL, stroke_width=4, buff=0)
        path.next_to(civ, UP, buff=0.85)
        self.play(GrowArrow(path), run_time=0.8)
        self._t += 0.8
        self._extra.append(path)

        # ── 1:47–1:51 visual pulse → rising city (no word stack) ─────────────
        self.sync(107.0)
        self.wipe(run_time=0.4)
        pulse = Circle(radius=0.4, color=GREY, stroke_width=2)
        self.add(pulse)
        self.play(pulse.animate.scale(3.0).set_stroke(opacity=0.2), run_time=1.0)
        self._t += 1.0
        self._extra = [pulse]

        self.sync(111.0)
        civ_rise = self._civilization().move_to(ORIGIN)
        self.wipe(run_time=0.35)
        self.show(civ_rise, run_time=1.1, anims=[FadeIn(civ_rise, shift=UP * 0.35)])

        # ── 1:55 pioneer + star (top padding) ────────────────────────────────
        self.sync(115.0)
        star = Star(n=5, outer_radius=0.5, color=YELLOW, fill_opacity=0.95)
        star.to_edge(UP, buff=vs.PIONEER_TOP_BUFF)
        pioneer = Text("a pioneer", font_size=40, color=TEAL)
        pioneer.next_to(star, DOWN, buff=0.75)
        self.wipe(run_time=0.3)
        self.show(star, pioneer, run_time=1.0, anims=[FadeIn(star, scale=0.6), FadeIn(pioneer)])

        # ── 1:58 channel mark ────────────────────────────────────────────────
        self.sync(118.0)
        ch_mark = RoundedRectangle(
            width=3.4, height=1.2, corner_radius=0.12, color=WHITE, stroke_width=2
        )
        ch_dot = Dot(color=TEAL, radius=0.12).move_to(ch_mark.get_left() + RIGHT * 0.45)
        self.wipe(run_time=0.3)
        self.show(ch_mark, ch_dot, run_time=0.9)

        # ── 2:01 build — skyline only + bottom word, large gap ───────────────
        self.sync(121.0)
        towers = self._civilization().move_to(UP * 0.15)
        build = Text("build", font_size=28, color=YELLOW)
        build.to_edge(DOWN, buff=vs.SKYLINE_BOTTOM_BUFF)
        self.wipe(run_time=0.3)
        self.show(
            towers,
            build,
            run_time=1.9,
            anims=[FadeIn(towers, shift=UP * 0.5), FadeIn(build)],
        )

        # ── 2:07 Earth ───────────────────────────────────────────────────────
        self.sync(127.0)
        earth = Circle(radius=1.0, color=BLUE, stroke_width=3)
        land = Ellipse(
            width=0.8, height=0.4, color=TEAL, fill_opacity=0.5, stroke_width=0
        ).shift(UP * 0.12)
        earth_g = VGroup(earth, land).move_to(ORIGIN)
        self.wipe(run_time=0.3)
        self.show(earth_g, run_time=0.9, anims=[Create(earth), FadeIn(land)])

        # ── 2:09 universe — compact, nothing else on screen ──────────────────
        self.sync(129.0)
        orbits = VGroup(
            Circle(radius=1.3, color=GREY, stroke_width=1.2, stroke_opacity=0.55),
            Circle(radius=1.75, color=GREY, stroke_width=1.2, stroke_opacity=0.4),
            Circle(radius=2.2, color=GREY, stroke_width=1.0, stroke_opacity=0.3),
        )
        dots = VGroup(
            Dot(orbits[0].point_at_angle(0.5), color=ORANGE, radius=0.07),
            Dot(orbits[1].point_at_angle(2.2), color=PURPLE, radius=0.08),
            Dot(orbits[2].point_at_angle(4.1), color=YELLOW, radius=0.06),
        )
        self.play(earth_g.animate.scale(0.42), Create(orbits), FadeIn(dots), run_time=1.6)
        self._t += 1.6
        self._extra = [earth_g, orbits, dots]

        # ── 2:13 motive rays ─────────────────────────────────────────────────
        self.sync(133.0)
        core = Dot(ORIGIN, color=YELLOW, radius=0.14)
        ring = Circle(radius=1.2, color=TEAL, stroke_width=2)
        rays = VGroup(
            *[
                Line(
                    0.25 * np.array([np.cos(a), np.sin(a), 0]),
                    1.85 * np.array([np.cos(a), np.sin(a), 0]),
                    color=YELLOW,
                    stroke_width=1.5,
                    stroke_opacity=0.7,
                )
                for a in np.linspace(0, TAU, 6, endpoint=False)
            ]
        )
        self.wipe(run_time=0.35)
        self.show(rays, ring, core, run_time=1.0, anims=[Create(ring), FadeIn(core), Create(rays)])

        # ── 2:16 visual story flow ───────────────────────────────────────────
        self.sync(136.0)
        qbox = RoundedRectangle(
            width=1.3, height=1.0, corner_radius=0.08, color=YELLOW, stroke_width=2
        )
        qmark = MathTex(r"?", font_size=40, color=YELLOW).move_to(qbox)
        step1 = VGroup(qbox, qmark)
        step2 = self._daily_science().scale(0.42)
        step3 = self._civilization().scale(0.5)
        flow = VGroup(step1, step2, step3).arrange(RIGHT, buff=0.9).move_to(ORIGIN)
        arrs = VGroup(
            Arrow(step1.get_right(), step2.get_left(), buff=0.1, color=GREY, stroke_width=2),
            Arrow(step2.get_right(), step3.get_left(), buff=0.1, color=GREY, stroke_width=2),
        )
        self.wipe(run_time=0.3)
        self.show(flow, arrs, run_time=1.3)

        self.sync(CLOSING)
        self.wipe(run_time=0.5, keep_brand=False)
        end = Text("Science Community", font_size=40, color=WHITE)
        self.play(FadeIn(end), run_time=0.8)
        self.wait(1.5)

    def _community_graph(self, n=7, radius=2.0, color=BLUE) -> VGroup:
        angles = np.linspace(0, TAU, n, endpoint=False)
        pts = [radius * np.array([np.cos(a), np.sin(a), 0]) for a in angles]
        dots = VGroup(*[Dot(p, color=color, radius=0.1) for p in pts])
        edges = VGroup()
        for i in range(n):
            j = (i + 1) % n
            edges.add(Line(pts[i], pts[j], color=color, stroke_width=1.8, stroke_opacity=0.6))
            if i % 2 == 0:
                edges.add(
                    Line(ORIGIN, pts[i], color=YELLOW, stroke_width=1.2, stroke_opacity=0.35)
                )
        center = Dot(ORIGIN, color=YELLOW, radius=0.12)
        return VGroup(edges, dots, center)

    def _empty_slot(self, name: str) -> VGroup:
        box = RoundedRectangle(
            width=2.4, height=1.6, corner_radius=0.1, color=ORANGE, stroke_width=2
        )
        cross = VGroup(
            Line(UL * 0.35, DR * 0.35, color=ORANGE, stroke_width=3),
            Line(UR * 0.35, DL * 0.35, color=ORANGE, stroke_width=3),
        )
        lbl = Text(f"no {name}", font_size=20, color=GREY).next_to(box, DOWN, buff=0.2)
        return VGroup(box, cross, lbl)

    def _daily_science(self) -> VGroup:
        apple = Circle(radius=0.28, color=ORANGE, fill_opacity=0.85, stroke_width=0)
        stem = Line(UP * 0.28, UP * 0.45, color=TEAL, stroke_width=2)
        g_arrow = Arrow(ORIGIN, DOWN * 0.9, color=YELLOW, stroke_width=2, buff=0)
        g_lbl = MathTex(r"g", font_size=22, color=YELLOW).next_to(g_arrow, RIGHT, buff=0.1)
        grav = VGroup(apple, stem, g_arrow, g_lbl).arrange(DOWN, buff=0.05)
        wave = FunctionGraph(lambda x: 0.35 * np.sin(2.5 * x), x_range=[-1.4, 1.4], color=BLUE)
        wave_lbl = MathTex(r"y=\sin x", font_size=20, color=GREY).next_to(wave, DOWN, buff=0.15)
        wave_g = VGroup(wave, wave_lbl)
        ray = Arrow(LEFT * 0.9, RIGHT * 0.9, color=YELLOW, stroke_width=3, buff=0)
        prism = Polygon(
            LEFT * 0.4 + DOWN * 0.35, RIGHT * 0.4 + DOWN * 0.35, UP * 0.45, color=TEAL, stroke_width=2
        )
        light = VGroup(ray, prism)
        return VGroup(grav, wave_g, light).arrange(RIGHT, buff=1.1)

    def _civilization(self) -> VGroup:
        bars = VGroup(
            *[
                Rectangle(width=0.35, height=h, fill_color=c, fill_opacity=0.85, stroke_width=0)
                for h, c in [
                    (0.9, BLUE),
                    (1.4, TEAL),
                    (1.1, PURPLE),
                    (1.8, BLUE),
                    (1.2, ORANGE),
                    (1.55, TEAL),
                ]
            ]
        ).arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
        base = Line(bars.get_left() + LEFT * 0.2, bars.get_right() + RIGHT * 0.2, color=GREY)
        base.next_to(bars, DOWN, buff=0.05)
        return VGroup(bars, base)
