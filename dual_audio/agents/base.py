from __future__ import annotations

from typing import Protocol

from dual_audio.core.types import AgentResponse, Observation


class Agent(Protocol):
    """Common alternating-turn interface implemented by every model adapter."""

    def respond(
        self,
        observation: Observation,
        history: list[dict],
    ) -> AgentResponse:
        """Produce a dialogue response or a structured menu choice."""
