"""Validation and scoring for explicit probabilistic hidden-state beliefs."""

from __future__ import annotations

import math
from typing import Any


def normalize_state_belief(
    raw_belief: dict[str, Any] | None,
    schema: dict[str, tuple[str, ...]],
) -> dict[str, dict[str, float]]:
    """Return valid normalized distributions for declared state variables.

    Missing variables, unknown values, non-numeric probabilities, negative
    probabilities, and zero-mass distributions are omitted. Omitting rather
    than silently inventing a uniform distribution lets the evaluator mark the
    structured response invalid.
    """

    if not isinstance(raw_belief, dict):
        return {}
    normalized: dict[str, dict[str, float]] = {}
    for variable, allowed_values in schema.items():
        candidate = raw_belief.get(variable)
        if not isinstance(candidate, dict):
            continue
        if set(candidate) - set(allowed_values):
            continue
        try:
            values = {
                value: float(candidate.get(value, 0.0)) for value in allowed_values
            }
        except (TypeError, ValueError):
            continue
        if any(not math.isfinite(probability) or probability < 0 for probability in values.values()):
            continue
        total = sum(values.values())
        if total <= 0:
            continue
        normalized[variable] = {
            value: probability / total for value, probability in values.items()
        }
    return normalized


def evaluate_state_belief(
    belief: dict[str, dict[str, float]],
    schema: dict[str, tuple[str, ...]],
    state: dict[str, Any],
) -> dict[str, Any]:
    """Score top-state accuracy, confidence, Brier score, NLL, and entropy."""

    variables: dict[str, dict[str, Any]] = {}
    for variable, allowed_values in schema.items():
        target = str(state[variable])
        distribution = belief.get(variable)
        valid = distribution is not None and target in allowed_values
        if not valid:
            variables[variable] = {
                "target": target,
                "valid": False,
                "top_state": None,
                "confidence": None,
                "correct": False,
                "target_probability": 0.0,
                "brier": None,
                "nll": None,
                "normalized_entropy": None,
            }
            continue
        top_state = max(allowed_values, key=lambda value: distribution[value])
        confidence = distribution[top_state]
        target_probability = distribution[target]
        brier = sum(
            (
                distribution[value]
                - (1.0 if value == target else 0.0)
            )
            ** 2
            for value in allowed_values
        )
        entropy = -sum(
            probability * math.log(probability)
            for probability in distribution.values()
            if probability > 0
        )
        variables[variable] = {
            "target": target,
            "valid": True,
            "top_state": top_state,
            "confidence": confidence,
            "correct": top_state == target,
            "target_probability": target_probability,
            "brier": brier,
            "nll": -math.log(max(target_probability, 1e-12)),
            "normalized_entropy": (
                entropy / math.log(len(allowed_values))
                if len(allowed_values) > 1
                else 0.0
            ),
        }

    valid_rows = [row for row in variables.values() if row["valid"]]
    return {
        "variables": variables,
        "valid": len(valid_rows) == len(schema),
        "all_correct": bool(valid_rows)
        and len(valid_rows) == len(schema)
        and all(row["correct"] for row in valid_rows),
        "mean_confidence": (
            sum(row["confidence"] for row in valid_rows) / len(valid_rows)
            if valid_rows
            else None
        ),
        "mean_brier": (
            sum(row["brier"] for row in valid_rows) / len(valid_rows)
            if valid_rows
            else None
        ),
        "mean_nll": (
            sum(row["nll"] for row in valid_rows) / len(valid_rows)
            if valid_rows
            else None
        ),
        "mean_normalized_entropy": (
            sum(row["normalized_entropy"] for row in valid_rows) / len(valid_rows)
            if valid_rows
            else None
        ),
    }


def probability_of(
    belief: dict[str, dict[str, float]],
    variable: str,
    value: Any,
) -> float:
    """Return assigned probability for a state value, defaulting to zero."""

    return float(belief.get(variable, {}).get(str(value), 0.0))


def top_state_assignment(
    evaluation: dict[str, Any],
) -> dict[str, str]:
    """Extract valid top-state predictions from a belief evaluation."""

    return {
        variable: row["top_state"]
        for variable, row in evaluation["variables"].items()
        if row["valid"] and row["top_state"] is not None
    }
