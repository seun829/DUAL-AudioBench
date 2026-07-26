from __future__ import annotations

import copy
from typing import Any


class InvalidStateError(ValueError):
    """Raised when a task requests an unknown domain or unsupported state."""

    pass


def execute_action(
    domain: str,
    current_state: dict[str, Any],
    action: str,
) -> dict[str, Any]:
    """Execute a symbolic tool action and return a new state."""

    state = copy.deepcopy(current_state)
    state.setdefault("action_history", []).append(action)

    if domain == "tech_support":
        if action == "run_maintenance":
            if state["firmware_status"] in {"not_started", "stuck"}:
                state["firmware_status"] = "updating"
                state["maintenance_attempts"] += 1
        elif action == "repeat_power_cycle":
            state["restart_attempts"] += 1
        elif action == "inspect_persistent_state":
            state["configuration_inspected"] = True
        elif action == "close_case":
            state["ticket_status"] = "closed"
    elif domain == "pharmacy":
        if action == "submit_claim":
            state["claim_status"] = "processing"
            state["claim_attempts"] += 1
        elif action == "review_account_configuration":
            state["billing_plan"] = state["active_plan"]
            state["billing_profile_reviewed"] = True
        elif action == "contact_prescriber":
            state["prescriber_contacted"] = True
        elif action == "apply_alternate_payment":
            state["alternate_payment_offered"] = True
        elif action == "close_case":
            state["ticket_status"] = "closed"
    elif domain == "travel":
        if action == "enable_itinerary_monitoring":
            state["monitoring_enabled"] = True
        elif action == "protect_onward_segment":
            state["connection_status"] = "protected"
        elif action == "change_departing_segment":
            state["departure_change_requested"] = True
        elif action == "offer_service_recovery":
            state["service_recovery_offered"] = True
        elif action == "close_case":
            state["ticket_status"] = "closed"
    else:
        raise InvalidStateError(f"Unknown domain: {domain}")
    return state


def transition(
    domain: str,
    current_state: dict[str, Any],
    agent_action: str,
    elapsed_minutes: int,
    external_event: dict[str, Any] | None,
) -> dict[str, Any]:
    """Pure deterministic time transition.

    The result is computed from the prior state, executed action, elapsed time,
    and external event. No scenario embeds a precomputed post-gap state.
    """

    if elapsed_minutes < 0:
        raise ValueError("elapsed_minutes must be non-negative")
    state = copy.deepcopy(current_state)
    state["elapsed_minutes"] = state.get("elapsed_minutes", 0) + elapsed_minutes
    state["last_pre_gap_action"] = agent_action
    event = external_event or {"type": "none"}
    state["last_external_event"] = event["type"]

    if domain == "tech_support":
        if (
            event["type"] == "maintenance_window_elapsed"
            and state["firmware_status"] == "updating"
            and elapsed_minutes >= event["minimum_minutes"]
        ):
            if state["config_integrity"] == "corrupted":
                state["firmware_status"] = "stuck"
                state["firmware_progress"] = event["stuck_percent"]
            else:
                state["firmware_status"] = "completed"
                state["firmware_progress"] = 100
    elif domain == "pharmacy":
        if (
            event["type"] == "claim_processor_cycle"
            and state["claim_status"] == "processing"
            and elapsed_minutes >= event["minimum_minutes"]
        ):
            if state["billing_plan"] != state["active_plan"]:
                state["claim_status"] = "rejected"
                state["claim_rejection_reason"] = "coverage_not_found_for_billed_plan"
            else:
                state["claim_status"] = "approved"
    elif domain == "travel":
        if event["type"] == "departure_delay":
            state["departure_delay_minutes"] = event["delay_minutes"]
            state["flight_status"] = "delayed"
            if (
                state["connection_status"] != "protected"
                and event["delay_minutes"] >= state["layover_minutes"]
            ):
                state["connection_status"] = "missed"
    else:
        raise InvalidStateError(f"Unknown domain: {domain}")
    return state


def correct_action(domain: str, state: dict[str, Any]) -> str:
    """State-based post-gap policy used by the evaluator."""

    if domain == "tech_support":
        status = state["firmware_status"]
        if status in {"stuck", "completed"}:
            return "inspect_persistent_state"
        if status == "not_started":
            return "run_maintenance"
        return "continue_monitoring"
    if domain == "pharmacy":
        status = state["claim_status"]
        if status == "not_submitted":
            return "submit_claim"
        if status == "processing":
            return "continue_monitoring"
        if (
            status == "rejected"
            and state.get("billing_plan") != state.get("active_plan")
        ):
            return "review_account_configuration"
        return "close_case"
    if domain == "travel":
        if state["connection_status"] == "missed":
            return "protect_onward_segment"
        return "enable_itinerary_monitoring"
    raise InvalidStateError(f"Unknown domain: {domain}")


def post_gap_observation(domain: str, state: dict[str, Any]) -> str:
    """Generate a deterministic user report from the actual hidden state."""

    if domain == "tech_support":
        status = state["firmware_status"]
        if status == "stuck":
            return (
                f"It has been half an hour and the update is still at "
                f"{state['firmware_progress']} percent. What should we do now?"
            )
        if status == "updating":
            return (
                "It has been half an hour. The update still says it is in progress, "
                "but it has not shown an error."
            )
        if status == "not_started":
            return (
                "It has been half an hour, but the maintenance never started and "
                "the connection still drops."
            )
        if status == "completed":
            return "The update finished, but the connection is still dropping."
    elif domain == "pharmacy":
        status = state["claim_status"]
        if status == "rejected":
            return (
                "I came back after twenty minutes and the message says the claim "
                "was denied. That has never happened before."
            )
        if status == "processing":
            return (
                "It has been twenty minutes and the claim still says it is processing, "
                "with no decision yet."
            )
        if status == "not_submitted":
            return (
                "I came back after twenty minutes, but there is no claim on the order yet."
            )
        if status == "approved":
            return "I came back and the claim was approved. Is there anything else?"
    elif domain == "travel":
        if state["flight_status"] == "delayed":
            return (
                f"I just got a notice that the flight is delayed "
                f"{state['departure_delay_minutes']} minutes. What should I do now?"
            )
        return "I checked again after forty-five minutes and the flight still shows on time."
    raise InvalidStateError(f"No observation rule for {domain}: {state}")
