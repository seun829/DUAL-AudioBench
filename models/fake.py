"""Compatibility import for the deterministic closed-loop dry-run agent."""

from dual_audio.agents.mock import MockAgent


Agent = MockAgent

__all__ = ["Agent", "MockAgent"]
