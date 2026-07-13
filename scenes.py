"""
3Blue1Brown-style Manim animations with TTS narration.

  python generate_audio.py   # once
  python run.py              # high quality + play
"""

from __future__ import annotations

import json
from pathlib import Path

from manim import *
import numpy as np

from narration import AUDIO_DIR


# ─── Palette ──────────────────────────────────────────────────────────────────
BLUE_3B1B = "#58C4DD"
YELLOW_3B1B = "#FFFF00"
BROWN_3B1B = "#CD853F"
TEAL = "#5CD0B3"
PINK_Q = "#FF6B9D"
PURPLE_Q = "#C77DFF"
BG = "#0C0F1A"

PAD_AFTER_VOICE = 0.45  # brief breath after each line


def _durations() -> dict[str, float]:
    meta = AUDIO_DIR / "durations.json"
    if meta.exists():
        return json.loads(meta.read_text())
    return {}


DURATIONS = _durations()


def brand_squares(side=0.35, buff=0.12):
    return VGroup(
        Square(side_length=side, fill_color=BLUE_3B1B, fill_opacity=1, stroke_width=0),
        Square(side_length=side, fill_color=BLUE_3B1B, fill_opacity=1, stroke_width=0),
        Square(side_length=side, fill_color=BLUE_3B1B, fill_opacity=1, stroke_width=0),
        Square(side_length=side, fill_color=BROWN_3B1B, fill_opacity=1, stroke_width=0),
    ).arrange(RIGHT, buff=buff)


def make_qubit(color, label, position):
    disk = Circle(
        radius=0.55,
        fill_color=color,
        fill_opacity=0.85,
        stroke_color=WHITE,
        stroke_width=2,
    )
    glow = Circle(radius=0.7, color=color, stroke_width=1.5, stroke_opacity=0.35)
    tex = MathTex(label, font_size=26, color=WHITE)
    group = VGroup(glow, disk, tex)
    group.move_to(position)
    return group


def cue(text, color=GREY_B, font_size=22):
    return Text(text, font_size=font_size, color=color)


def speak(scene: Scene, key: str) -> None:
    """Play narration clip and wait until it finishes (+ small pad)."""
    path = AUDIO_DIR / f"{key}.mp3"
    if not path.exists():
        scene.wait(2.5)
        return
    scene.add_sound(str(path))
    scene.wait(DURATIONS.get(key, 2.5) + PAD_AFTER_VOICE)


class Intro(Scene):
    def construct(self):
        self.camera.background_color = BG

        squares = brand_squares().move_to(UP * 1.8)
        title = Text(
            "Qubits, Collisions &\nComplex Amplitudes",
            font_size=40,
            color=WHITE,
            weight=BOLD,
            line_spacing=1.25,
        ).next_to(squares, DOWN, buff=0.55)
        subtitle = cue("A visual introduction").next_to(title, DOWN, buff=0.4)

        self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in squares], lag_ratio=0.18))
        self.play(Write(title), run_time=2.0)
        self.play(FadeIn(subtitle, shift=UP * 0.15))
        speak(self, "intro_title")

        self.play(FadeOut(squares), FadeOut(subtitle), FadeOut(title))
        self.wait(0.35)

        question = Text("What even is a qubit?", font_size=38, color=YELLOW_3B1B)
        self.play(Write(question), run_time=1.4)
        speak(self, "intro_question")

        self.play(question.animate.scale(0.7).to_edge(UP))
        self.wait(0.3)

        classical_label = Text("Classical bit", font_size=28, color=GREY_A)
        classical_math = MathTex(r"0 \quad\text{or}\quad 1", font_size=44, color=BLUE_3B1B)
        classical = VGroup(classical_label, classical_math).arrange(DOWN, buff=0.35)
        classical.move_to(ORIGIN + UP * 0.3)

        bit_cue = cue("Just one of two values. Nothing in between.")
        bit_cue.to_edge(DOWN, buff=1.0)

        self.play(FadeIn(classical, shift=UP * 0.2))
        self.play(FadeIn(bit_cue))
        speak(self, "intro_bit")

        quantum_label = Text("Qubit", font_size=28, color=GREY_A)
        quantum_math = MathTex(
            r"\alpha|0\rangle + \beta|1\rangle",
            font_size=44,
            color=TEAL,
        )
        quantum = VGroup(quantum_label, quantum_math).arrange(DOWN, buff=0.35)

        pair = VGroup(classical.copy(), quantum).arrange(RIGHT, buff=2.0)
        pair.move_to(ORIGIN + UP * 0.2)

        qubit_cue = cue("A weighted blend of both — at the same time.")
        qubit_cue.to_edge(DOWN, buff=1.0)

        self.play(
            FadeOut(bit_cue),
            Transform(classical, pair[0]),
            FadeIn(quantum, shift=LEFT * 0.25),
        )
        self.play(FadeIn(qubit_cue))
        speak(self, "intro_qubit")

        note = MathTex(r"\alpha,\,\beta \in \mathbb{C}", font_size=36, color=YELLOW_3B1B)
        note.next_to(pair, DOWN, buff=0.7)
        amp_cue = cue("Those weights — alpha and beta — are complex numbers.")
        amp_cue.to_edge(DOWN, buff=0.7)

        self.play(FadeOut(qubit_cue), Write(note), run_time=1.5)
        self.play(FadeIn(amp_cue))
        speak(self, "intro_complex")
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.4)


class QubitCollision(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = Text("Qubit–Qubit Collision", font_size=34, color=WHITE)
        header.to_edge(UP)
        setup_cue = cue("Two separate qubits. No shared state yet.")
        setup_cue.next_to(header, DOWN, buff=0.4)

        self.play(FadeIn(header, shift=DOWN * 0.15))
        self.play(FadeIn(setup_cue))
        speak(self, "col_setup")

        q0 = make_qubit(PINK_Q, r"|q_0\rangle", LEFT * 4)
        q1 = make_qubit(PURPLE_Q, r"|q_1\rangle", RIGHT * 4)
        state0 = MathTex(r"|0\rangle", font_size=28, color=PINK_Q)
        state1 = MathTex(r"|1\rangle", font_size=28, color=PURPLE_Q)
        state0.next_to(q0, DOWN, buff=0.4)
        state1.next_to(q1, DOWN, buff=0.4)

        self.play(FadeIn(q0, scale=0.85), FadeIn(q1, scale=0.85), run_time=1.4)
        self.play(Write(state0), Write(state1))
        speak(self, "col_states")

        approach_cue = cue("Bring them together…")
        approach_cue.next_to(header, DOWN, buff=0.4)
        self.play(FadeOut(setup_cue), FadeIn(approach_cue))
        speak(self, "col_approach")
        self.play(
            q0.animate.shift(RIGHT * 2.6),
            q1.animate.shift(LEFT * 2.6),
            state0.animate.shift(RIGHT * 2.6),
            state1.animate.shift(LEFT * 2.6),
            run_time=2.8,
            rate_func=smooth,
        )
        self.wait(0.4)

        flash = Circle(radius=0.9, color=YELLOW_3B1B, stroke_width=6).move_to(ORIGIN)
        self.play(FadeOut(approach_cue))
        self.play(Create(flash), flash.animate.scale(1.9).set_opacity(0), run_time=0.8)

        ring = Ellipse(width=3.6, height=1.6, color=YELLOW_3B1B, stroke_width=3)
        ent_label = Text("entangled", font_size=26, color=YELLOW_3B1B)
        ent_label.next_to(ring, UP, buff=0.3)
        collide_cue = cue("They no longer have independent states.")
        collide_cue.to_edge(DOWN, buff=1.2)

        self.play(
            Create(ring),
            FadeOut(state0),
            FadeOut(state1),
            Write(ent_label),
            run_time=1.5,
        )
        self.play(FadeIn(collide_cue))
        speak(self, "col_entangle")

        bell = MathTex(
            r"|\Phi^+\rangle = \frac{1}{\sqrt{2}}"
            r"\big(|00\rangle + |11\rangle\big)",
            font_size=34,
            color=TEAL,
        )
        bell.to_edge(DOWN, buff=1.5)
        bell_cue = cue("One shared wave — both zero, or both one.")
        bell_cue.next_to(bell, UP, buff=0.35)

        self.play(FadeOut(collide_cue), Write(bell), run_time=2.0)
        self.play(FadeIn(bell_cue))
        speak(self, "col_bell")

        for _ in range(2):
            self.play(
                ring.animate.set_stroke(opacity=0.25),
                q0[1].animate.set_fill(YELLOW_3B1B, opacity=0.9),
                q1[1].animate.set_fill(YELLOW_3B1B, opacity=0.9),
                run_time=0.55,
            )
            self.play(
                ring.animate.set_stroke(opacity=1),
                q0[1].animate.set_fill(PINK_Q, opacity=0.85),
                q1[1].animate.set_fill(PURPLE_Q, opacity=0.85),
                run_time=0.55,
            )
        self.wait(0.35)

        measure_cue = cue("Separate them — and measuring one still fixes the other.")
        measure_cue.to_edge(DOWN, buff=0.55)

        self.play(FadeOut(bell_cue))
        self.play(
            q0.animate.shift(LEFT * 1.8),
            q1.animate.shift(RIGHT * 1.8),
            ring.animate.stretch(1.7, 0),
            run_time=2.2,
        )
        self.play(bell.animate.shift(UP * 0.35), FadeIn(measure_cue))
        speak(self, "col_measure")
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.4)


class ComplexNumbers(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = Text("Complex Numbers", font_size=34, color=WHITE)
        header.to_edge(UP)
        plane_cue = cue("Every complex number is a point on a plane.")
        plane_cue.next_to(header, DOWN, buff=0.35)

        self.play(FadeIn(header, shift=DOWN * 0.15))
        self.play(FadeIn(plane_cue))
        speak(self, "cx_plane")

        plane = ComplexPlane(
            x_range=[-3, 3, 1],
            y_range=[-2.2, 2.2, 1],
            x_length=7.5,
            y_length=5.5,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.4,
            },
            axis_config={"stroke_color": GREY_A, "stroke_width": 2},
        ).shift(DOWN * 0.55)
        plane.add_coordinates(font_size=18)

        re_label = MathTex(r"\mathrm{Re}", font_size=22, color=GREY_B)
        im_label = MathTex(r"\mathrm{Im}", font_size=22, color=GREY_B)
        re_label.next_to(plane.x_axis.get_end(), RIGHT, buff=0.12)
        im_label.next_to(plane.y_axis.get_end(), UP, buff=0.12)

        self.play(Create(plane), run_time=2.0)
        self.play(FadeIn(re_label), FadeIn(im_label))
        self.wait(0.6)

        z_val = 1 + 1j
        dot = Dot(plane.n2p(z_val), color=YELLOW_3B1B, radius=0.09)
        arrow = Arrow(
            plane.n2p(0),
            plane.n2p(z_val),
            buff=0,
            color=YELLOW_3B1B,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.12,
        )
        z_tex = MathTex(r"z = 1 + i", font_size=30, color=YELLOW_3B1B)
        z_tex.next_to(dot, UR, buff=0.2)

        point_cue = cue("One real part. One imaginary part.")
        point_cue.next_to(header, DOWN, buff=0.35)

        self.play(FadeOut(plane_cue), FadeIn(point_cue))
        self.play(GrowArrow(arrow), FadeIn(dot, scale=2), Write(z_tex), run_time=1.6)
        speak(self, "cx_point")

        polar = MathTex(r"z = r\,e^{i\theta}", font_size=34, color=TEAL)
        polar.to_corner(UL).shift(DOWN * 1.05 + RIGHT * 0.15)

        angle = np.angle(z_val)
        arc = Arc(
            radius=0.75,
            start_angle=0,
            angle=angle,
            arc_center=plane.n2p(0),
            color=TEAL,
            stroke_width=3,
        )
        theta_label = MathTex(r"\theta", font_size=26, color=TEAL)
        theta_label.move_to(plane.n2p(0.6 * np.exp(1j * angle / 2)))

        r_brace = BraceBetweenPoints(
            plane.n2p(0),
            plane.n2p(z_val),
            direction=normalize(plane.n2p(1j * z_val)),
        )
        r_label = MathTex(r"r", font_size=26, color=TEAL)
        r_label.next_to(r_brace, UP, buff=0.05)

        polar_cue = cue("Or: a length, and an angle — magnitude and phase.")
        polar_cue.next_to(header, DOWN, buff=0.35)

        self.play(FadeOut(point_cue), FadeIn(polar_cue), Write(polar))
        self.play(Create(arc), Write(theta_label), run_time=1.2)
        self.play(Create(r_brace), Write(r_label), run_time=1.0)
        speak(self, "cx_polar")

        tip = Text("× i   rotates by 90°", font_size=24, color=PINK_Q)
        tip.to_corner(UR).shift(DOWN * 1.05 + LEFT * 0.15)
        rot_cue = cue("Multiplying by i spins the arrow a quarter turn.")
        rot_cue.next_to(header, DOWN, buff=0.35)

        self.play(
            FadeOut(polar_cue),
            FadeIn(rot_cue),
            FadeIn(tip),
            FadeOut(r_brace),
            FadeOut(r_label),
        )
        speak(self, "cx_rotate")

        z2 = z_val * 1j
        new_dot = Dot(plane.n2p(z2), color=PINK_Q, radius=0.09)
        new_arrow = Arrow(
            plane.n2p(0),
            plane.n2p(z2),
            buff=0,
            color=PINK_Q,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.12,
        )
        z2_tex = MathTex(r"i\cdot z = -1 + i", font_size=28, color=PINK_Q)
        z2_tex.next_to(new_dot, UL, buff=0.15)

        self.play(
            Transform(arrow, new_arrow),
            Transform(dot, new_dot),
            Transform(z_tex, z2_tex),
            FadeOut(arc),
            FadeOut(theta_label),
            run_time=2.4,
        )
        self.wait(0.8)

        bridge = MathTex(
            r"|\psi\rangle = \underbrace{\alpha}_{\in\mathbb{C}}|0\rangle"
            r" + \underbrace{\beta}_{\in\mathbb{C}}|1\rangle",
            font_size=30,
            color=WHITE,
        )
        bridge.to_edge(DOWN, buff=0.7)
        box = SurroundingRectangle(bridge, color=BLUE_3B1B, buff=0.18, corner_radius=0.08)
        bridge_cue = cue("So qubit amplitudes live right here — on this plane.")
        bridge_cue.next_to(header, DOWN, buff=0.35)

        self.play(FadeOut(rot_cue), FadeOut(tip), FadeOut(polar), FadeIn(bridge_cue))
        self.play(Write(bridge), Create(box), run_time=2.0)
        speak(self, "cx_bridge")
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.4)


class FullSimulation(Scene):
    def construct(self):
        self.camera.background_color = BG
        Intro.construct(self)
        QubitCollision.construct(self)
        ComplexNumbers.construct(self)

        end = Text("Thanks for watching", font_size=36, color=WHITE)
        mark = brand_squares(side=0.28, buff=0.1)
        closer = VGroup(mark, end).arrange(DOWN, buff=0.5)
        self.play(FadeIn(closer, scale=0.9))
        speak(self, "thanks")
        self.play(FadeOut(closer))
