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
        "Briefly acknowledge the user's frustration or experienced impact before proceeding.",
    ),
    style(
        "acknowledge_urgency",
        "Acknowledge the time pressure and prioritize the immediate next step.",
    ),
    style(
        "clarify_and_reassure",
        "Briefly clarify the situation and reassure the user before proceeding.",
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
        "clue_ablation_text": "I am not sure; I do not have that detail available.",
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
        "clue_ablation_text": "I am not sure; I do not have the account-history detail available.",
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
        "clue_ablation_text": "I am not sure; I do not have the rest of the itinerary available.",
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
    "bank": {
        "domain": "banking",
        "clue": "Worth mentioning: my card was reissued a few weeks ago after a skimming alert.",
        "clue_prompt": "Has anything about the card itself changed before this charge?",
        "clue_answer": "the card was reissued after a skimming alert",
        "clue_ablation_text": "I am not sure; I do not have the card-history detail available.",
        "setup": [
            ("user", "Hi, there is a charge on my account that I did not make."),
            ("agent", "I can help with that. Do you see the amount and date?"),
            ("user", "Yes, it is forty-two dollars from last Tuesday."),
        ],
        "fillers": [
            ("agent", "Was the physical card in your possession that day?"),
            ("user", "Yes, it was in my wallet the whole time."),
            ("agent", "Have you shared the number with any recurring service?"),
            ("user", "Only my usual streaming subscription."),
            ("agent", "Did you travel outside your normal area recently?"),
            ("user", "No, I have been home all month."),
            ("agent", "Is the mailing address on the profile still correct?"),
            ("user", "Yes, that address is right."),
            ("agent", "Would you like alerts for every future transaction?"),
            ("user", "Yes, please turn those on."),
            ("agent", "Do you use the mobile application to check balances?"),
            ("user", "Yes, almost every day."),
            ("agent", "Were there other unfamiliar amounts on the same statement?"),
            ("user", "No, just that single one."),
            ("agent", "Is the contact number ending in six-one-eight still yours?"),
            ("user", "Yes, that number is current."),
            ("agent", "Would a paper copy of the outcome be helpful?"),
            ("user", "No, electronic is fine."),
        ],
        "pre_ff": [
            ("agent", "File the disputed amount into the automated review queue."),
            ("user", "Okay, I will wait while that goes through."),
        ],
        "initial_state": {
            "dispute_status": "not_filed",
            "dispute_attempts": 0,
            "card_on_file": "reissued",
            "charge_card": "original",
            "records_reconciled": False,
            "elapsed_minutes": 0,
            "ticket_status": "open",
            "action_history": [],
            "user_action_history": [],
            "user_confirmed_reissue": False,
        },
        "transition": {
            "elapsed_minutes": 25,
            "external_event": {
                "type": "dispute_review_cycle",
                "minimum_minutes": 25,
            },
            "user_action": {
                "action": "call_card_services",
                "at_minute": 9,
            },
        },
        "belief_schema": {
            "dispute_status": [
                "not_filed",
                "under_review",
                "returned_unmatched",
                "approved",
            ]
        },
        "revalidation_actions": ["reconcile_card_records"],
        "belief_confidence_threshold": 0.60,
        "pre_gap_actions": [
            action("file_dispute", "File the disputed amount into the automated review queue."),
            action(
                "order_replacement_card",
                "Send out another physical card before reviewing the charge.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "freeze_account",
                "Freeze the whole account before the charge is examined.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "request_merchant_receipt",
                "Ask the merchant for paperwork before opening anything.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "close_case",
                "Close the request and tell the user to watch the balance.",
                "PREMATURE_CLOSE",
            ),
        ],
        "post_gap_actions": [
            action(
                "reconcile_card_records",
                "Match the stored account identifiers against the charge before trying again.",
            ),
            action(
                "file_dispute",
                "Put the same amount through the automated queue again now.",
                "STATE_SYNC_FAILURE",
            ),
            action(
                "request_merchant_receipt",
                "Ask the merchant for paperwork about the amount.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "continue_monitoring",
                "Leave the existing entry alone and wait another interval.",
                "TIME_INFERENCE_FAILURE",
            ),
            action(
                "close_case",
                "Close the request because the review interval has passed.",
                "PREMATURE_CLOSE",
            ),
        ],
        "pre_gap_correct": "file_dispute",
        "prosody_pair": {
            "native_prosody": "frustrated",
            "high": {"prosody": "frustrated", "expected_style": "acknowledge_impact"},
            "low": {"prosody": "calm", "expected_style": "proceed_directly"},
        },
        "response_styles": COMMON_STYLES,
        "questions": [
            ("What changed about the card before the charge?", "it was reissued after a skimming alert", "clue"),
            ("What was the disputed amount?", "forty-two dollars", "filler"),
            ("What did the review return?", "it came back unmatched", "post_ff"),
        ],
    },
    "clinic": {
        "domain": "scheduling",
        "clue": "I should say the referral came from the walk-in centre, not my regular physician.",
        "clue_prompt": "Where did the referral originate?",
        "clue_answer": "a walk-in centre rather than the regular physician",
        "clue_ablation_text": "I am not sure; I do not have the referral-source detail available.",
        "setup": [
            ("user", "Hi, I am trying to book the specialist appointment I was referred for."),
            ("agent", "I can look at that. Do you have the referral date?"),
            ("user", "Yes, it was issued on the ninth."),
        ],
        "fillers": [
            ("agent", "Have you seen this specialist before?"),
            ("user", "No, this would be the first visit."),
            ("agent", "Do mornings or afternoons suit you better?"),
            ("user", "Mornings are easier for me."),
            ("agent", "Is the address on the file still where you live?"),
            ("user", "Yes, nothing has moved."),
            ("agent", "Would you like a reminder message beforehand?"),
            ("user", "Yes, a message would help."),
            ("agent", "Do you need step-free access at the building?"),
            ("user", "No, stairs are fine for me."),
            ("agent", "Are you currently taking any regular medication?"),
            ("user", "Just a vitamin supplement."),
            ("agent", "Do you have a preferred practitioner at the practice?"),
            ("user", "No, whoever is available is fine."),
            ("agent", "Is the phone number ending in three-four-zero correct?"),
            ("user", "Yes, that one is right."),
            ("agent", "Would you travel to the second site if it were sooner?"),
            ("user", "Yes, I could manage that."),
        ],
        "pre_ff": [
            ("agent", "Send the booking through for coverage approval."),
            ("user", "Okay, I will hold on while that happens."),
        ],
        "initial_state": {
            "authorization_status": "not_requested",
            "authorization_attempts": 0,
            "referral_source": "walk_in",
            "required_source": "primary_care",
            "referral_corrected": False,
            "elapsed_minutes": 0,
            "ticket_status": "open",
            "action_history": [],
            "user_action_history": [],
            "user_confirmed_coverage": False,
        },
        "transition": {
            "elapsed_minutes": 30,
            "external_event": {
                "type": "authorization_review",
                "minimum_minutes": 30,
            },
            "user_action": {
                "action": "call_insurer",
                "at_minute": 12,
            },
        },
        "belief_schema": {
            "authorization_status": [
                "not_requested",
                "pending",
                "declined",
                "granted",
            ]
        },
        "revalidation_actions": ["obtain_qualifying_referral"],
        "belief_confidence_threshold": 0.60,
        "pre_gap_actions": [
            action("request_authorization", "Send the booking through for coverage approval."),
            action(
                "book_without_authorization",
                "Reserve the slot and settle the coverage question later.",
                "ACTION_SELECTION_FAILURE",
            ),
            action(
                "offer_private_payment",
                "Move straight to a self-funded booking instead.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "contact_specialist_office",
                "Ring the specialist office before requesting anything.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "close_case",
                "Close the request and ask the user to try again later.",
                "PREMATURE_CLOSE",
            ),
        ],
        "post_gap_actions": [
            action(
                "obtain_qualifying_referral",
                "Obtain the qualifying document from the provider type the policy requires.",
            ),
            action(
                "request_authorization",
                "Put the identical booking through for approval again now.",
                "STATE_SYNC_FAILURE",
            ),
            action(
                "contact_specialist_office",
                "Ring the specialist office about the booking.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "continue_monitoring",
                "Leave the request in place and wait another interval.",
                "TIME_INFERENCE_FAILURE",
            ),
            action(
                "close_case",
                "Close the request because the review interval has passed.",
                "PREMATURE_CLOSE",
            ),
        ],
        "pre_gap_correct": "request_authorization",
        "prosody_pair": {
            "native_prosody": "confused",
            "high": {"prosody": "confused", "expected_style": "acknowledge_impact"},
            "low": {"prosody": "confident", "expected_style": "proceed_directly"},
        },
        "response_styles": COMMON_STYLES,
        "questions": [
            ("Where did the referral originate?", "a walk-in centre", "clue"),
            ("What time of day does the user prefer?", "mornings", "filler"),
            ("What did the coverage review decide?", "it was declined", "post_ff"),
        ],
    },
    "delivery": {
        "domain": "logistics",
        "clue": "Bear in mind I relocated last month, and I doubt every record caught up.",
        "clue_prompt": "Has anything about where you receive parcels changed lately?",
        "clue_answer": "the user relocated last month",
        "clue_ablation_text": "I am not sure; I cannot confirm whether every address record is current.",
        "setup": [
            ("user", "Hi, a parcel of mine says it could not be delivered."),
            ("agent", "I can check that. Do you have the tracking reference?"),
            ("user", "Yes, it begins with seven-seven-four."),
        ],
        "fillers": [
            ("agent", "Was anybody at home during the attempt?"),
            ("user", "Yes, I was in all afternoon."),
            ("agent", "Did the courier leave a card of any kind?"),
            ("user", "No, I did not find one."),
            ("agent", "Is there a secure porch or side entrance?"),
            ("user", "There is a porch, yes."),
            ("agent", "Would a neighbour accept the parcel for you?"),
            ("user", "Yes, the one next door usually would."),
            ("agent", "Is the parcel time-sensitive at all?"),
            ("user", "Somewhat, I need it this week."),
            ("agent", "Would you like notifications by message?"),
            ("user", "Yes, that would be useful."),
            ("agent", "Has this happened with earlier parcels?"),
            ("user", "Not that I can recall."),
            ("agent", "Is the contact number ending in two-nine-five current?"),
            ("user", "Yes, that is the right number."),
            ("agent", "Would a collection point be acceptable instead?"),
            ("user", "Yes, if it is nearby."),
        ],
        "pre_ff": [
            ("agent", "Book the parcel onto the next available delivery run."),
            ("user", "Okay, I will see what comes of it."),
        ],
        "initial_state": {
            "shipment_status": "at_facility",
            "delivery_attempts": 1,
            "label_address": "previous",
            "account_address": "current",
            "address_corrected": False,
            "elapsed_minutes": 0,
            "ticket_status": "open",
            "action_history": [],
            "user_action_history": [],
            "user_checked_collection_point": False,
        },
        "transition": {
            "elapsed_minutes": 40,
            "external_event": {
                "type": "delivery_run_window",
                "minimum_minutes": 40,
            },
            "user_action": {
                "action": "check_collection_point",
                "at_minute": 15,
            },
        },
        "belief_schema": {
            "shipment_status": [
                "at_facility",
                "out_for_delivery",
                "returned_to_sender",
                "delivered",
            ]
        },
        "revalidation_actions": ["correct_destination_record"],
        "belief_confidence_threshold": 0.60,
        "pre_gap_actions": [
            action("schedule_redelivery", "Book the parcel onto the next available delivery run."),
            action(
                "open_loss_claim",
                "Open a loss claim before another attempt is made.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "dispatch_replacement_goods",
                "Send out replacement goods straight away.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "contact_courier_depot",
                "Ring the depot before arranging anything else.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "close_case",
                "Close the request and ask the user to track it themselves.",
                "PREMATURE_CLOSE",
            ),
        ],
        "post_gap_actions": [
            action(
                "correct_destination_record",
                "Update the stored destination details before booking another run.",
            ),
            action(
                "schedule_redelivery",
                "Book the parcel onto another delivery run right now.",
                "STATE_SYNC_FAILURE",
            ),
            action(
                "contact_courier_depot",
                "Ring the depot about the parcel.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "continue_monitoring",
                "Leave the booking alone and wait another interval.",
                "TIME_INFERENCE_FAILURE",
            ),
            action(
                "close_case",
                "Close the request because the delivery interval has passed.",
                "PREMATURE_CLOSE",
            ),
        ],
        "pre_gap_correct": "schedule_redelivery",
        "prosody_pair": {
            "native_prosody": "urgent",
            "high": {"prosody": "urgent", "expected_style": "acknowledge_impact"},
            "low": {"prosody": "calm", "expected_style": "proceed_directly"},
        },
        "response_styles": COMMON_STYLES,
        "questions": [
            ("What changed for the user recently?", "they relocated last month", "clue"),
            ("Was anyone at home for the attempt?", "yes, all afternoon", "filler"),
            ("Where did the parcel end up?", "it went back to the sender", "post_ff"),
        ],
    },
    "utility": {
        "domain": "energy",
        "clue": "Something to note: the property has a second meter that arrived with the extension.",
        "clue_prompt": "Is there anything unusual about how the property is metered?",
        "clue_answer": "the property has a second meter",
        "clue_ablation_text": "I am not sure; I do not have the full metering detail available.",
        "setup": [
            ("user", "Hi, my latest energy statement looks far too high."),
            ("agent", "I can look into that. Do you have the account reference?"),
            ("user", "Yes, it ends in four-eight-one."),
        ],
        "fillers": [
            ("agent", "Has your household size changed this quarter?"),
            ("user", "No, still the same two of us."),
            ("agent", "Have you added any large appliance lately?"),
            ("user", "No, nothing new like that."),
            ("agent", "Is the statement paper or electronic?"),
            ("user", "Electronic, it arrives by email."),
            ("agent", "Do you pay by fixed monthly amount?"),
            ("user", "Yes, a fixed amount each month."),
            ("agent", "Would you like a breakdown by period?"),
            ("user", "Yes, that would be helpful."),
            ("agent", "Has anyone been out to the property recently?"),
            ("user", "No, nobody has visited."),
            ("agent", "Is the heating electric or gas?"),
            ("user", "It is all electric here."),
            ("agent", "Is the contact number ending in five-five-two right?"),
            ("user", "Yes, that is correct."),
            ("agent", "Would you like the outcome by email as well?"),
            ("user", "Yes, email is fine."),
        ],
        "pre_ff": [
            ("agent", "Send the figure you gave me for automated validation."),
            ("user", "Okay, I will wait to hear back."),
        ],
        "initial_state": {
            "reading_status": "not_submitted",
            "submission_attempts": 0,
            "registered_points": 1,
            "actual_points": 2,
            "points_registered": False,
            "elapsed_minutes": 0,
            "ticket_status": "open",
            "action_history": [],
            "user_action_history": [],
            "user_photographed_dials": False,
        },
        "transition": {
            "elapsed_minutes": 25,
            "external_event": {
                "type": "billing_validation_cycle",
                "minimum_minutes": 25,
            },
            "user_action": {
                "action": "photograph_dials",
                "at_minute": 10,
            },
        },
        "belief_schema": {
            "reading_status": [
                "not_submitted",
                "validating",
                "flagged_incomplete",
                "accepted",
            ]
        },
        "revalidation_actions": ["register_all_supply_points"],
        "belief_confidence_threshold": 0.60,
        "pre_gap_actions": [
            action("submit_reading", "Send the figure you gave me for automated validation."),
            action(
                "issue_refund",
                "Refund the difference before anything is validated.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "book_engineer_visit",
                "Send an engineer out before checking the figure.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "review_tariff_history",
                "Read back through old tariff rates before submitting.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "close_case",
                "Close the request and ask the user to watch the next statement.",
                "PREMATURE_CLOSE",
            ),
        ],
        "post_gap_actions": [
            action(
                "register_all_supply_points",
                "Record every supply connection on the account before validating again.",
            ),
            action(
                "submit_reading",
                "Send the identical figure for validation again now.",
                "STATE_SYNC_FAILURE",
            ),
            action(
                "review_tariff_history",
                "Read back through old tariff rates instead.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "continue_monitoring",
                "Leave the submission alone and wait another interval.",
                "TIME_INFERENCE_FAILURE",
            ),
            action(
                "close_case",
                "Close the request because the validation interval has passed.",
                "PREMATURE_CLOSE",
            ),
        ],
        "pre_gap_correct": "submit_reading",
        "prosody_pair": {
            "native_prosody": "frustrated",
            "high": {"prosody": "frustrated", "expected_style": "acknowledge_impact"},
            "low": {"prosody": "calm", "expected_style": "proceed_directly"},
        },
        "response_styles": COMMON_STYLES,
        "questions": [
            ("What is unusual about the property?", "it has a second meter", "clue"),
            ("How does the user pay?", "a fixed monthly amount", "filler"),
            ("What did validation report?", "the reading was incomplete", "post_ff"),
        ],
    },
    "saas": {
        "domain": "account_access",
        "clue": "Relevant detail: our company switched to single sign-on just before the holidays.",
        "clue_prompt": "Has the way your company handles logins changed at all?",
        "clue_answer": "the company switched to single sign-on",
        "clue_ablation_text": "I am not sure; I cannot confirm the sign-in configuration history.",
        "setup": [
            ("user", "Hi, I cannot get into my work account this morning."),
            ("agent", "I can help. Does it reject you at the first screen?"),
            ("user", "Yes, it will not take me past that point."),
        ],
        "fillers": [
            ("agent", "Have you tried a different browser?"),
            ("user", "Yes, I tried two of them."),
            ("agent", "Does the same thing happen on your phone?"),
            ("user", "Yes, exactly the same."),
            ("agent", "Are colleagues able to get in normally?"),
            ("user", "As far as I know, yes."),
            ("agent", "Did you change anything on your machine recently?"),
            ("user", "No, nothing that I noticed."),
            ("agent", "Is the address you enter the work one?"),
            ("user", "Yes, my work address."),
            ("agent", "Do you have the authenticator application installed?"),
            ("user", "Yes, it is on my phone."),
            ("agent", "Are you connected through the office network?"),
            ("user", "No, I am at home today."),
            ("agent", "Is the recovery contact ending in eight-three-seven current?"),
            ("user", "Yes, that is still current."),
            ("agent", "Would a written summary afterwards be useful?"),
            ("user", "Yes, please send one."),
        ],
        "pre_ff": [
            ("agent", "Start the standard credential reset for the account."),
            ("user", "Okay, I will try once that comes through."),
        ],
        "initial_state": {
            "access_status": "locked",
            "reset_attempts": 0,
            "authentication_mode": "federated",
            "reset_target": "local",
            "identity_provider_engaged": False,
            "elapsed_minutes": 0,
            "ticket_status": "open",
            "action_history": [],
            "user_action_history": [],
            "user_tried_recovery_contact": False,
        },
        "transition": {
            "elapsed_minutes": 20,
            "external_event": {
                "type": "reset_propagation_window",
                "minimum_minutes": 20,
            },
            "user_action": {
                "action": "try_recovery_contact",
                "at_minute": 7,
            },
        },
        "belief_schema": {
            "access_status": [
                "locked",
                "reset_pending",
                "still_locked",
                "restored",
            ]
        },
        "revalidation_actions": ["engage_identity_provider"],
        "belief_confidence_threshold": 0.60,
        "pre_gap_actions": [
            action("initiate_credential_reset", "Start the standard credential reset for the account."),
            action(
                "provision_new_account",
                "Create an entirely new account for the user instead.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "grant_temporary_bypass",
                "Hand out a temporary way around the login screen.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "clear_browser_state",
                "Have the user wipe stored browser data before anything else.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "close_case",
                "Close the request and ask the user to retry tomorrow.",
                "PREMATURE_CLOSE",
            ),
        ],
        "post_gap_actions": [
            action(
                "engage_identity_provider",
                "Take the account to the external directory team that owns the sign-in path.",
            ),
            action(
                "initiate_credential_reset",
                "Run the same credential reset over again now.",
                "STATE_SYNC_FAILURE",
            ),
            action(
                "clear_browser_state",
                "Have the user wipe stored browser data.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "continue_monitoring",
                "Leave the reset alone and wait another interval.",
                "TIME_INFERENCE_FAILURE",
            ),
            action(
                "close_case",
                "Close the request because the reset interval has passed.",
                "PREMATURE_CLOSE",
            ),
        ],
        "pre_gap_correct": "initiate_credential_reset",
        "prosody_pair": {
            "native_prosody": "urgent",
            "high": {"prosody": "urgent", "expected_style": "acknowledge_impact"},
            "low": {"prosody": "confident", "expected_style": "proceed_directly"},
        },
        "response_styles": COMMON_STYLES,
        "questions": [
            ("What changed about company logins?", "they switched to single sign-on", "clue"),
            ("Where was the user working from?", "at home", "filler"),
            ("What happened after the reset?", "the account was still locked", "post_ff"),
        ],
    },
    "warranty": {
        "domain": "repair",
        "clue": "I ought to mention we bought it as a display unit, discounted from the shop floor.",
        "clue_prompt": "How was the appliance purchased originally?",
        "clue_answer": "as a discounted display unit",
        "clue_ablation_text": "I am not sure; I do not have the original purchase detail available.",
        "setup": [
            ("user", "Hi, my washing machine has stopped draining properly."),
            ("agent", "I can look at that. Do you have the model number?"),
            ("user", "Yes, it starts with W-D-nine."),
        ],
        "fillers": [
            ("agent", "How long has it been doing this?"),
            ("user", "About four days now."),
            ("agent", "Does it make any unusual noise?"),
            ("user", "There is a low humming sound."),
            ("agent", "Have you cleaned the filter recently?"),
            ("user", "Yes, I cleared it yesterday."),
            ("agent", "Is the machine level on the floor?"),
            ("user", "Yes, it sits flat."),
            ("agent", "Is it plumbed into a standard waste pipe?"),
            ("user", "Yes, the usual arrangement."),
            ("agent", "Would weekday or weekend suit for a visit?"),
            ("user", "Weekdays are easier."),
            ("agent", "Is there parking near the property?"),
            ("user", "Yes, right outside."),
            ("agent", "Is the number ending in one-seven-four still yours?"),
            ("user", "Yes, that is mine."),
            ("agent", "Would you like the outcome confirmed in writing?"),
            ("user", "Yes, in writing please."),
        ],
        "pre_ff": [
            ("agent", "Open the cover claim and send it for assessment."),
            ("user", "Okay, I will wait to hear the outcome."),
        ],
        "initial_state": {
            "claim_state": "not_opened",
            "claim_attempts": 0,
            "purchase_channel": "display_unit",
            "covered_channel": "standard_retail",
            "retailer_route_used": False,
            "elapsed_minutes": 0,
            "ticket_status": "open",
            "action_history": [],
            "user_action_history": [],
            "user_located_paperwork": False,
        },
        "transition": {
            "elapsed_minutes": 30,
            "external_event": {
                "type": "assessment_cycle",
                "minimum_minutes": 30,
            },
            "user_action": {
                "action": "locate_paperwork",
                "at_minute": 11,
            },
        },
        "belief_schema": {
            "claim_state": [
                "not_opened",
                "in_assessment",
                "outside_terms",
                "authorised",
            ]
        },
        "revalidation_actions": ["use_retailer_route"],
        "belief_confidence_threshold": 0.60,
        "pre_gap_actions": [
            action("open_cover_claim", "Open the cover claim and send it for assessment."),
            action(
                "dispatch_engineer_now",
                "Send an engineer before any assessment happens.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "authorise_replacement",
                "Approve a whole replacement machine straight away.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "suggest_self_repair",
                "Talk the user through fixing it themselves first.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "close_case",
                "Close the request and ask the user to call back.",
                "PREMATURE_CLOSE",
            ),
        ],
        "post_gap_actions": [
            action(
                "use_retailer_route",
                "Take the repair through the seller channel that matches the original purchase route.",
            ),
            action(
                "open_cover_claim",
                "Send the identical claim for assessment again now.",
                "STATE_SYNC_FAILURE",
            ),
            action(
                "suggest_self_repair",
                "Talk the user through fixing it themselves.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "continue_monitoring",
                "Leave the claim alone and wait another interval.",
                "TIME_INFERENCE_FAILURE",
            ),
            action(
                "close_case",
                "Close the request because the assessment interval has passed.",
                "PREMATURE_CLOSE",
            ),
        ],
        "pre_gap_correct": "open_cover_claim",
        "prosody_pair": {
            "native_prosody": "confused",
            "high": {"prosody": "confused", "expected_style": "acknowledge_impact"},
            "low": {"prosody": "calm", "expected_style": "proceed_directly"},
        },
        "response_styles": COMMON_STYLES,
        "questions": [
            ("How was the appliance bought?", "as a discounted display unit", "clue"),
            ("How long has the fault lasted?", "about four days", "filler"),
            ("What did the assessment return?", "it fell outside the terms", "post_ff"),
        ],
    },
    "tenancy": {
        "domain": "housing",
        "clue": "Worth knowing: the building changed managing agents at the start of the quarter.",
        "clue_prompt": "Has anything changed about who looks after the building?",
        "clue_answer": "the building changed managing agents",
        "clue_ablation_text": "I am not sure; I cannot confirm the building-management history.",
        "setup": [
            ("user", "Hi, the heating in my flat has not worked for three days."),
            ("agent", "I am sorry about that. Can you confirm the flat number?"),
            ("user", "Yes, it is flat twelve on the third floor."),
        ],
        "fillers": [
            ("agent", "Is it the whole flat or one room?"),
            ("user", "The whole flat is cold."),
            ("agent", "Does the hot water still run?"),
            ("user", "Yes, the water is fine."),
            ("agent", "Have you checked the thermostat setting?"),
            ("user", "Yes, it is turned right up."),
            ("agent", "Is there a boiler cupboard inside the flat?"),
            ("user", "Yes, in the hallway."),
            ("agent", "Are neighbours reporting the same problem?"),
            ("user", "One of them mentioned it too."),
            ("agent", "Would daytime access be possible?"),
            ("user", "Yes, I work from home."),
            ("agent", "Is there a buzzer at the main entrance?"),
            ("user", "Yes, there is one."),
            ("agent", "Is the number ending in nine-zero-six still right?"),
            ("user", "Yes, that is my number."),
            ("agent", "Would you like a text before anyone arrives?"),
            ("user", "Yes, a text would help."),
        ],
        "pre_ff": [
            ("agent", "Raise the job and send it to the contractor rota."),
            ("user", "Okay, I will wait for someone to come."),
        ],
        "initial_state": {
            "work_order_status": "not_created",
            "dispatch_attempts": 0,
            "vendor_credentials": "expired",
            "required_credentials": "current",
            "credentials_reissued": False,
            "elapsed_minutes": 0,
            "ticket_status": "open",
            "action_history": [],
            "user_action_history": [],
            "user_arranged_neighbour_access": False,
        },
        "transition": {
            "elapsed_minutes": 35,
            "external_event": {
                "type": "visit_window_elapsed",
                "minimum_minutes": 35,
            },
            "user_action": {
                "action": "arrange_neighbour_access",
                "at_minute": 14,
            },
        },
        "belief_schema": {
            "work_order_status": [
                "not_created",
                "dispatched",
                "access_refused",
                "completed",
            ]
        },
        "revalidation_actions": ["reissue_access_authority"],
        "belief_confidence_threshold": 0.60,
        "pre_gap_actions": [
            action("dispatch_maintenance_visit", "Raise the job and send it to the contractor rota."),
            action(
                "rehouse_tenant",
                "Move the tenant elsewhere before any visit is attempted.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "authorise_full_replacement",
                "Approve a complete new heating system immediately.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "send_portable_heaters",
                "Post out portable heaters and leave it there.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "close_case",
                "Close the request and ask the tenant to report it again.",
                "PREMATURE_CLOSE",
            ),
        ],
        "post_gap_actions": [
            action(
                "reissue_access_authority",
                "Get fresh entry permissions issued for whoever now holds the contract.",
            ),
            action(
                "dispatch_maintenance_visit",
                "Send the same job to the contractor rota again now.",
                "STATE_SYNC_FAILURE",
            ),
            action(
                "send_portable_heaters",
                "Post out portable heaters instead.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "continue_monitoring",
                "Leave the job alone and wait another interval.",
                "TIME_INFERENCE_FAILURE",
            ),
            action(
                "close_case",
                "Close the request because the visit interval has passed.",
                "PREMATURE_CLOSE",
            ),
        ],
        "pre_gap_correct": "dispatch_maintenance_visit",
        "prosody_pair": {
            "native_prosody": "frustrated",
            "high": {"prosody": "frustrated", "expected_style": "acknowledge_impact"},
            "low": {"prosody": "calm", "expected_style": "proceed_directly"},
        },
        "response_styles": COMMON_STYLES,
        "questions": [
            ("What changed about the building?", "it changed managing agents", "clue"),
            ("Does the hot water still run?", "yes", "filler"),
            ("Why did the visit fail?", "the contractor could not get access", "post_ff"),
        ],
    },
    "telecom": {
        "domain": "mobile_service",
        "clue": "I should flag that I upgraded the handset through a separate reseller in the spring.",
        "clue_prompt": "How was the current arrangement originally set up?",
        "clue_answer": "through a separate reseller",
        "clue_ablation_text": "I am not sure; I do not have the handset-purchase detail available.",
        "setup": [
            ("user", "Hi, I am trying to move my number across to your network."),
            ("agent", "I can start that. Do you have the transfer code ready?"),
            ("user", "Yes, I received it by text yesterday."),
        ],
        "fillers": [
            ("agent", "Is the number currently active and in use?"),
            ("user", "Yes, I am using it right now."),
            ("agent", "Do you want to keep the same monthly bundle?"),
            ("user", "Yes, the same one is fine."),
            ("agent", "Would you like a paper bill as well?"),
            ("user", "No, online only is fine."),
            ("agent", "Is the billing address on file still correct?"),
            ("user", "Yes, that has not changed."),
            ("agent", "Do you need international calling enabled?"),
            ("user", "No, I do not need that."),
            ("agent", "Would you like data roaming switched on?"),
            ("user", "Yes, that would be useful."),
            ("agent", "Have you settled the balance with the old network?"),
            ("user", "Yes, that was cleared last week."),
            ("agent", "Is the alternative contact ending in four-zero-three current?"),
            ("user", "Yes, that one still works."),
            ("agent", "Would you like a confirmation message when it completes?"),
            ("user", "Yes, please send one."),
        ],
        "pre_ff": [
            ("agent", "Send the transfer into the automated porting queue."),
            ("user", "Okay, I will wait and see what happens."),
        ],
        "initial_state": {
            "port_status": "not_started",
            "port_attempts": 0,
            "ownership_record": "intermediary",
            "required_record": "direct",
            "ownership_aligned": False,
            "elapsed_minutes": 0,
            "ticket_status": "open",
            "action_history": [],
            "user_action_history": [],
            "user_called_old_network": False,
        },
        "transition": {
            "elapsed_minutes": 30,
            "external_event": {
                "type": "porting_window",
                "minimum_minutes": 30,
            },
            "user_action": {
                "action": "call_old_network",
                "at_minute": 13,
            },
        },
        "belief_schema": {
            "port_status": [
                "not_started",
                "in_progress",
                "rejected",
                "completed",
            ]
        },
        "revalidation_actions": ["align_ownership_record"],
        "belief_confidence_threshold": 0.60,
        "pre_gap_actions": [
            action("submit_port_request", "Send the transfer into the automated porting queue."),
            action(
                "issue_new_number",
                "Give the user a brand new number instead of moving the old one.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "ship_replacement_sim",
                "Post out another SIM before the transfer is attempted.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "verify_transfer_code",
                "Read the transfer code back once more before sending anything.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "close_case",
                "Close the request and ask the user to start again later.",
                "PREMATURE_CLOSE",
            ),
        ],
        "post_gap_actions": [
            action(
                "align_ownership_record",
                "Bring the stored account ownership details into line before trying again.",
            ),
            action(
                "submit_port_request",
                "Push the identical transfer into the queue again now.",
                "STATE_SYNC_FAILURE",
            ),
            action(
                "verify_transfer_code",
                "Read the transfer code back once more.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "continue_monitoring",
                "Leave the transfer alone and wait another interval.",
                "TIME_INFERENCE_FAILURE",
            ),
            action(
                "close_case",
                "Close the request because the transfer interval has passed.",
                "PREMATURE_CLOSE",
            ),
        ],
        "pre_gap_correct": "submit_port_request",
        "prosody_pair": {
            "native_prosody": "frustrated",
            "high": {"prosody": "frustrated", "expected_style": "acknowledge_impact"},
            "low": {"prosody": "calm", "expected_style": "proceed_directly"},
        },
        "response_styles": COMMON_STYLES,
        "questions": [
            ("How was the arrangement originally set up?", "through a separate reseller", "clue"),
            ("Was the old balance settled?", "yes, last week", "filler"),
            ("What happened to the transfer?", "it was rejected", "post_ff"),
        ],
    },
    "college": {
        "domain": "education",
        "clue": "One detail: I transferred credits from a college overseas last autumn.",
        "clue_prompt": "Is any of your prior study from outside the usual system?",
        "clue_answer": "credits transferred from overseas",
        "clue_ablation_text": "I am not sure; I do not have my prior-study records available.",
        "setup": [
            ("user", "Hi, I am trying to finish enrolling for the coming term."),
            ("agent", "I can help with that. Do you have your student reference?"),
            ("user", "Yes, it ends in six-two-two."),
        ],
        "fillers": [
            ("agent", "Have you chosen all of your modules yet?"),
            ("user", "Yes, I picked them last week."),
            ("agent", "Are you studying full time or part time?"),
            ("user", "Full time this year."),
            ("agent", "Do you need a timetable sent to you?"),
            ("user", "Yes, that would be handy."),
            ("agent", "Is your term address the same as last year?"),
            ("user", "Yes, the same place."),
            ("agent", "Have you arranged your tuition payment method?"),
            ("user", "Yes, that is all set up."),
            ("agent", "Would you like a locker on campus?"),
            ("user", "No, I do not need one."),
            ("agent", "Do you require any study support arrangements?"),
            ("user", "No, nothing like that."),
            ("agent", "Is the contact number ending in eight-one-nine right?"),
            ("user", "Yes, that is correct."),
            ("agent", "Would you like reminders before the deadline?"),
            ("user", "Yes, reminders would help."),
        ],
        "pre_ff": [
            ("agent", "Put the enrolment through the automated registration run."),
            ("user", "Okay, I will wait for it to go through."),
        ],
        "initial_state": {
            "enrolment_status": "not_submitted",
            "enrolment_attempts": 0,
            "prior_study_state": "unassessed",
            "required_state": "assessed",
            "assessment_requested": False,
            "elapsed_minutes": 0,
            "ticket_status": "open",
            "action_history": [],
            "user_action_history": [],
            "user_emailed_office": False,
        },
        "transition": {
            "elapsed_minutes": 30,
            "external_event": {
                "type": "registration_run",
                "minimum_minutes": 30,
            },
            "user_action": {
                "action": "email_records_office",
                "at_minute": 12,
            },
        },
        "belief_schema": {
            "enrolment_status": [
                "not_submitted",
                "processing",
                "held_for_review",
                "confirmed",
            ]
        },
        "revalidation_actions": ["request_prior_study_assessment"],
        "belief_confidence_threshold": 0.60,
        "pre_gap_actions": [
            action("submit_enrolment", "Put the enrolment through the automated registration run."),
            action(
                "defer_to_next_term",
                "Push the whole thing back to a later term instead.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "waive_requirements",
                "Set aside the entry requirements entirely for this student.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "reconfirm_module_choices",
                "Go back over the chosen modules before submitting.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "close_case",
                "Close the request and ask the student to try again.",
                "PREMATURE_CLOSE",
            ),
        ],
        "post_gap_actions": [
            action(
                "request_prior_study_assessment",
                "Have the earlier qualifications formally evaluated before submitting again.",
            ),
            action(
                "submit_enrolment",
                "Send the identical enrolment through the run again now.",
                "STATE_SYNC_FAILURE",
            ),
            action(
                "reconfirm_module_choices",
                "Go back over the chosen modules instead.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "continue_monitoring",
                "Leave the enrolment alone and wait another interval.",
                "TIME_INFERENCE_FAILURE",
            ),
            action(
                "close_case",
                "Close the request because the registration interval has passed.",
                "PREMATURE_CLOSE",
            ),
        ],
        "pre_gap_correct": "submit_enrolment",
        "prosody_pair": {
            "native_prosody": "confused",
            "high": {"prosody": "confused", "expected_style": "acknowledge_impact"},
            "low": {"prosody": "confident", "expected_style": "proceed_directly"},
        },
        "response_styles": COMMON_STYLES,
        "questions": [
            ("Where did the earlier study come from?", "a college overseas", "clue"),
            ("Is the student full time or part time?", "full time", "filler"),
            ("What happened to the enrolment?", "it was held for review", "post_ff"),
        ],
    },
    "motor": {
        "domain": "motor_insurance",
        "clue": "I ought to say the vehicle is registered to my partner, not to me.",
        "clue_prompt": "Whose name is on the ownership paperwork?",
        "clue_answer": "the partner, not the caller",
        "clue_ablation_text": "I am not sure; I do not have the ownership paperwork available.",
        "setup": [
            ("user", "Hi, I need to report some damage to my car from this morning."),
            ("agent", "I am sorry to hear that. Was anybody injured?"),
            ("user", "No, thankfully everyone is fine."),
        ],
        "fillers": [
            ("agent", "Where did the incident take place?"),
            ("user", "In a supermarket car park."),
            ("agent", "Was another driver involved?"),
            ("user", "Yes, but they left before I could speak to them."),
            ("agent", "Did anybody witness what happened?"),
            ("user", "One person nearby saw it."),
            ("agent", "Is the car still driveable?"),
            ("user", "Yes, it drives, but the wing is dented."),
            ("agent", "Have you reported it to the authorities?"),
            ("user", "Yes, I did that this morning."),
            ("agent", "Do you have a preferred repair garage?"),
            ("user", "No, whichever one you recommend."),
            ("agent", "Would you need a courtesy car meanwhile?"),
            ("user", "Yes, that would help a lot."),
            ("agent", "Is the number ending in seven-six-five still yours?"),
            ("user", "Yes, that is right."),
            ("agent", "Would you like updates by message?"),
            ("user", "Yes, messages are fine."),
        ],
        "pre_ff": [
            ("agent", "Lodge the report into the automated assessment run."),
            ("user", "Okay, I will wait to hear back."),
        ],
        "initial_state": {
            "claim_progress": "not_lodged",
            "lodge_attempts": 0,
            "keeper_name": "other_party",
            "policy_name": "caller",
            "records_aligned": False,
            "elapsed_minutes": 0,
            "ticket_status": "open",
            "action_history": [],
            "user_action_history": [],
            "user_sent_photographs": False,
        },
        "transition": {
            "elapsed_minutes": 35,
            "external_event": {
                "type": "assessment_run",
                "minimum_minutes": 35,
            },
            "user_action": {
                "action": "send_photographs",
                "at_minute": 16,
            },
        },
        "belief_schema": {
            "claim_progress": [
                "not_lodged",
                "assessing",
                "held_for_proof",
                "settled",
            ]
        },
        "revalidation_actions": ["align_policy_records"],
        "belief_confidence_threshold": 0.60,
        "pre_gap_actions": [
            action("lodge_claim", "Lodge the report into the automated assessment run."),
            action(
                "declare_total_loss",
                "Write the car off before anything has been assessed.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "authorise_immediate_repair",
                "Approve the garage work before the report is lodged.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "collect_witness_statement",
                "Chase the bystander for a statement before lodging anything.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "close_case",
                "Close the report and ask the caller to get in touch later.",
                "PREMATURE_CLOSE",
            ),
        ],
        "post_gap_actions": [
            action(
                "align_policy_records",
                "Bring the policy paperwork into line with who legally owns the car.",
            ),
            action(
                "lodge_claim",
                "Put the identical report through the assessment run again now.",
                "STATE_SYNC_FAILURE",
            ),
            action(
                "collect_witness_statement",
                "Chase the bystander for a statement instead.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "continue_monitoring",
                "Leave the report alone and wait another interval.",
                "TIME_INFERENCE_FAILURE",
            ),
            action(
                "close_case",
                "Close the report because the assessment interval has passed.",
                "PREMATURE_CLOSE",
            ),
        ],
        "pre_gap_correct": "lodge_claim",
        "prosody_pair": {
            "native_prosody": "urgent",
            "high": {"prosody": "urgent", "expected_style": "acknowledge_impact"},
            "low": {"prosody": "calm", "expected_style": "proceed_directly"},
        },
        "response_styles": COMMON_STYLES,
        "questions": [
            ("Whose name is on the ownership paperwork?", "the partner", "clue"),
            ("Where did the incident happen?", "a supermarket car park", "filler"),
            ("What happened to the report?", "it was held pending proof", "post_ff"),
        ],
    },
    "permit": {
        "domain": "permits",
        "clue": "Worth saying the tenancy paperwork is in the name of my flatmate, not mine.",
        "clue_prompt": "Whose name is on the household documents?",
        "clue_answer": "the flatmate, not the caller",
        "clue_ablation_text": "I am not sure; I do not have the household documents available.",
        "setup": [
            ("user", "Hi, I am applying for a resident parking permit."),
            ("agent", "I can take you through that. Do you have the property reference?"),
            ("user", "Yes, it ends in three-one-seven."),
        ],
        "fillers": [
            ("agent", "How many vehicles need covering?"),
            ("user", "Just the one."),
            ("agent", "Do you know the registration plate?"),
            ("user", "Yes, I have it written down here."),
            ("agent", "Would you like an annual or monthly permit?"),
            ("user", "Annual would be better."),
            ("agent", "Do you need a visitor allowance as well?"),
            ("user", "No, just the one permit."),
            ("agent", "Is the vehicle kept at the property overnight?"),
            ("user", "Yes, every night."),
            ("agent", "Would you like the permit posted or collected?"),
            ("user", "Posted is easier for me."),
            ("agent", "Have you held a permit in this zone before?"),
            ("user", "No, this is my first one."),
            ("agent", "Is the number ending in two-four-eight still current?"),
            ("user", "Yes, that is current."),
            ("agent", "Would you like a receipt by email?"),
            ("user", "Yes, email please."),
        ],
        "pre_ff": [
            ("agent", "Send the application into the automated eligibility check."),
            ("user", "Okay, I will wait for the outcome."),
        ],
        "initial_state": {
            "permit_status": "not_applied",
            "application_attempts": 0,
            "proof_name": "other_occupant",
            "applicant_name": "caller",
            "alternative_proof_supplied": False,
            "elapsed_minutes": 0,
            "ticket_status": "open",
            "action_history": [],
            "user_action_history": [],
            "user_visited_office": False,
        },
        "transition": {
            "elapsed_minutes": 25,
            "external_event": {
                "type": "eligibility_check_run",
                "minimum_minutes": 25,
            },
            "user_action": {
                "action": "visit_local_office",
                "at_minute": 10,
            },
        },
        "belief_schema": {
            "permit_status": [
                "not_applied",
                "in_check",
                "refused",
                "issued",
            ]
        },
        "revalidation_actions": ["supply_alternative_proof"],
        "belief_confidence_threshold": 0.60,
        "pre_gap_actions": [
            action("submit_permit_application", "Send the application into the automated eligibility check."),
            action(
                "issue_temporary_permit",
                "Hand out a temporary permit before any check is run.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "escalate_to_appeals",
                "Send the whole thing straight to the appeals team.",
                "PREMATURE_ESCALATION",
            ),
            action(
                "reconfirm_vehicle_plate",
                "Read the plate back once more before applying.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "close_case",
                "Close the request and ask the caller to apply again later.",
                "PREMATURE_CLOSE",
            ),
        ],
        "post_gap_actions": [
            action(
                "supply_alternative_proof",
                "Provide a different document that shows the applicant lives at the address.",
            ),
            action(
                "submit_permit_application",
                "Send the identical application through the check again now.",
                "STATE_SYNC_FAILURE",
            ),
            action(
                "reconfirm_vehicle_plate",
                "Read the plate back once more instead.",
                "EARLY_CLUE_LOSS",
            ),
            action(
                "continue_monitoring",
                "Leave the application alone and wait another interval.",
                "TIME_INFERENCE_FAILURE",
            ),
            action(
                "close_case",
                "Close the request because the checking interval has passed.",
                "PREMATURE_CLOSE",
            ),
        ],
        "pre_gap_correct": "submit_permit_application",
        "prosody_pair": {
            "native_prosody": "calm",
            "high": {"prosody": "urgent", "expected_style": "acknowledge_impact"},
            "low": {"prosody": "calm", "expected_style": "proceed_directly"},
        },
        "response_styles": COMMON_STYLES,
        "questions": [
            ("Whose name is on the household documents?", "the flatmate", "clue"),
            ("How many vehicles need covering?", "just one", "filler"),
            ("What happened to the application?", "it was refused", "post_ff"),
        ],
    },
}


# High-affect deliveries require category-specific behavior.  This is applied
# once at template load so every generated scenario contains an explicit gold
# mapping rather than collapsing urgency, frustration, and confusion into one
# generic response.
HIGH_STYLE_BY_PROSODY = {
    "frustrated": "acknowledge_impact",
    "urgent": "acknowledge_urgency",
    "confused": "clarify_and_reassure",
}
for _template in TEMPLATES.values():
    _high = _template["prosody_pair"]["high"]
    _high["expected_style"] = HIGH_STYLE_BY_PROSODY[_high["prosody"]]
