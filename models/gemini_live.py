"""Gemini audio/text adapter used by the alternating-turn replay runner.

The benchmark is half-duplex and does not require a persistent realtime
session. Each call sends the accumulated replay WAV plus the current decision
instruction through the standard multimodal content API.

Requires: ``pip install google-genai``
Environment: ``GOOGLE_API_KEY`` and optionally ``GEMINI_MODEL``.
"""

from __future__ import annotations

import os
from pathlib import Path

from google import genai
from google.genai import types


MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")


def _client() -> genai.Client:
    """Create a Gemini client from the standard environment API key."""

    return genai.Client(api_key=os.environ["GOOGLE_API_KEY"])


def ask(audio_path: str, question: str) -> str:
    """Send a replay WAV plus current turn instruction to Gemini."""

    audio = types.Part.from_bytes(
        data=Path(audio_path).read_bytes(),
        mime_type="audio/wav",
    )
    response = _client().models.generate_content(
        model=MODEL,
        contents=[audio, question],
    )
    return (response.text or "").strip()


def ask_text(prompt: str) -> str:
    """Run the transcript-only control through the same configured model."""

    response = _client().models.generate_content(model=MODEL, contents=prompt)
    return (response.text or "").strip()


if __name__ == "__main__":
    import sys

    print(ask(sys.argv[1], sys.argv[2]))
