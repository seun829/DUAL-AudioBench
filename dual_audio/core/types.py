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
    belief_schema: dict[str, tuple[str, ...]] = field(default_factory=dict)
    belief_definitions: dict[str, dict[str, str]] | None = None
    prior_state_belief: dict[str, dict[str, float]] = field(default_factory=dict)
    # Test adapters may use private metadata. Production prompts never serialize it.
    private: dict[str, Any] = field(default_factory=dict, repr=False, compare=False)


@dataclass
class AgentResponse:
    """Normalized agent turn. Actions are public menu labels, not gold action names."""

    message: str = ""
    action: str | None = None
    response_style: str | None = None
    state_belief: dict[str, dict[str, float]] = field(default_factory=dict)
    needs_revalidation: bool | None = None
    raw: str | None = None
