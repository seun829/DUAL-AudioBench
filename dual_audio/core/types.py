from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Observation:
    """One state-conditioned user turn presented to an agent."""

    text: str
    stage: str
    modality: str = "audio"
    audio_path: Path | None = None
    instruction: str = ""
    action_menu: tuple[dict[str, str], ...] = ()
    style_menu: tuple[dict[str, str], ...] = ()
    # Test adapters may use private metadata. Production prompts never serialize it.
    private: dict[str, Any] = field(default_factory=dict, repr=False, compare=False)


@dataclass
class AgentResponse:
    """Normalized agent turn. Actions are public menu labels, not gold action names."""

    message: str = ""
    action: str | None = None
    response_style: str | None = None
    raw: str | None = None
