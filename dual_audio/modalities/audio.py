from __future__ import annotations

import hashlib
import subprocess
import tempfile
import wave
from pathlib import Path


VOICE = {"user": "en-us+f3", "agent": "en-us+m3"}
PROSODY = {
    "frustrated": ("30", "185"),
    "confused": ("60", "150"),
    "urgent": ("65", "190"),
    "confident": ("55", "165"),
    "calm": ("50", "160"),
    "neutral": ("50", "165"),
}


class TurnAudioRenderer:
    """Render and cache one 16 kHz mono WAV per alternating turn."""

    def __init__(self, cache_dir: str | Path = "data/turn_audio"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def render(self, text: str, speaker: str, prosody: str = "neutral") -> Path:
        """Render and cache a normalized 16 kHz, mono, signed-16-bit WAV."""

        key = hashlib.sha256(
            f"{speaker}|{prosody}|{text}".encode("utf-8")
        ).hexdigest()[:24]
        target = self.cache_dir / f"{key}.wav"
        if target.exists():
            return target
        pitch, speed = PROSODY.get(prosody, PROSODY["neutral"])
        with tempfile.TemporaryDirectory() as tmp:
            raw = Path(tmp) / "raw.wav"
            subprocess.run(
                [
                    "espeak-ng",
                    "-v",
                    VOICE[speaker],
                    "-p",
                    pitch,
                    "-s",
                    speed,
                    "-w",
                    str(raw),
                    text,
                ],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    str(raw),
                    "-ar",
                    "16000",
                    "-ac",
                    "1",
                    "-sample_fmt",
                    "s16",
                    str(target),
                ],
                check=True,
                capture_output=True,
            )
        return target


def combine_wavs(paths: list[Path], cache_dir: str | Path) -> Path:
    """Concatenate compatible PCM turn WAVs without re-encoding."""

    if not paths:
        raise ValueError("At least one WAV is required.")
    cache = Path(cache_dir)
    cache.mkdir(parents=True, exist_ok=True)
    fingerprint = "|".join(
        f"{path.resolve()}:{path.stat().st_mtime_ns}:{path.stat().st_size}"
        for path in paths
    )
    target = cache / f"{hashlib.sha256(fingerprint.encode()).hexdigest()[:24]}.wav"
    if target.exists():
        return target

    with wave.open(str(paths[0]), "rb") as first:
        params = first.getparams()
        frames = [first.readframes(first.getnframes())]
    for path in paths[1:]:
        with wave.open(str(path), "rb") as source:
            if (
                source.getnchannels(),
                source.getsampwidth(),
                source.getframerate(),
                source.getcomptype(),
            ) != (
                params.nchannels,
                params.sampwidth,
                params.framerate,
                params.comptype,
            ):
                raise ValueError(f"Incompatible WAV parameters: {path}")
            frames.append(source.readframes(source.getnframes()))
    with wave.open(str(target), "wb") as output:
        output.setparams(params)
        for chunk in frames:
            output.writeframes(chunk)
    return target
