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
    elif domain == "banking":
        if action == "file_dispute":
            state["dispute_status"] = "under_review"
            state["dispute_attempts"] += 1
        elif action == "reconcile_card_records":
            state["charge_card"] = state["card_on_file"]
            state["records_reconciled"] = True
        elif action == "order_replacement_card":
            state["replacement_card_ordered"] = True
        elif action == "freeze_account":
            state["account_frozen"] = True
        elif action == "request_merchant_receipt":
            state["merchant_receipt_requested"] = True
        elif action == "close_case":
            state["ticket_status"] = "closed"
    elif domain == "scheduling":
        if action == "request_authorization":
            state["authorization_status"] = "pending"
            state["authorization_attempts"] += 1
        elif action == "obtain_qualifying_referral":
            state["referral_source"] = state["required_source"]
            state["referral_corrected"] = True
        elif action == "book_without_authorization":
            state["provisional_booking"] = True
        elif action == "offer_private_payment":
            state["private_payment_offered"] = True
        elif action == "contact_specialist_office":
            state["specialist_office_contacted"] = True
        elif action == "close_case":
            state["ticket_status"] = "closed"
    elif domain == "logistics":
        if action == "schedule_redelivery":
            state["shipment_status"] = "out_for_delivery"
            state["delivery_attempts"] += 1
        elif action == "correct_destination_record":
            state["label_address"] = state["account_address"]
            state["address_corrected"] = True
        elif action == "open_loss_claim":
            state["loss_claim_opened"] = True
        elif action == "dispatch_replacement_goods":
            state["replacement_dispatched"] = True
        elif action == "contact_courier_depot":
            state["depot_contacted"] = True
        elif action == "close_case":
            state["ticket_status"] = "closed"
    elif domain == "energy":
        if action == "submit_reading":
            state["reading_status"] = "validating"
            state["submission_attempts"] += 1
        elif action == "register_all_supply_points":
            state["registered_points"] = state["actual_points"]
            state["points_registered"] = True
        elif action == "issue_refund":
            state["refund_issued"] = True
        elif action == "book_engineer_visit":
            state["engineer_booked"] = True
        elif action == "review_tariff_history":
            state["tariff_history_reviewed"] = True
        elif action == "close_case":
            state["ticket_status"] = "closed"
    elif domain == "account_access":
        if action == "initiate_credential_reset":
            state["access_status"] = "reset_pending"
            state["reset_attempts"] += 1
        elif action == "engage_identity_provider":
            state["reset_target"] = state["authentication_mode"]
            state["identity_provider_engaged"] = True
        elif action == "provision_new_account":
            state["new_account_provisioned"] = True
        elif action == "grant_temporary_bypass":
            state["temporary_bypass_granted"] = True
        elif action == "clear_browser_state":
            state["browser_state_cleared"] = True
        elif action == "close_case":
            state["ticket_status"] = "closed"
    elif domain == "repair":
        if action == "open_cover_claim":
            state["claim_state"] = "in_assessment"
            state["claim_attempts"] += 1
        elif action == "use_retailer_route":
            state["covered_channel"] = state["purchase_channel"]
            state["retailer_route_used"] = True
        elif action == "dispatch_engineer_now":
            state["engineer_dispatched"] = True
        elif action == "authorise_replacement":
            state["replacement_authorised"] = True
        elif action == "suggest_self_repair":
            state["self_repair_suggested"] = True
        elif action == "close_case":
            state["ticket_status"] = "closed"
    elif domain == "housing":
        if action == "dispatch_maintenance_visit":
            state["work_order_status"] = "dispatched"
            state["dispatch_attempts"] += 1
        elif action == "reissue_access_authority":
            state["vendor_credentials"] = state["required_credentials"]
            state["credentials_reissued"] = True
        elif action == "rehouse_tenant":
            state["tenant_rehoused"] = True
        elif action == "authorise_full_replacement":
            state["full_replacement_authorised"] = True
        elif action == "send_portable_heaters":
            state["portable_heaters_sent"] = True
        elif action == "close_case":
            state["ticket_status"] = "closed"
    elif domain == "mobile_service":
        if action == "submit_port_request":
            state["port_status"] = "in_progress"
            state["port_attempts"] += 1
        elif action == "align_ownership_record":
            state["ownership_record"] = state["required_record"]
            state["ownership_aligned"] = True
        elif action == "issue_new_number":
            state["new_number_issued"] = True
        elif action == "ship_replacement_sim":
            state["replacement_sim_sent"] = True
        elif action == "verify_transfer_code":
            state["transfer_code_verified"] = True
        elif action == "close_case":
            state["ticket_status"] = "closed"
    elif domain == "education":
        if action == "submit_enrolment":
            state["enrolment_status"] = "processing"
            state["enrolment_attempts"] += 1
        elif action == "request_prior_study_assessment":
            state["prior_study_state"] = state["required_state"]
            state["assessment_requested"] = True
        elif action == "defer_to_next_term":
            state["deferred"] = True
        elif action == "waive_requirements":
            state["requirements_waived"] = True
        elif action == "reconfirm_module_choices":
            state["modules_reconfirmed"] = True
        elif action == "close_case":
            state["ticket_status"] = "closed"
    elif domain == "motor_insurance":
        if action == "lodge_claim":
            state["claim_progress"] = "assessing"
            state["lodge_attempts"] += 1
        elif action == "align_policy_records":
            state["policy_name"] = state["keeper_name"]
            state["records_aligned"] = True
        elif action == "declare_total_loss":
            state["total_loss_declared"] = True
        elif action == "authorise_immediate_repair":
            state["repair_authorised"] = True
        elif action == "collect_witness_statement":
            state["witness_statement_collected"] = True
        elif action == "close_case":
            state["ticket_status"] = "closed"
    elif domain == "permits":
        if action == "submit_permit_application":
            state["permit_status"] = "in_check"
            state["application_attempts"] += 1
        elif action == "supply_alternative_proof":
            state["proof_name"] = state["applicant_name"]
            state["alternative_proof_supplied"] = True
        elif action == "issue_temporary_permit":
            state["temporary_permit_issued"] = True
        elif action == "escalate_to_appeals":
            state["appeals_escalated"] = True
        elif action == "reconfirm_vehicle_plate":
            state["plate_reconfirmed"] = True
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
    elif domain == "banking":
        if action != "call_card_services":
            raise InvalidStateError(f"Unknown banking user action: {action}")
        state["user_confirmed_reissue"] = True
    elif domain == "scheduling":
        if action != "call_insurer":
            raise InvalidStateError(f"Unknown scheduling user action: {action}")
        state["user_confirmed_coverage"] = True
    elif domain == "logistics":
        if action != "check_collection_point":
            raise InvalidStateError(f"Unknown logistics user action: {action}")
        state["user_checked_collection_point"] = True
    elif domain == "energy":
        if action != "photograph_dials":
            raise InvalidStateError(f"Unknown energy user action: {action}")
        state["user_photographed_dials"] = True
    elif domain == "account_access":
        if action != "try_recovery_contact":
            raise InvalidStateError(f"Unknown account-access user action: {action}")
        state["user_tried_recovery_contact"] = True
    elif domain == "repair":
        if action != "locate_paperwork":
            raise InvalidStateError(f"Unknown repair user action: {action}")
        state["user_located_paperwork"] = True
    elif domain == "housing":
        if action != "arrange_neighbour_access":
            raise InvalidStateError(f"Unknown housing user action: {action}")
        state["user_arranged_neighbour_access"] = True
    elif domain == "mobile_service":
        if action != "call_old_network":
            raise InvalidStateError(f"Unknown mobile-service user action: {action}")
        state["user_called_old_network"] = True
    elif domain == "education":
        if action != "email_records_office":
            raise InvalidStateError(f"Unknown education user action: {action}")
        state["user_emailed_office"] = True
    elif domain == "motor_insurance":
        if action != "send_photographs":
            raise InvalidStateError(f"Unknown motor-insurance user action: {action}")
        state["user_sent_photographs"] = True
    elif domain == "permits":
        if action != "visit_local_office":
            raise InvalidStateError(f"Unknown permits user action: {action}")
        state["user_visited_office"] = True
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
    elif domain == "banking":
        if (
            event["type"] == "dispute_review_cycle"
            and state["dispute_status"] == "under_review"
            and elapsed_minutes >= event["minimum_minutes"]
        ):
            if state["charge_card"] != state["card_on_file"]:
                state["dispute_status"] = "returned_unmatched"
                state["dispute_return_reason"] = "identifier_mismatch_against_filed_card"
            else:
                state["dispute_status"] = "approved"
    elif domain == "scheduling":
        if (
            event["type"] == "authorization_review"
            and state["authorization_status"] == "pending"
            and elapsed_minutes >= event["minimum_minutes"]
        ):
            if state["referral_source"] != state["required_source"]:
                state["authorization_status"] = "declined"
                state["decline_reason"] = "referral_source_not_eligible"
            else:
                state["authorization_status"] = "granted"
    elif domain == "logistics":
        if (
            event["type"] == "delivery_run_window"
            and state["shipment_status"] == "out_for_delivery"
            and elapsed_minutes >= event["minimum_minutes"]
        ):
            if state["label_address"] != state["account_address"]:
                state["shipment_status"] = "returned_to_sender"
                state["return_reason"] = "destination_record_mismatch"
            else:
                state["shipment_status"] = "delivered"
    elif domain == "energy":
        if (
            event["type"] == "billing_validation_cycle"
            and state["reading_status"] == "validating"
            and elapsed_minutes >= event["minimum_minutes"]
        ):
            if state["registered_points"] != state["actual_points"]:
                state["reading_status"] = "flagged_incomplete"
                state["flag_reason"] = "supply_points_missing_from_account"
            else:
                state["reading_status"] = "accepted"
    elif domain == "account_access":
        if (
            event["type"] == "reset_propagation_window"
            and state["access_status"] == "reset_pending"
            and elapsed_minutes >= event["minimum_minutes"]
        ):
            if state["reset_target"] != state["authentication_mode"]:
                state["access_status"] = "still_locked"
                state["lock_reason"] = "reset_applied_to_unused_credential_store"
            else:
                state["access_status"] = "restored"
    elif domain == "repair":
        if (
            event["type"] == "assessment_cycle"
            and state["claim_state"] == "in_assessment"
            and elapsed_minutes >= event["minimum_minutes"]
        ):
            if state["purchase_channel"] != state["covered_channel"]:
                state["claim_state"] = "outside_terms"
                state["decline_reason"] = "purchase_channel_not_covered"
            else:
                state["claim_state"] = "authorised"
    elif domain == "housing":
        if (
            event["type"] == "visit_window_elapsed"
            and state["work_order_status"] == "dispatched"
            and elapsed_minutes >= event["minimum_minutes"]
        ):
            if state["vendor_credentials"] != state["required_credentials"]:
                state["work_order_status"] = "access_refused"
                state["refusal_reason"] = "entry_permissions_not_valid_for_current_contract"
            else:
                state["work_order_status"] = "completed"
    elif domain == "mobile_service":
        if (
            event["type"] == "porting_window"
            and state["port_status"] == "in_progress"
            and elapsed_minutes >= event["minimum_minutes"]
        ):
            if state["ownership_record"] != state["required_record"]:
                state["port_status"] = "rejected"
                state["rejection_reason"] = "ownership_record_does_not_match_request"
            else:
                state["port_status"] = "completed"
    elif domain == "education":
        if (
            event["type"] == "registration_run"
            and state["enrolment_status"] == "processing"
            and elapsed_minutes >= event["minimum_minutes"]
        ):
            if state["prior_study_state"] != state["required_state"]:
                state["enrolment_status"] = "held_for_review"
                state["hold_reason"] = "prior_study_not_yet_evaluated"
            else:
                state["enrolment_status"] = "confirmed"
    elif domain == "motor_insurance":
        if (
            event["type"] == "assessment_run"
            and state["claim_progress"] == "assessing"
            and elapsed_minutes >= event["minimum_minutes"]
        ):
            if state["keeper_name"] != state["policy_name"]:
                state["claim_progress"] = "held_for_proof"
                state["hold_reason"] = "named_party_does_not_match_ownership"
            else:
                state["claim_progress"] = "settled"
    elif domain == "permits":
        if (
            event["type"] == "eligibility_check_run"
            and state["permit_status"] == "in_check"
            and elapsed_minutes >= event["minimum_minutes"]
        ):
            if state["proof_name"] != state["applicant_name"]:
                state["permit_status"] = "refused"
                state["refusal_reason"] = "supporting_document_names_another_occupant"
            else:
                state["permit_status"] = "issued"
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
    if domain == "banking":
        status = state["dispute_status"]
        if status == "not_filed":
            return "file_dispute"
        if status == "under_review":
            return "continue_monitoring"
        if (
            status == "returned_unmatched"
            and state.get("charge_card") != state.get("card_on_file")
        ):
            return "reconcile_card_records"
        return "close_case"
    if domain == "scheduling":
        status = state["authorization_status"]
        if status == "not_requested":
            return "request_authorization"
        if status == "pending":
            return "continue_monitoring"
        if (
            status == "declined"
            and state.get("referral_source") != state.get("required_source")
        ):
            return "obtain_qualifying_referral"
        return "close_case"
    if domain == "logistics":
        status = state["shipment_status"]
        if status == "at_facility":
            return "schedule_redelivery"
        if status == "out_for_delivery":
            return "continue_monitoring"
        if (
            status == "returned_to_sender"
            and state.get("label_address") != state.get("account_address")
        ):
            return "correct_destination_record"
        return "close_case"
    if domain == "energy":
        status = state["reading_status"]
        if status == "not_submitted":
            return "submit_reading"
        if status == "validating":
            return "continue_monitoring"
        if (
            status == "flagged_incomplete"
            and state.get("registered_points") != state.get("actual_points")
        ):
            return "register_all_supply_points"
        return "close_case"
    if domain == "account_access":
        status = state["access_status"]
        if status == "locked":
            return "initiate_credential_reset"
        if status == "reset_pending":
            return "continue_monitoring"
        if (
            status == "still_locked"
            and state.get("reset_target") != state.get("authentication_mode")
        ):
            return "engage_identity_provider"
        return "close_case"
    if domain == "repair":
        status = state["claim_state"]
        if status == "not_opened":
            return "open_cover_claim"
        if status == "in_assessment":
            return "continue_monitoring"
        if (
            status == "outside_terms"
            and state.get("purchase_channel") != state.get("covered_channel")
        ):
            return "use_retailer_route"
        return "close_case"
    if domain == "housing":
        status = state["work_order_status"]
        if status == "not_created":
            return "dispatch_maintenance_visit"
        if status == "dispatched":
            return "continue_monitoring"
        if (
            status == "access_refused"
            and state.get("vendor_credentials") != state.get("required_credentials")
        ):
            return "reissue_access_authority"
        return "close_case"
    if domain == "mobile_service":
        status = state["port_status"]
        if status == "not_started":
            return "submit_port_request"
        if status == "in_progress":
            return "continue_monitoring"
        if (
            status == "rejected"
            and state.get("ownership_record") != state.get("required_record")
        ):
            return "align_ownership_record"
        return "close_case"
    if domain == "education":
        status = state["enrolment_status"]
        if status == "not_submitted":
            return "submit_enrolment"
        if status == "processing":
            return "continue_monitoring"
        if (
            status == "held_for_review"
            and state.get("prior_study_state") != state.get("required_state")
        ):
            return "request_prior_study_assessment"
        return "close_case"
    if domain == "motor_insurance":
        status = state["claim_progress"]
        if status == "not_lodged":
            return "lodge_claim"
        if status == "assessing":
            return "continue_monitoring"
        if (
            status == "held_for_proof"
            and state.get("keeper_name") != state.get("policy_name")
        ):
            return "align_policy_records"
        return "close_case"
    if domain == "permits":
        status = state["permit_status"]
        if status == "not_applied":
            return "submit_permit_application"
        if status == "in_check":
            return "continue_monitoring"
        if (
            status == "refused"
            and state.get("proof_name") != state.get("applicant_name")
        ):
            return "supply_alternative_proof"
        return "close_case"
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
    elif domain == "banking":
        status = state["dispute_status"]
        prefix = (
            "While you were away I rang the card line and they confirmed my details are in order. "
            if state.get("user_confirmed_reissue")
            else ""
        )
        if status == "returned_unmatched":
            return (
                f"{prefix}I checked back after twenty-five minutes and the case came "
                "back saying the details did not match anything on record."
            )
        if status == "under_review":
            return (
                f"{prefix}It has been twenty-five minutes and the case still says it "
                "is being looked at, with no outcome yet."
            )
        if status == "not_filed":
            return (
                f"{prefix}I came back after twenty-five minutes, but there is still "
                "nothing logged against the charge."
            )
        if status == "approved":
            return f"{prefix}I came back and the amount has been refunded. Anything else needed?"
    elif domain == "scheduling":
        status = state["authorization_status"]
        prefix = (
            "While you were away I rang the insurer and they said my cover is active. "
            if state.get("user_confirmed_coverage")
            else ""
        )
        if status == "declined":
            return (
                f"{prefix}I checked back after half an hour and the approval came back "
                "refused. I do not understand why."
            )
        if status == "pending":
            return (
                f"{prefix}It has been half an hour and the approval is still sitting "
                "there waiting for a decision."
            )
        if status == "not_requested":
            return (
                f"{prefix}I came back after half an hour, but no approval seems to have "
                "been started at all."
            )
        if status == "granted":
            return f"{prefix}I came back and the approval went through. Can we book it now?"
    elif domain == "logistics":
        status = state["shipment_status"]
        prefix = (
            "While you were away I walked to the collection point and it was not there. "
            if state.get("user_checked_collection_point")
            else ""
        )
        if status == "returned_to_sender":
            return (
                f"{prefix}I looked again after forty minutes and the tracking now says "
                "it is going back to the sender."
            )
        if status == "out_for_delivery":
            return (
                f"{prefix}It has been forty minutes and the tracking still shows it out "
                "on the round, with nothing further."
            )
        if status == "at_facility":
            return (
                f"{prefix}I came back after forty minutes and it has not left the depot at all."
            )
        if status == "delivered":
            return f"{prefix}It arrived a few minutes ago. Thank you for sorting that."
    elif domain == "energy":
        status = state["reading_status"]
        prefix = (
            "While you were away I took photographs of the dials for my own records. "
            if state.get("user_photographed_dials")
            else ""
        )
        if status == "flagged_incomplete":
            return (
                f"{prefix}I checked back after twenty-five minutes and the figure has "
                "been marked as incomplete."
            )
        if status == "validating":
            return (
                f"{prefix}It has been twenty-five minutes and the figure is still being "
                "checked, with no result yet."
            )
        if status == "not_submitted":
            return (
                f"{prefix}I came back after twenty-five minutes and nothing appears to "
                "have been sent for checking."
            )
        if status == "accepted":
            return f"{prefix}The figure went through and the statement has been corrected."
    elif domain == "account_access":
        status = state["access_status"]
        prefix = (
            "While you were away I tried the recovery contact myself and it made no difference. "
            if state.get("user_tried_recovery_contact")
            else ""
        )
        if status == "still_locked":
            return (
                f"{prefix}I waited twenty minutes and tried again, and it still will not "
                "let me in at the first screen."
            )
        if status == "reset_pending":
            return (
                f"{prefix}It has been twenty minutes and the reset still has not come "
                "through to me."
            )
        if status == "locked":
            return (
                f"{prefix}I came back after twenty minutes and no reset was ever started."
            )
        if status == "restored":
            return f"{prefix}I am back in now. Thank you for the help."
    elif domain == "repair":
        status = state["claim_state"]
        prefix = (
            "While you were away I dug out the original paperwork from the drawer. "
            if state.get("user_located_paperwork")
            else ""
        )
        if status == "outside_terms":
            return (
                f"{prefix}I heard back after half an hour and they said it falls outside "
                "what is covered."
            )
        if status == "in_assessment":
            return (
                f"{prefix}It has been half an hour and it is still with the assessors, "
                "with no answer yet."
            )
        if status == "not_opened":
            return (
                f"{prefix}I came back after half an hour and nothing seems to have been "
                "opened for it."
            )
        if status == "authorised":
            return f"{prefix}It has been approved and they are arranging the repair."
    elif domain == "housing":
        status = state["work_order_status"]
        prefix = (
            "While you were away I asked my neighbour to be around to let someone in. "
            if state.get("user_arranged_neighbour_access")
            else ""
        )
        if status == "access_refused":
            return (
                f"{prefix}Someone did turn up after thirty-five minutes but they could "
                "not get into the building, so they left again."
            )
        if status == "dispatched":
            return (
                f"{prefix}It has been thirty-five minutes and the job still shows as "
                "sent out, but nobody has arrived."
            )
        if status == "not_created":
            return (
                f"{prefix}I came back after thirty-five minutes and no job appears to "
                "have been raised at all."
            )
        if status == "completed":
            return f"{prefix}Someone came and the heating is working again now."
    elif domain == "mobile_service":
        status = state["port_status"]
        prefix = (
            "While you were away I rang the old network and they said nothing is blocking it. "
            if state.get("user_called_old_network")
            else ""
        )
        if status == "rejected":
            return (
                f"{prefix}I checked back after half an hour and the transfer has come "
                "back refused. My old number still is not working here."
            )
        if status == "in_progress":
            return (
                f"{prefix}It has been half an hour and the transfer still shows as "
                "running, with nothing decided."
            )
        if status == "not_started":
            return (
                f"{prefix}I came back after half an hour and no transfer seems to have "
                "been started at all."
            )
        if status == "completed":
            return f"{prefix}It has gone through and my number works now. Thank you."
    elif domain == "education":
        status = state["enrolment_status"]
        prefix = (
            "While you were away I emailed the records office for my own peace of mind. "
            if state.get("user_emailed_office")
            else ""
        )
        if status == "held_for_review":
            return (
                f"{prefix}I checked back after half an hour and my place is being held "
                "back for someone to look at."
            )
        if status == "processing":
            return (
                f"{prefix}It has been half an hour and it still says it is going "
                "through, with no result."
            )
        if status == "not_submitted":
            return (
                f"{prefix}I came back after half an hour and nothing has been put "
                "through for me at all."
            )
        if status == "confirmed":
            return f"{prefix}It is confirmed now and my modules are showing. Thank you."
    elif domain == "motor_insurance":
        status = state["claim_progress"]
        prefix = (
            "While you were away I sent in photographs of the damage myself. "
            if state.get("user_sent_photographs")
            else ""
        )
        if status == "held_for_proof":
            return (
                f"{prefix}I heard back after thirty-five minutes and they are holding "
                "it until I can prove something about the car."
            )
        if status == "assessing":
            return (
                f"{prefix}It has been thirty-five minutes and it is still being looked "
                "at, with no decision."
            )
        if status == "not_lodged":
            return (
                f"{prefix}I came back after thirty-five minutes and nothing appears to "
                "have been lodged."
            )
        if status == "settled":
            return f"{prefix}It has been settled and the repair is being arranged."
    elif domain == "permits":
        status = state["permit_status"]
        prefix = (
            "While you were away I called in at the local office to ask about it. "
            if state.get("user_visited_office")
            else ""
        )
        if status == "refused":
            return (
                f"{prefix}I checked back after twenty-five minutes and the application "
                "has been turned down."
            )
        if status == "in_check":
            return (
                f"{prefix}It has been twenty-five minutes and it still says it is being "
                "checked, with no outcome."
            )
        if status == "not_applied":
            return (
                f"{prefix}I came back after twenty-five minutes and no application seems "
                "to exist yet."
            )
        if status == "issued":
            return f"{prefix}It has been approved and the permit is on its way."
    raise InvalidStateError(f"No observation rule for {domain}: {state}")
