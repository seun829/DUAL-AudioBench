"""OpenRouter audio/text adapter used by the alternating-turn replay runner.

Exposes the same ``ask``/``ask_text`` pair as :mod:`models.gemini_live`, so
``ReplayModelAgent`` can drive it unchanged. The transport is OpenRouter's
OpenAI-compatible chat-completions endpoint, which accepts base64 ``input_audio``
parts for audio-capable models.

The benchmark is half-duplex, so each call sends the accumulated replay WAV plus
the current decision instruction as one stateless request.

Environment:
  ``OPENROUTER_API_KEY``  falls back to a ``key=`` entry in ``.env``
  ``OPENROUTER_MODEL``    default ``google/gemini-2.5-flash``

Reported token usage and upstream cost are accumulated per process and written
to ``results/openrouter_usage.json`` at interpreter exit, so a pilot run's real
spend is auditable rather than estimated.
"""

from __future__ import annotations

import atexit
import base64
import json
import os
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path


ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
MODEL = os.environ.get("OPENROUTER_MODEL", "google/gemini-2.5-flash")
TIMEOUT = float(os.environ.get("OPENROUTER_TIMEOUT", "180"))
MAX_ATTEMPTS = int(os.environ.get("OPENROUTER_ATTEMPTS", "4"))
RETRY_STATUS = {408, 409, 429, 500, 502, 503, 504}
USAGE_PATH = Path(os.environ.get("OPENROUTER_USAGE_PATH", "results/openrouter_usage.json"))
FLUSH_EVERY = int(os.environ.get("OPENROUTER_USAGE_FLUSH_EVERY", "20"))

_lock = threading.Lock()
USAGE = {
    "model": MODEL,
    "calls": 0,
    "audio_calls": 0,
    "text_calls": 0,
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "audio_bytes_sent": 0,
    "audio_seconds_sent": 0.0,
    "cost_usd": 0.0,
    "errors": 0,
}


def _api_key() -> str:
    """Return the OpenRouter key from the environment or the local .env file."""

    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if key:
        return key
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            name, value = line.split("=", 1)
            if name.strip() in {"OPENROUTER_API_KEY", "key"}:
                return value.strip()
    raise RuntimeError(
        "No OpenRouter API key found. Set OPENROUTER_API_KEY or add it to .env."
    )


def _record(payload_usage: dict | None, *, audio: bool, audio_bytes: int, seconds: float) -> None:
    """Accumulate reported token usage and upstream cost for one call."""

    usage = payload_usage or {}
    with _lock:
        USAGE["calls"] += 1
        USAGE["audio_calls" if audio else "text_calls"] += 1
        USAGE["prompt_tokens"] += int(usage.get("prompt_tokens") or 0)
        USAGE["completion_tokens"] += int(usage.get("completion_tokens") or 0)
        USAGE["audio_bytes_sent"] += audio_bytes
        USAGE["audio_seconds_sent"] = round(USAGE["audio_seconds_sent"] + seconds, 3)
        USAGE["cost_usd"] = round(USAGE["cost_usd"] + float(usage.get("cost") or 0.0), 6)
        due = USAGE["calls"] % FLUSH_EVERY == 0
    # Flush periodically as well as at exit: a long run killed by a terminal or
    # session teardown never reaches atexit, which loses the whole cost record.
    if due:
        _dump_usage()


def _dump_usage() -> None:
    """Persist accumulated usage so a run's real spend survives the process."""

    if not USAGE["calls"]:
        return
    try:
        USAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
        USAGE_PATH.write_text(json.dumps(USAGE, indent=2) + "\n", encoding="utf-8")
    except OSError:
        pass


atexit.register(_dump_usage)


def _post(body: dict, *, audio_bytes: int = 0, seconds: float = 0.0) -> str:
    """Send one chat completion, retrying transient upstream failures."""

    data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={
            "Authorization": f"Bearer {_api_key()}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/DUAL-AudioBench",
            "X-Title": "DUAL-AudioBench",
        },
        method="POST",
    )
    last = None
    for attempt in range(MAX_ATTEMPTS):
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                payload = json.loads(response.read())
            break
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:400]
            last = RuntimeError(f"OpenRouter HTTP {exc.code}: {detail}")
            if exc.code not in RETRY_STATUS or attempt == MAX_ATTEMPTS - 1:
                with _lock:
                    USAGE["errors"] += 1
                raise last from exc
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last = RuntimeError(f"OpenRouter transport error: {exc!r}")
            if attempt == MAX_ATTEMPTS - 1:
                with _lock:
                    USAGE["errors"] += 1
                raise last from exc
        time.sleep(min(2**attempt, 8))
    else:  # pragma: no cover - loop always breaks or raises
        raise last or RuntimeError("OpenRouter call failed.")

    if payload.get("error"):
        with _lock:
            USAGE["errors"] += 1
        raise RuntimeError(f"OpenRouter error: {payload['error']}")

    _record(payload.get("usage"), audio=bool(audio_bytes), audio_bytes=audio_bytes, seconds=seconds)
    choices = payload.get("choices") or []
    if not choices:
        raise RuntimeError(f"OpenRouter returned no choices: {str(payload)[:300]}")
    return (choices[0].get("message", {}).get("content") or "").strip()


def _wav_seconds(path: Path) -> float:
    """Return WAV duration, or 0.0 when the header cannot be read."""

    import wave

    try:
        with wave.open(str(path), "rb") as handle:
            return handle.getnframes() / float(handle.getframerate())
    except Exception:
        return 0.0


def ask(audio_path: str, question: str) -> str:
    """Send a replay WAV plus the current turn instruction to the model."""

    path = Path(audio_path)
    raw = path.read_bytes()
    body = {
        "model": MODEL,
        "usage": {"include": True},
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": base64.b64encode(raw).decode("ascii"),
                            "format": "wav",
                        },
                    },
                    {"type": "text", "text": question},
                ],
            }
        ],
    }
    return _post(body, audio_bytes=len(raw), seconds=_wav_seconds(path))


def ask_text(prompt: str) -> str:
    """Run the transcript-only control through the same configured model."""

    body = {
        "model": MODEL,
        "usage": {"include": True},
        "messages": [{"role": "user", "content": prompt}],
    }
    return _post(body)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 2:
        print(ask(sys.argv[1], sys.argv[2]))
    else:
        print(ask_text(sys.argv[1]))
