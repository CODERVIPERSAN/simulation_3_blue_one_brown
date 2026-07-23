"""Timestamped channel-intro script for intro_video2.

Voiceover source: audio/Standard recording 22.mp3
Enhanced output:  audio/intro_video2/voice_enhanced.mp3
"""

from pathlib import Path

AUDIO_DIR = Path(__file__).parent / "audio" / "intro_video2"
SOURCE_RECORDING = Path(__file__).parent / "audio" / "Standard recording 22.mp3"
VOICE_FILE = AUDIO_DIR / "voice_enhanced.mp3"

# Transcript timestamps (match Standard recording 22)
END = 136.0  # 2:16 — last line starts
CLOSING = 139.3  # ~end of recording (2:19)

BEATS: list[tuple[float, str]] = [
    (
        1.0,
        "In the science community, through this channel, "
        "we want to bring awareness to the people in our village.",
    ),
    (11.0, "In our village, everyone thinks that science is a mystery."),
    (18.0, "So, this is an eighth grade subject."),
    (
        20.0,
        "We studied this as a subject and if we get a job opportunity, "
        "we will go in that track.",
    ),
    (28.0, "But still, we want to bring new innovations in science to everyone."),
    (37.0, "Even if we want to bring different innovations to our country,"),
    (
        43.0,
        "there are no places to generate ideas for it, "
        "no persons to motivate it, no community for it.",
    ),
    (
        50.0,
        "So, through this channel, if we can bring a broader "
        "science thinking community,",
    ),
    (56.0, "it is our decision."),
    (59.0, "So, what we are going to do is,"),
    (62.0, "in this channel, instead of just telling facts,"),
    (67.0, "in an entertaining way,"),
    (70.0, "we are going to take each and every science fact as a mystery,"),
    (75.0, "not as a distant subject,"),
    (79.0, "but as a day-to-day thing,"),
    (81.0, "as a fact, as an entertaining thing."),
    (84.0, "So, for the people, science is not a distant subject,"),
    (89.0, "it is a reality of existence."),
    (91.0, "So, what we see in our day-to-day life is science."),
    (
        94.0,
        "So, how can we modify science and bring the necessary "
        "innovations to our country in the future.",
    ),
    (100.0, "So, we can bring the future human civilization like this."),
    (105.0, "This channel will be very useful for that."),
    (107.0, "So, the broad motivation of this channel is,"),
    (111.0, "we are going to bring a future human civilization."),
    (115.0, "So, we believe that this channel will be a pioneer for that."),
    (118.0, "So, we are going to bring this channel for that."),
    (121.0, "So, we are going to build a future human civilization,"),
    (127.0, "which is going to rule not only our earth,"),
    (129.0, "but going to rule our broader universe itself."),
    (133.0, "So, that is our main motive."),
    (136.0, "So, this is what all our channel is about."),
]
