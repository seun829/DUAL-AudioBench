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


def execute_user_action(
    domain: str,
    current_state: dict[str, Any],
    user_action: dict[str, Any] | None,
) -> dict[str, Any]:
    """Execute a hidden user tool call that occurs while the agent is absent.

    The action specification is part of the task transition input. It is not
    shown to the agent before the gap. The resumed observation reports its
    outcome, allowing the agent to resynchronize its belief afterward.
    """

    state = copy.deepcopy(current_state)
    if not user_action:
        return state
    action = user_action["action"]
    state.setdefault("user_action_history", []).append(action)
    state["last_gap_user_action"] = action
    state["gap_user_action_minute"] = user_action.get("at_minute")

    if domain == "tech_support":
        if action != "power_cycle_during_maintenance":
            raise InvalidStateError(f"Unknown tech-support user action: {action}")
        state["restart_attempts"] += 1
        if state["firmware_status"] == "updating":
            state["firmware_status"] = "interrupted"
            state["firmware_progress"] = 0
    elif domain == "pharmacy":
        if action != "contact_plan_provider":
            raise InvalidStateError(f"Unknown pharmacy user action: {action}")
        state["user_verified_active_plan"] = True
    elif domain == "travel":
        if action != "self_protect_onward_segment":
            raise InvalidStateError(f"Unknown travel user action: {action}")
        state["user_rebooked_onward_segment"] = True
        state["connection_status"] = "protected"
    else:
        raise InvalidStateError(f"Unknown domain: {domain}")
    return state


def transition(
    domain: str,
    current_state: dict[str, Any],
    agent_action: str,
    elapsed_minutes: int,
    external_event: dict[str, Any] | None,
    user_action: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Pure deterministic time transition.

    The result is computed from the prior state, executed action, elapsed time,
    external event, and optional hidden user action. No scenario embeds a
    precomputed post-gap state.

    Ordering is explicit: the user's gap action is applied first at its task
    timestamp, then elapsed-time/exogenous rules are evaluated. Current tasks
    use user actions that occur before the external transition threshold.
    """

    if elapsed_minutes < 0:
        raise ValueError("elapsed_minutes must be non-negative")
    if user_action:
        at_minute = user_action.get("at_minute")
        if (
            not isinstance(at_minute, (int, float))
            or at_minute < 0
            or at_minute > elapsed_minutes
        ):
            raise ValueError(
                "user_action.at_minute must fall within the elapsed gap"
            )
    state = execute_user_action(domain, current_state, user_action)
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
        if status in {"stuck", "completed", "interrupted"}:
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
        if status == "interrupted":
            return (
                "While you were unavailable, I unplugged the router and plugged "
                "it back in. The maintenance screen disappeared, and the "
                "connection is still dropping."
            )
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
            if state.get("last_gap_user_action"):
                return (
                    "While you were unavailable, I unplugged the router and "
                    "plugged it back in. The maintenance never started, and the "
                    "connection still drops."
                )
            return (
                "It has been half an hour, but the maintenance never started and "
                "the connection still drops."
            )
        if status == "completed":
            return "The update finished, but the connection is still dropping."
    elif domain == "pharmacy":
        status = state["claim_status"]
        if status == "rejected":
            if state.get("user_verified_active_plan"):
                return (
                    "While you were unavailable, I called the plan provider and "
                    "they confirmed my current plan is active. I came back after "
                    "twenty minutes and the pharmacy claim was still denied."
                )
            return (
                "I came back after twenty minutes and the message says the claim "
                "was denied. That has never happened before."
            )
        if status == "processing":
            if state.get("user_verified_active_plan"):
                return (
                    "While you were unavailable, I called the plan provider and "
                    "they confirmed my current plan is active. The pharmacy claim "
                    "still says it is processing."
                )
            return (
                "It has been twenty minutes and the claim still says it is processing, "
                "with no decision yet."
            )
        if status == "not_submitted":
            if state.get("user_verified_active_plan"):
                return (
                    "While you were unavailable, I called the plan provider and "
                    "they confirmed my current plan is active, but there is still "
                    "no pharmacy claim on the order."
                )
            return (
                "I came back after twenty minutes, but there is no claim on the order yet."
            )
        if status == "approved":
            return "I came back and the claim was approved. Is there anything else?"
    elif domain == "travel":
        if state["flight_status"] == "delayed":
            if state.get("user_rebooked_onward_segment"):
                return (
                    f"While you were unavailable, I changed my later flight and "
                    f"received confirmation. I have now been told this departure "
                    f"is delayed {state['departure_delay_minutes']} minutes."
                )
            return (
                f"I just got a notice that the flight is delayed "
                f"{state['departure_delay_minutes']} minutes. What should I do now?"
            )
        if state.get("user_rebooked_onward_segment"):
            return (
                "While you were unavailable, I changed my later flight and "
                "received confirmation. This departure still shows on time."
            )
        return "I checked again after forty-five minutes and the flight still shows on time."
    raise InvalidStateError(f"No observation rule for {domain}: {state}")
