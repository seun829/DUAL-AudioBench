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
from pathlib import Path

import requests


ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
MODEL = os.environ.get("OPENROUTER_MODEL", "google/gemini-2.5-flash")
TIMEOUT = float(os.environ.get("OPENROUTER_TIMEOUT", "180"))
MAX_ATTEMPTS = int(os.environ.get("OPENROUTER_ATTEMPTS", "4"))
MAX_TOKENS = int(os.environ.get("OPENROUTER_MAX_TOKENS", "512"))
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
    "total_tokens": 0,
    "audio_bytes_sent": 0,
    "audio_seconds_sent": 0.0,
    "cost_usd": 0.0,
    "errors": 0,
    "provider_counts": {},
}
_PENDING_USAGE: dict[str, int | float | str] = {}
_LOGGABLE_CALLS = 0


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


def _record(
    payload_usage: dict | None,
    *,
    audio: bool,
    audio_bytes: int,
    seconds: float,
    latency_s: float,
    resolved_model: str,
    resolved_provider: str,
) -> None:
    """Accumulate reported token usage and upstream cost for one call."""

    global _LOGGABLE_CALLS
    usage = payload_usage or {}
    with _lock:
        USAGE["calls"] += 1
        USAGE["audio_calls" if audio else "text_calls"] += 1
        USAGE["prompt_tokens"] += int(usage.get("prompt_tokens") or 0)
        USAGE["completion_tokens"] += int(usage.get("completion_tokens") or 0)
        USAGE["total_tokens"] += int(usage.get("total_tokens") or 0)
        USAGE["audio_bytes_sent"] += audio_bytes
        USAGE["audio_seconds_sent"] = round(USAGE["audio_seconds_sent"] + seconds, 3)
        USAGE["cost_usd"] = round(USAGE["cost_usd"] + float(usage.get("cost") or 0.0), 6)
        provider = resolved_provider or "unknown"
        USAGE["provider_counts"][provider] = (
            int(USAGE["provider_counts"].get(provider, 0)) + 1
        )
        _PENDING_USAGE["model_calls"] = int(_PENDING_USAGE.get("model_calls", 0)) + 1
        _PENDING_USAGE["metered_calls"] = int(_PENDING_USAGE.get("metered_calls", 0)) + 1
        for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
            _PENDING_USAGE[key] = int(_PENDING_USAGE.get(key, 0)) + int(
                usage.get(key) or 0
            )
        _PENDING_USAGE["cost"] = round(
            float(_PENDING_USAGE.get("cost", 0.0))
            + float(usage.get("cost") or 0.0),
            8,
        )
        _PENDING_USAGE["request_latency_s"] = round(
            float(_PENDING_USAGE.get("request_latency_s", 0.0)) + latency_s,
            3,
        )
        _PENDING_USAGE["resolved_model"] = resolved_model or MODEL
        pending_providers = _PENDING_USAGE.setdefault("provider_counts", {})
        pending_providers[provider] = int(pending_providers.get(provider, 0)) + 1
        if os.environ.get("OPENROUTER_LOG_USAGE", "1").lower() not in {
            "0", "false", "no"
        }:
            _LOGGABLE_CALLS += 1
        due = USAGE["calls"] % FLUSH_EVERY == 0
    # Flush periodically as well as at exit: a long run killed by a terminal or
    # session teardown never reaches atexit, which loses the whole cost record.
    if due:
        _dump_usage()


def _dump_usage() -> None:
    """Persist accumulated usage so a run's real spend survives the process."""

    if not _LOGGABLE_CALLS:
        return
    try:
        USAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
        USAGE_PATH.write_text(json.dumps(USAGE, indent=2) + "\n", encoding="utf-8")
    except OSError:
        pass


atexit.register(_dump_usage)


def pop_usage() -> dict:
    """Consume per-trajectory telemetry accumulated since the previous call."""

    with _lock:
        usage = dict(_PENDING_USAGE)
        _PENDING_USAGE.clear()
    return usage


def _record_error() -> None:
    """Record one terminal API request failure globally and for its trajectory."""

    with _lock:
        USAGE["errors"] += 1
        _PENDING_USAGE["errors"] = int(_PENDING_USAGE.get("errors", 0)) + 1


def _schema_for_example(value, key: str | None = None) -> dict:
    """Convert the prompt's response example into a strict JSON schema."""

    if isinstance(value, dict):
        return {
            "type": "object",
            "properties": {
                child_key: _schema_for_example(child, child_key)
                for child_key, child in value.items()
            },
            "required": list(value),
            "additionalProperties": False,
        }
    if isinstance(value, bool):
        return {"type": "boolean"}
    if isinstance(value, (int, float)):
        return {"type": "number", "minimum": 0, "maximum": 1}
    if key == "choice":
        return {"type": "string", "enum": list("ABCDE")}
    if key == "response_style":
        return {"type": "string", "enum": list("WXYZ")}
    return {"type": "string"}


def _response_format(prompt: str) -> dict | None:
    """Build strict structured output from the JSON shape embedded in a prompt."""

    marker = "Return JSON only in this shape:"
    if marker not in prompt:
        return None
    try:
        example = json.loads(prompt.rsplit(marker, 1)[1].strip())
    except (json.JSONDecodeError, TypeError):
        return {"type": "json_object"}
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "dual_audio_response",
            "strict": True,
            "schema": _schema_for_example(example),
        },
    }


def _response_text(payload: dict) -> str:
    """Normalize OpenRouter string or typed-list message content to text."""

    choices = payload.get("choices") or []
    if not choices:
        raise RuntimeError(f"OpenRouter returned no choices: {str(payload)[:300]}")
    content = choices[0].get("message", {}).get("content") or ""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        return "".join(
            str(item.get("text") or "")
            for item in content
            if isinstance(item, dict)
            and item.get("type") in {"text", "output_text"}
        ).strip()
    return str(content).strip()


def _post(body: dict, *, audio_bytes: int = 0, seconds: float = 0.0) -> str:
    """Send one chat completion, retrying transient upstream failures."""

    headers = {
        "Authorization": f"Bearer {_api_key()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/DUAL-AudioBench",
        "X-Title": "DUAL-AudioBench",
    }
    last = None
    for attempt in range(MAX_ATTEMPTS):
        started = time.perf_counter()
        try:
            response = requests.post(
                ENDPOINT,
                headers=headers,
                json=body,
                timeout=TIMEOUT,
            )
            if not response.ok:
                status = int(response.status_code)
                last = RuntimeError(
                    f"OpenRouter HTTP {status}: {response.text[:400]}"
                )
                if status not in RETRY_STATUS or attempt == MAX_ATTEMPTS - 1:
                    _record_error()
                    raise last
                time.sleep(min(2**attempt, 8))
                continue
            payload = response.json()
            break
        except (requests.RequestException, ValueError) as exc:
            last = RuntimeError(f"OpenRouter transport error: {exc!r}")
            if attempt == MAX_ATTEMPTS - 1:
                _record_error()
                raise last from exc
            time.sleep(min(2**attempt, 8))
    else:  # pragma: no cover - loop always breaks or raises
        raise last or RuntimeError("OpenRouter call failed.")

    if payload.get("error"):
        _record_error()
        raise RuntimeError(f"OpenRouter error: {payload['error']}")

    _record(
        payload.get("usage"),
        audio=bool(audio_bytes),
        audio_bytes=audio_bytes,
        seconds=seconds,
        latency_s=time.perf_counter() - started,
        resolved_model=str(payload.get("model") or MODEL),
        resolved_provider=str(payload.get("provider") or "unknown"),
    )
    return _response_text(payload)


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
        "max_tokens": MAX_TOKENS,
        "top_p": 1,
        "messages": [
            {
                "role": "system",
                "content": "Follow the supplied conversation and response format exactly.",
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": base64.b64encode(raw).decode("ascii"),
                            "format": "wav",
                        },
                    },
                ],
            }
        ],
    }
    if MODEL.startswith("google/gemini"):
        body["reasoning"] = {"effort": "none"}
    response_format = _response_format(question)
    if response_format:
        body["response_format"] = response_format
    return _post(body, audio_bytes=len(raw), seconds=_wav_seconds(path))


def ask_text(prompt: str) -> str:
    """Run the transcript-only control through the same configured model."""

    body = {
        "model": MODEL,
        "usage": {"include": True},
        "max_tokens": MAX_TOKENS,
        "top_p": 1,
        "messages": [
            {
                "role": "system",
                "content": "Follow the supplied conversation and response format exactly.",
            },
            {"role": "user", "content": prompt},
        ],
    }
    if MODEL.startswith("google/gemini"):
        body["reasoning"] = {"effort": "none"}
    response_format = _response_format(prompt)
    if response_format:
        body["response_format"] = response_format
    return _post(body)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 2:
        print(ask(sys.argv[1], sys.argv[2]))
    else:
        print(ask_text(sys.argv[1]))
