"""Shared narration lines and audio paths."""

from pathlib import Path

VOICE = "en-US-GuyNeural"
AUDIO_DIR = Path(__file__).parent / "audio"

LINES: dict[str, str] = {
    "intro_title": (
        "Today: qubits, how they collide, and why we need complex numbers."
    ),
    "intro_question": "Let's start with a simple question. What even is a qubit?",
    "intro_bit": (
        "A classical bit is just one of two values: zero, or one. "
        "Nothing in between."
    ),
    "intro_qubit": (
        "A qubit can be a weighted blend of both — zero and one — "
        "at the same time."
    ),
    "intro_complex": (
        "Those weights, alpha and beta, are not ordinary numbers. "
        "They are complex numbers."
    ),
    "col_setup": "Two separate qubits. No shared state yet.",
    "col_states": "One sits in zero. The other sits in one.",
    "col_approach": "Now bring them together.",
    "col_entangle": (
        "At the moment of interaction, they become entangled. "
        "They no longer have independent states."
    ),
    "col_bell": (
        "The shared state is a Bell state: both zero, or both one, "
        "with equal weight."
    ),
    "col_measure": (
        "Separate them in space, and measuring one still instantly "
        "fixes the other."
    ),
    "cx_plane": (
        "Every complex number is a point on a plane — "
        "a real part, and an imaginary part."
    ),
    "cx_point": "Here is one plus i. One step right, one step up.",
    "cx_polar": (
        "We can also write it as a length r, and an angle theta — "
        "magnitude and phase."
    ),
    "cx_rotate": (
        "Multiplying by i spins the arrow a quarter turn. "
        "Rotation is built into complex arithmetic."
    ),
    "cx_bridge": (
        "And that is why qubit amplitudes live here — "
        "on the complex plane."
    ),
    "thanks": "Thanks for watching.",
}
