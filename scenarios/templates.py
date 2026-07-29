"""Meaning-level task templates for the closed-loop benchmark.

Templates initialize hidden state and declare symbolic tools. Post-gap state is
never embedded here: ``dual_audio.core.environment.transition`` computes it.
Public action descriptions avoid repeating clue wording, and the runner exposes
only randomized option labels.
"""


def action(name, description, *failure_tags):
    """Create one private action/public description/multilabel specification."""

    return {
        "action": name,
        "description": description,
        "failure_tags": list(failure_tags),
    }


def style(name, description):
    """Create a secondary response-style choice used by prosodic pairs."""

    return {"style": name, "description": description}


TAGS = {
    "EARLY_CLUE_LOSS": "The selected action is attractive when the early clue is unavailable or unused.",
    "STATE_SYNC_FAILURE": "The action treats the pre-gap world as if it still held after time advanced.",
    "TIME_INFERENCE_FAILURE": "The action fails to use elapsed time when interpreting the observation.",
    "REPEATED_ACTION": "The action repeats a step already attempted without a new justification.",
    "PREMATURE_CLOSE": "The action closes an interaction whose state is unresolved.",
    "PREMATURE_ESCALATION": "The action escalates before supported diagnostic or policy steps are exhausted.",
    "ACTION_SELECTION_FAILURE": "The action is inconsistent with the current state but has no narrower failure label.",
    "PROSODY_GROUNDING_FAILURE": "The response approach does not match the audible delivery.",
    "BELIEF_REPORT_INVALID": "One or more required state-belief distributions or revalidation flags are missing or malformed.",
    "STATE_BELIEF_ERROR": "At least one required checkpoint assigns its highest probability to the wrong hidden state.",
}


COMMON_STYLES = [
    style(
        "acknowledge_impact",
        "Briefly acknowledge the user's impact or urgency before proceeding.",
    ),
    style(
        "proceed_directly",
        "Proceed directly and neutrally to the next operational step.",
    ),
]


TEMPLATES = {
    "router": {
        "domain": "tech_support",
        "clue": "One thing I remember: this all started right after we had a power outage last week.",
        "clue_prompt": "Was there any event around the time the problem first began?",
        "clue_answer": "a power outage",
        "clue_ablation_text": "No, I do not remember any event around when it began.",
        "setup": [
            ("user", "Hi, my router keeps dropping the connection every few minutes."),
            ("agent", "Sorry to hear that. How long has this been happening?"),
            ("user", "About a week now. I work from home, so it is disruptive."),
        ],
        "fillers": [
            ("agent", "Have you tried restarting the router?"),
            ("user", "Yes, I restarted it once already. It came back up but still drops."),
            ("agent", "Is the issue on wireless only, or wired too?"),
            ("user", "Both. Even my desktop on ethernet loses connection."),
            ("agent", "Have you moved it away from possible wireless interference?"),
            ("user", "Yes, and that made no difference."),
            ("agent", "What do the lights do when the connection drops?"),
            ("user", "The internet light goes orange for a bit, then back to green."),
            ("agent", "Does the unit itself ever lose power?"),
            ("user", "No, it never fully turns off."),
            ("agent", "Do all devices drop at the same time?"),
            ("user", "Yes. Phones, TV, and laptop all lose it together."),
            ("agent", "Did your provider report a service interruption?"),
            ("user", "Their status page shows nothing in my area."),
            ("agent", "Can another nearby customer on the same service connect normally?"),
            ("user", "Yes, my neighbor uses the same provider and hers is fine."),
            ("agent", "Have any cables or ports been changed recently?"),
            ("user", "No, the cabling is exactly as it was before."),
        ],
        "pre_ff": [
            ("agent", "Begin the guided software maintenance procedure."),
            ("user", "Okay, I have followed that step."),
        ],
        "initial_state": {
            "restart_attempts": 1,
            "firmware_status": "not_started",
            "firmware_progress": 0,
            "maintenance_attempts": 0,
            "config_integrity": "corrupted",
            "configuration_inspected": False,
            "elapsed_minutes": 0,
            "ticket_status": "open",
            "action_history": [],
            "user_action_history": [],
        },
        "transition": {
            "elapsed_minutes": 30,
            "external_event": {
                "type": "maintenance_window_elapsed",
                "minimum_minutes": 30,
                "stuck_percent": 47,
            },
            "user_action": {
                "action": "power_cycle_during_maintenance",
                "at_minute": 10,
            },
        },
        "belief_schema": {
            "firmware_status": [
                "not_started",
                "updating",
                "stuck",
                "completed",
                "interrupted",
            ]
        },
        "revalidation_actions": ["inspect_persistent_state"],
        "belief_confidence_threshold": 0.60,
        "pre_gap_actions": [
            action("run_maintenance", "Begin the guided software maintenance procedure."),
            action(
                "repeat_power_cycle",
                "Run the basic power recovery procedure one more time.",
                "REPEATED_ACTION",
            ),
            action(
                "inspect_upstream_service",
                "Investigate the upstream service path before changing the device.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "replace_hardware",
                "Escalate immediately to a hardware replacement.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "close_case",
                "Close the case and ask the user to monitor it independently.",
                "PREMATURE_CLOSE",
            ),
        ],
        "post_gap_actions": [
            action(
                "inspect_persistent_state",
                "Inspect persistent device settings for an inconsistent state.",
            ),
            action(
                "run_maintenance",
                "Run the guided software maintenance procedure now.",
                "STATE_SYNC_FAILURE",
            ),
            action(
                "repeat_power_cycle",
                "Repeat the basic power recovery procedure.",
                "REPEATED_ACTION",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "continue_monitoring",
                "Leave the current process alone and monitor it for another interval.",
                "TIME_INFERENCE_FAILURE",
            ),
            action(
                "close_case",
                "Close the case because sufficient time has passed.",
                "PREMATURE_CLOSE",
            ),
        ],
        "pre_gap_correct": "run_maintenance",
        "prosody_pair": {
            "native_prosody": "frustrated",
            "high": {
                "prosody": "frustrated",
                "expected_style": "acknowledge_impact",
            },
            "low": {"prosody": "calm", "expected_style": "proceed_directly"},
        },
        "response_styles": COMMON_STYLES,
        "questions": [
            ("What event happened when the router problem began?", "a power outage", "clue"),
            ("Had the router already been restarted?", "yes, once", "filler"),
            ("What percentage did the maintenance reach?", "47 percent", "post_ff"),
        ],
    },
    "pharmacy": {
        "domain": "pharmacy",
        "clue": "My coverage is switching over; the replacement plan started on the first of this month.",
        "clue_prompt": "Has anything about the account or coverage changed recently?",
        "clue_answer": "a replacement insurance plan began this month",
        "clue_ablation_text": "No, nothing about the account comes to mind.",
        "setup": [
            ("user", "Hi, I am calling to refill my blood pressure prescription."),
            ("agent", "Can I get your date of birth to open the profile?"),
            ("user", "It is March twelfth, nineteen seventy-one."),
        ],
        "fillers": [
            ("agent", "Has the dosage changed recently?"),
            ("user", "No, it is the same ten milligram dose."),
            ("agent", "Would you like pickup or delivery?"),
            ("user", "Pickup is fine."),
            ("agent", "Do you need any other prescriptions refilled?"),
            ("user", "No, just this one."),
            ("agent", "Is Doctor Patel still the prescriber?"),
            ("user", "Yes, Doctor Patel is still my doctor."),
            ("agent", "Is the phone number ending in four-two-two-one current?"),
            ("user", "Yes, that is still my number."),
            ("agent", "Are there any new allergies to record?"),
            ("user", "No new allergies."),
            ("agent", "Would you like a text when the order is ready?"),
            ("user", "Yes, a text is fine."),
            ("agent", "Is the generic version acceptable?"),
            ("user", "Yes, generic is fine."),
            ("agent", "Is the pickup location on Main Street still convenient?"),
            ("user", "Yes, I am nearby."),
        ],
        "pre_ff": [
            ("agent", "Submit the order to the automated claim process."),
            ("user", "Okay, I will wait while you handle that."),
        ],
        "initial_state": {
            "prescription_status": "valid",
            "claim_status": "not_submitted",
            "claim_attempts": 0,
            "active_plan": "plan_b",
            "billing_plan": "plan_a",
            "billing_profile_reviewed": False,
            "elapsed_minutes": 0,
            "ticket_status": "open",
            "action_history": [],
            "user_action_history": [],
            "user_verified_active_plan": False,
        },
        "transition": {
            "elapsed_minutes": 20,
            "external_event": {
                "type": "claim_processor_cycle",
                "minimum_minutes": 20,
            },
            "user_action": {
                "action": "contact_plan_provider",
                "at_minute": 8,
            },
        },
        "belief_schema": {
            "claim_status": [
                "not_submitted",
                "processing",
                "rejected",
                "approved",
            ]
        },
        "revalidation_actions": ["review_account_configuration"],
        "belief_confidence_threshold": 0.60,
        "pre_gap_actions": [
            action("submit_claim", "Submit the order to the automated claim process."),
            action(
                "contact_prescriber",
                "Pause and contact the prescriber for a new order.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "apply_alternate_payment",
                "Bypass the normal transaction and offer another payment route.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "continue_monitoring",
                "Wait without submitting anything yet.",
                "ACTION_SELECTION_FAILURE",
            ),
            action(
                "close_case",
                "Close the request without sending the order.",
                "PREMATURE_CLOSE",
            ),
        ],
        "post_gap_actions": [
            action(
                "review_account_configuration",
                "Review the account information used by the automated transaction before retrying.",
            ),
            action(
                "submit_claim",
                "Send the same transaction through the automated process now.",
                "STATE_SYNC_FAILURE",
            ),
            action(
                "contact_prescriber",
                "Ask the prescriber to issue a replacement order.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "continue_monitoring",
                "Wait another interval for the existing transaction.",
                "TIME_INFERENCE_FAILURE",
            ),
            action(
                "close_case",
                "Close the request because processing time has elapsed.",
                "PREMATURE_CLOSE",
            ),
        ],
        "pre_gap_correct": "submit_claim",
        "prosody_pair": {
            "native_prosody": "confused",
            "high": {
                "prosody": "confused",
                "expected_style": "acknowledge_impact",
            },
            "low": {"prosody": "confident", "expected_style": "proceed_directly"},
        },
        "response_styles": COMMON_STYLES,
        "questions": [
            ("What account change did the user mention?", "a replacement plan began this month", "clue"),
            ("Who is the prescriber?", "Doctor Patel", "filler"),
            ("What happened to the transaction?", "it was denied", "post_ff"),
        ],
    },
    "flight": {
        "domain": "travel",
        "clue": "Keep in mind I have another flight out of Denver, and there are only ninety minutes between them.",
        "clue_prompt": "Is this trip ending in Denver, or is there another segment afterward?",
        "clue_answer": "a 90-minute onward connection in Denver",
        "clue_ablation_text": "Denver is the only part of the trip I need help with right now.",
        "setup": [
            ("user", "Hi, I am checking on my flight to Denver this afternoon."),
            ("agent", "I see the two-fifteen departure. Is that the flight you mean?"),
            ("user", "Yes. I want to make sure everything is on track."),
        ],
        "fillers": [
            ("agent", "Are you checking any bags?"),
            ("user", "Just one checked bag."),
            ("agent", "Do you already have a seat assignment?"),
            ("user", "Yes, fourteen C, an aisle."),
            ("agent", "The security wait is about twenty minutes. Are you leaving soon?"),
            ("user", "Yes, I am heading to the airport shortly."),
            ("agent", "Would you like gate-change notifications by text?"),
            ("user", "Yes, that would help."),
            ("agent", "Do you have dietary or accessibility needs?"),
            ("user", "No, nothing like that."),
            ("agent", "Is the rewards number ending in nine-nine-three yours?"),
            ("user", "Yes, that is mine."),
            ("agent", "Does anything else on the reservation look wrong?"),
            ("user", "No, everything else looks right."),
            ("agent", "Do you need directions to the departure terminal?"),
            ("user", "No, I know where to go."),
            ("agent", "Is the contact phone number on the booking current?"),
            ("user", "Yes, it is current."),
        ],
        "pre_ff": [
            ("agent", "Enable active monitoring for changes to the itinerary."),
            ("user", "Okay, I will watch for what happens."),
        ],
        "initial_state": {
            "flight_status": "on_time",
            "departure_delay_minutes": 0,
            "layover_minutes": 90,
            "connection_status": "at_risk_if_delayed",
            "monitoring_enabled": False,
            "elapsed_minutes": 0,
            "ticket_status": "open",
            "action_history": [],
            "user_action_history": [],
            "user_rebooked_onward_segment": False,
        },
        "transition": {
            "elapsed_minutes": 45,
            "external_event": {"type": "departure_delay", "delay_minutes": 120},
            "user_action": {
                "action": "self_protect_onward_segment",
                "at_minute": 20,
            },
        },
        "belief_schema": {
            "connection_status": [
                "at_risk_if_delayed",
                "missed",
                "protected",
                "viable",
            ]
        },
        "revalidation_actions": ["enable_itinerary_monitoring"],
        "belief_confidence_threshold": 0.60,
        "pre_gap_actions": [
            action(
                "enable_itinerary_monitoring",
                "Enable active monitoring for changes to the itinerary.",
            ),
            action(
                "protect_onward_segment",
                "Change the later segment immediately despite the current on-time status.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "change_departing_segment",
                "Replace the current departure even though it is still on time.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "offer_service_recovery",
                "Offer disruption compensation before a disruption occurs.",
                "ACTION_SELECTION_FAILURE",
            ),
            action(
                "close_case",
                "Close the request without monitoring for changes.",
                "PREMATURE_CLOSE",
            ),
        ],
        "post_gap_actions": [
            action(
                "protect_onward_segment",
                "Protect the later segment now and offer a compatible alternative.",
            ),
            action(
                "enable_itinerary_monitoring",
                "Continue monitoring the existing itinerary without changing it.",
                "TIME_INFERENCE_FAILURE",
                "STATE_SYNC_FAILURE",
            ),
            action(
                "change_departing_segment",
                "Work only on the delayed departure and leave later segments unchanged.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "offer_service_recovery",
                "Offer disruption compensation without changing the itinerary.",
                "STATE_SYNC_FAILURE",
            ),
            action(
                "close_case",
                "Confirm the delay and close the request.",
                "PREMATURE_CLOSE",
            ),
        ],
        "pre_gap_correct": "enable_itinerary_monitoring",
        "prosody_pair": {
            "native_prosody": "calm",
            "high": {
                "prosody": "urgent",
                "expected_style": "acknowledge_impact",
            },
            "low": {"prosody": "calm", "expected_style": "proceed_directly"},
        },
        "response_styles": COMMON_STYLES,
        "questions": [
            ("How much time is there between the flights?", "90 minutes", "clue"),
            ("What seat is assigned?", "14C", "filler"),
            ("How long is the delay?", "120 minutes", "post_ff"),
        ],
    },
}
