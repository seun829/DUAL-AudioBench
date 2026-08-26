"""Causal counterfactual design for schema v0.5.

Each domain has two balanced branches.  The visible conversations are identical
apart from one early clue, while that clue determines whether the automated
transition succeeds or reaches a domain-specific repair state.  The resumed
observation deliberately withholds the terminal result for the standard event
conditions, so the clue is necessary for the post-gap belief and action.
"""

from __future__ import annotations


CAUSAL_DESIGNS = {
    "router": {
        "clue_prompt": "What did the saved-configuration check report before this began?",
        "rule_turns": [
            (
                "agent",
                "The maintenance cycle completes only when the saved configuration is intact; a corrupted configuration makes it stall.",
            ),
            ("user", "Understood; I checked that detail earlier."),
        ],
        "outcome_variable": "firmware_status",
        "hidden_outcomes": ["stuck", "completed"],
        "ambiguous_observation": (
            "Thirty minutes have passed and the maintenance cycle ended, but the result display is blank. "
            "Based on the configuration detail I gave earlier, what should we do next?"
        ),
        "causal_definitions": {
            "misaligned": "the saved configuration is corrupted, so maintenance will stall",
            "aligned": "the saved configuration is intact, so maintenance will complete",
        },
        "branches": [
            {
                "id": "misaligned",
                "clue": "The saved-configuration check reported corrupted data after last week's outage.",
                "clue_answer": "the saved configuration was corrupted",
                "state_patch": {"config_integrity": "corrupted"},
                "expected_post_action": "inspect_persistent_state",
                "post_answer": "47 percent",
            },
            {
                "id": "aligned",
                "clue": "The saved-configuration check reported intact data after last week's outage.",
                "clue_answer": "the saved configuration was intact",
                "state_patch": {"config_integrity": "intact"},
                "expected_post_action": "close_case",
                "post_answer": "100 percent",
            },
        ],
    },
    "pharmacy": {
        "clue_prompt": "Does the pharmacy billing profile match the plan that is active now?",
        "rule_turns": [
            (
                "agent",
                "The claim is approved only when the pharmacy billing profile matches the currently active plan; otherwise it is rejected.",
            ),
            ("user", "Understood; I checked which plan the profile uses."),
        ],
        "outcome_variable": "claim_status",
        "hidden_outcomes": ["rejected", "approved"],
        "ambiguous_observation": (
            "Twenty minutes have passed and processing finished, but the result code is not visible. "
            "Based on the plan detail I gave earlier, what is the next step?"
        ),
        "causal_definitions": {
            "misaligned": "the pharmacy bills an outdated plan rather than the active plan",
            "aligned": "the pharmacy billing profile matches the active plan",
        },
        "branches": [
            {
                "id": "misaligned",
                "clue": "The replacement plan is active, but the pharmacy profile still shows my previous plan.",
                "clue_answer": "the pharmacy profile still used the previous plan",
                "state_patch": {"active_plan": "plan_b", "billing_plan": "plan_a"},
                "expected_post_action": "review_account_configuration",
                "post_answer": "it was denied",
            },
            {
                "id": "aligned",
                "clue": "The replacement plan is active, and the pharmacy profile already shows that same plan.",
                "clue_answer": "the pharmacy profile matched the active plan",
                "state_patch": {"active_plan": "plan_b", "billing_plan": "plan_b"},
                "expected_post_action": "close_case",
                "post_answer": "it was approved",
            },
        ],
    },
    "flight": {
        "clue_prompt": "How much connection time is scheduled in Denver?",
        "rule_turns": [
            (
                "agent",
                "A departure delay that is at least as long as the Denver connection window makes the onward flight impossible unless it is protected.",
            ),
            ("user", "Understood; I have the connection time in front of me."),
        ],
        "outcome_variable": "connection_status",
        "hidden_outcomes": ["missed", "viable"],
        "ambiguous_observation": (
            "The departure is now delayed by 120 minutes, but the notice does not show my connection status. "
            "Based on the connection time I mentioned earlier, what should we do next?"
        ),
        "causal_definitions": {
            "misaligned": "the scheduled connection window is the short ninety-minute option",
            "aligned": "the scheduled connection window is the long four-hour option",
        },
        "branches": [
            {
                "id": "misaligned",
                "clue": "There are only ninety minutes between the flights in Denver.",
                "clue_answer": "the Denver connection time was ninety minutes",
                # Before any delay is announced, both branches are viable.  The
                # later two-hour event is what makes only this branch missed.
                "state_patch": {"layover_minutes": 90, "connection_status": "viable"},
                "expected_post_action": "protect_onward_segment",
                "post_answer": "120 minutes",
            },
            {
                "id": "aligned",
                "clue": "There are four hours between the flights in Denver.",
                "clue_answer": "the Denver connection time was four hours",
                "state_patch": {"layover_minutes": 240, "connection_status": "viable"},
                "expected_post_action": "close_case",
                "post_answer": "120 minutes",
            },
        ],
    },
    "bank": {
        "clue_prompt": "Was the disputed charge tied to the same card identifier that is currently on file?",
        "rule_turns": [
            (
                "agent",
                "The automated review accepts a dispute only when the charge's card identifier matches the current card record; otherwise it returns unmatched.",
            ),
            ("user", "Understood; I checked which card identifier the charge used."),
        ],
        "outcome_variable": "dispute_status",
        "hidden_outcomes": ["returned_unmatched", "approved"],
        "ambiguous_observation": (
            "Twenty-five minutes have passed and the dispute review finished, but its result code is hidden. "
            "Based on the card detail I gave earlier, what should happen next?"
        ),
        "causal_definitions": {
            "misaligned": "the charge identifier differs from the current card record",
            "aligned": "the charge identifier matches the current card record",
        },
        "branches": [
            {
                "id": "misaligned",
                "clue": "My current card was reissued, but the disputed transaction carried the original card reference.",
                "clue_answer": "the charge used the original identifier while the current card was reissued",
                "state_patch": {"card_on_file": "reissued", "charge_card": "original"},
                "expected_post_action": "reconcile_card_records",
                "post_answer": "it came back unmatched",
            },
            {
                "id": "aligned",
                "clue": "My current card was reissued, and the disputed transaction carried that same reissued-card reference.",
                "clue_answer": "the charge identifier matched the reissued card",
                "state_patch": {"card_on_file": "reissued", "charge_card": "reissued"},
                "expected_post_action": "close_case",
                "post_answer": "it was approved",
            },
        ],
    },
    "clinic": {
        "clue_prompt": "Did the referral come from the source required for authorization?",
        "rule_turns": [
            (
                "agent",
                "Authorization is granted only when the referral comes from the required primary-care source; another source is declined.",
            ),
            ("user", "Understood; I checked who issued the referral."),
        ],
        "outcome_variable": "authorization_status",
        "hidden_outcomes": ["declined", "granted"],
        "ambiguous_observation": (
            "Thirty minutes have passed and the authorization review finished, but the decision is not displayed. "
            "Based on the referral detail I gave earlier, what should we do next?"
        ),
        "causal_definitions": {
            "misaligned": "the referral came from a source that does not qualify",
            "aligned": "the referral came from the required qualifying source",
        },
        "branches": [
            {
                "id": "misaligned",
                "clue": "The referral came from the walk-in centre, not my regular primary-care physician.",
                "clue_answer": "the referral came from a walk-in centre",
                "state_patch": {"referral_source": "walk_in", "required_source": "primary_care"},
                "expected_post_action": "obtain_qualifying_referral",
                "post_answer": "it was declined",
            },
            {
                "id": "aligned",
                "clue": "The referral came from my regular primary-care physician, which is the required source.",
                "clue_answer": "the referral came from the required primary-care physician",
                "state_patch": {"referral_source": "primary_care", "required_source": "primary_care"},
                "expected_post_action": "close_case",
                "post_answer": "it was granted",
            },
        ],
    },
    "delivery": {
        "clue_prompt": "Does the address printed on the parcel match the current account address?",
        "rule_turns": [
            (
                "agent",
                "The delivery run succeeds only when the parcel label matches the current account address; a mismatch sends it back.",
            ),
            ("user", "Understood; I compared the label with the account."),
        ],
        "outcome_variable": "shipment_status",
        "hidden_outcomes": ["returned_to_sender", "delivered"],
        "ambiguous_observation": (
            "Forty minutes have passed and the delivery run ended, but tracking no longer shows the outcome. "
            "Based on the address detail I gave earlier, what should happen next?"
        ),
        "causal_definitions": {
            "misaligned": "the parcel label contains an outdated destination",
            "aligned": "the parcel label matches the current destination",
        },
        "branches": [
            {
                "id": "misaligned",
                "clue": "The parcel label still shows my previous address, while the account has my current address.",
                "clue_answer": "the label showed the previous address",
                "state_patch": {"label_address": "previous", "account_address": "current"},
                "expected_post_action": "correct_destination_record",
                "post_answer": "it went back to the sender",
            },
            {
                "id": "aligned",
                "clue": "The parcel label and the account both show my current address.",
                "clue_answer": "the label matched the current address",
                "state_patch": {"label_address": "current", "account_address": "current"},
                "expected_post_action": "close_case",
                "post_answer": "it was delivered",
            },
        ],
    },
    "utility": {
        "clue_prompt": "Does the account include every meter currently at the property?",
        "rule_turns": [
            (
                "agent",
                "Reading validation succeeds only when every meter at the property is registered on the account; an omitted meter is flagged.",
            ),
            ("user", "Understood; I compared the meters with the account."),
        ],
        "outcome_variable": "reading_status",
        "hidden_outcomes": ["flagged_incomplete", "accepted"],
        "ambiguous_observation": (
            "Twenty-five minutes have passed and validation finished, but the result is no longer visible. "
            "Based on the meter detail I gave earlier, what should we do next?"
        ),
        "causal_definitions": {
            "misaligned": "at least one property meter is missing from the account",
            "aligned": "every property meter is registered on the account",
        },
        "branches": [
            {
                "id": "misaligned",
                "clue": "The property has two meters, but the supplier profile lists only one of them.",
                "clue_answer": "one of the two meters was missing from the account",
                "state_patch": {"registered_points": 1, "actual_points": 2},
                "expected_post_action": "register_all_supply_points",
                "post_answer": "the reading was incomplete",
            },
            {
                "id": "aligned",
                "clue": "The property has two meters, and the supplier profile lists both of them.",
                "clue_answer": "both property meters were registered",
                "state_patch": {"registered_points": 2, "actual_points": 2},
                "expected_post_action": "close_case",
                "post_answer": "the reading was accepted",
            },
        ],
    },
    "saas": {
        "clue_prompt": "Was the reset aimed at the credential system the company currently uses?",
        "rule_turns": [
            (
                "agent",
                "Access is restored only when the reset targets the active authentication system; resetting an unused credential store leaves the account locked.",
            ),
            ("user", "Understood; I checked which credential system was targeted."),
        ],
        "outcome_variable": "access_status",
        "hidden_outcomes": ["still_locked", "restored"],
        "ambiguous_observation": (
            "Twenty minutes have passed and reset propagation finished, but the access result is not displayed. "
            "Based on the credential detail I gave earlier, what should happen next?"
        ),
        "causal_definitions": {
            "misaligned": "the reset targets a credential store the company no longer uses",
            "aligned": "the reset targets the company's active authentication system",
        },
        "branches": [
            {
                "id": "misaligned",
                "clue": "The company uses federated single sign-on, but the reset was aimed at the old local password store.",
                "clue_answer": "the reset targeted the old local store instead of federated sign-on",
                "state_patch": {"authentication_mode": "federated", "reset_target": "local"},
                "expected_post_action": "engage_identity_provider",
                "post_answer": "the account was still locked",
            },
            {
                "id": "aligned",
                "clue": "The company uses federated single sign-on, and the reset was aimed at that federated identity system.",
                "clue_answer": "the reset targeted the active federated identity system",
                "state_patch": {"authentication_mode": "federated", "reset_target": "federated"},
                "expected_post_action": "close_case",
                "post_answer": "access was restored",
            },
        ],
    },
    "warranty": {
        "clue_prompt": "Was the purchase made through the channel covered by this claim route?",
        "rule_turns": [
            (
                "agent",
                "The standard cover route authorises purchases from the covered retail channel; another purchase channel falls outside its terms.",
            ),
            ("user", "Understood; I checked how the item was purchased."),
        ],
        "outcome_variable": "claim_state",
        "hidden_outcomes": ["outside_terms", "authorised"],
        "ambiguous_observation": (
            "Thirty minutes have passed and the assessment finished, but the outcome is not shown. "
            "Based on the purchase detail I gave earlier, what should we do next?"
        ),
        "causal_definitions": {
            "misaligned": "the purchase channel falls outside the submitted cover route",
            "aligned": "the purchase channel is covered by the submitted route",
        },
        "branches": [
            {
                "id": "misaligned",
                "clue": "We bought it as a discounted display unit, while this cover route applies to standard retail purchases.",
                "clue_answer": "it was a display-unit purchase outside the standard route",
                "state_patch": {"purchase_channel": "display_unit", "covered_channel": "standard_retail"},
                "expected_post_action": "use_retailer_route",
                "post_answer": "it fell outside the terms",
            },
            {
                "id": "aligned",
                "clue": "We bought it as a standard retail item, which is the purchase channel covered by this route.",
                "clue_answer": "it was bought through the covered standard retail channel",
                "state_patch": {"purchase_channel": "standard_retail", "covered_channel": "standard_retail"},
                "expected_post_action": "close_case",
                "post_answer": "it was authorised",
            },
        ],
    },
    "tenancy": {
        "clue_prompt": "Does the contractor hold the access authority required by the current managing agent?",
        "rule_turns": [
            (
                "agent",
                "The visit can be completed only when the contractor's authority matches the current managing agent's requirements; expired authority blocks access.",
            ),
            ("user", "Understood; I checked the contractor's access authority."),
        ],
        "outcome_variable": "work_order_status",
        "hidden_outcomes": ["access_refused", "completed"],
        "ambiguous_observation": (
            "Thirty-five minutes have passed and the visit window ended, but the work-order outcome is hidden. "
            "Based on the authority detail I gave earlier, what should happen next?"
        ),
        "causal_definitions": {
            "misaligned": "the contractor holds expired authority from the former agent",
            "aligned": "the contractor holds current authority accepted by the managing agent",
        },
        "branches": [
            {
                "id": "misaligned",
                "clue": "The contractor still has expired authority from the former managing agent, not the current credentials.",
                "clue_answer": "the contractor had expired authority from the former agent",
                "state_patch": {"vendor_credentials": "expired", "required_credentials": "current"},
                "expected_post_action": "reissue_access_authority",
                "post_answer": "the contractor could not get access",
            },
            {
                "id": "aligned",
                "clue": "The contractor has the current authority required by the present managing agent.",
                "clue_answer": "the contractor had the required current authority",
                "state_patch": {"vendor_credentials": "current", "required_credentials": "current"},
                "expected_post_action": "close_case",
                "post_answer": "the work was completed",
            },
        ],
    },
    "telecom": {
        "clue_prompt": "Does the ownership record on the transfer match the required account holder?",
        "rule_turns": [
            (
                "agent",
                "The number transfer completes only when its ownership record matches the required direct account holder; an intermediary record is rejected.",
            ),
            ("user", "Understood; I checked the ownership record."),
        ],
        "outcome_variable": "port_status",
        "hidden_outcomes": ["rejected", "completed"],
        "ambiguous_observation": (
            "Thirty minutes have passed and the porting window ended, but the transfer result is not displayed. "
            "Based on the ownership detail I gave earlier, what should happen next?"
        ),
        "causal_definitions": {
            "misaligned": "the transfer carries an intermediary ownership record instead of the required direct record",
            "aligned": "the ownership record matches the required direct account holder",
        },
        "branches": [
            {
                "id": "misaligned",
                "clue": "The handset came through a reseller, and the transfer still carries the reseller's intermediary subscriber record.",
                "clue_answer": "the transfer carried the reseller's intermediary record",
                "state_patch": {"ownership_record": "intermediary", "required_record": "direct"},
                "expected_post_action": "align_ownership_record",
                "post_answer": "it was rejected",
            },
            {
                "id": "aligned",
                "clue": "The handset came through a reseller, but the transfer was already updated to my direct subscriber record.",
                "clue_answer": "the transfer used the required direct ownership record",
                "state_patch": {"ownership_record": "direct", "required_record": "direct"},
                "expected_post_action": "close_case",
                "post_answer": "it was completed",
            },
        ],
    },
    "college": {
        "clue_prompt": "Have the transferred credits already received the prior-study assessment required for enrolment?",
        "rule_turns": [
            (
                "agent",
                "Enrolment is confirmed only when transferred study has the required assessment; unassessed study is held for review.",
            ),
            ("user", "Understood; I checked the assessment status."),
        ],
        "outcome_variable": "enrolment_status",
        "hidden_outcomes": ["held_for_review", "confirmed"],
        "ambiguous_observation": (
            "Thirty minutes have passed and the registration run finished, but the enrolment result is not visible. "
            "Based on the assessment detail I gave earlier, what should happen next?"
        ),
        "causal_definitions": {
            "misaligned": "the transferred study has not received its required assessment",
            "aligned": "the transferred study has already received the required assessment",
        },
        "branches": [
            {
                "id": "misaligned",
                "clue": "My overseas transfer credits are still unassessed, although an assessment is required.",
                "clue_answer": "the transferred credits were still unassessed",
                "state_patch": {"prior_study_state": "unassessed", "required_state": "assessed"},
                "expected_post_action": "request_prior_study_assessment",
                "post_answer": "it was held for review",
            },
            {
                "id": "aligned",
                "clue": "My overseas transfer credits have already received the required assessment.",
                "clue_answer": "the transferred credits had already been assessed",
                "state_patch": {"prior_study_state": "assessed", "required_state": "assessed"},
                "expected_post_action": "close_case",
                "post_answer": "it was confirmed",
            },
        ],
    },
    "motor": {
        "clue_prompt": "Does the registered keeper match the person named on the policy?",
        "rule_turns": [
            (
                "agent",
                "The assessment settles only when the registered keeper matches the policy name; a mismatch is held for proof.",
            ),
            ("user", "Understood; I compared the keeper and policy names."),
        ],
        "outcome_variable": "claim_progress",
        "hidden_outcomes": ["held_for_proof", "settled"],
        "ambiguous_observation": (
            "Thirty-five minutes have passed and the assessment finished, but the outcome is not displayed. "
            "Based on the name detail I gave earlier, what should happen next?"
        ),
        "causal_definitions": {
            "misaligned": "the registered keeper and policyholder names differ",
            "aligned": "the registered keeper matches the policyholder name",
        },
        "branches": [
            {
                "id": "misaligned",
                "clue": "The vehicle is registered to my partner, while the insurance cover names me.",
                "clue_answer": "the keeper and policyholder names were different",
                "state_patch": {"keeper_name": "other_party", "policy_name": "caller"},
                "expected_post_action": "align_policy_records",
                "post_answer": "it was held pending proof",
            },
            {
                "id": "aligned",
                "clue": "The vehicle registration and the insurance cover are both in my name.",
                "clue_answer": "the keeper matched the policyholder",
                "state_patch": {"keeper_name": "caller", "policy_name": "caller"},
                "expected_post_action": "close_case",
                "post_answer": "it was settled",
            },
        ],
    },
    "permit": {
        "clue_prompt": "Does the supporting proof name the same person who is applying for the permit?",
        "rule_turns": [
            (
                "agent",
                "The eligibility check issues the permit only when the proof names the applicant; proof naming another occupant is refused.",
            ),
            ("user", "Understood; I compared the names on the documents."),
        ],
        "outcome_variable": "permit_status",
        "hidden_outcomes": ["refused", "issued"],
        "ambiguous_observation": (
            "Twenty-five minutes have passed and the eligibility check finished, but the decision is not shown. "
            "Based on the document detail I gave earlier, what should happen next?"
        ),
        "causal_definitions": {
            "misaligned": "the supporting proof names someone other than the applicant",
            "aligned": "the supporting proof names the permit applicant",
        },
        "branches": [
            {
                "id": "misaligned",
                "clue": "The tenancy proof is in my flatmate's name, while I am the person filing for the permit.",
                "clue_answer": "the proof named the flatmate instead of the applicant",
                "state_patch": {"proof_name": "other_occupant", "applicant_name": "caller"},
                "expected_post_action": "supply_alternative_proof",
                "post_answer": "it was refused",
            },
            {
                "id": "aligned",
                "clue": "The tenancy proof and the permit filing are both in my name.",
                "clue_answer": "the proof named the permit applicant",
                "state_patch": {"proof_name": "caller", "applicant_name": "caller"},
                "expected_post_action": "close_case",
                "post_answer": "it was issued",
            },
        ],
    },
}


# These user-initiated corrections occur during the fast-forward gap.  Each
# one repairs the relation encoded by the misaligned branch before the external
# processor runs.  Effects are declarative action semantics, not precomputed
# terminal states: the normal transition rules still determine the outcome.
# Router and flight retain their domain-specific interruption/protection actions
# from the base templates because those already change a scored state.
HIDDEN_USER_INTERVENTIONS = {
    "pharmacy": {
        "action": "correct_pharmacy_billing_profile",
        "at_minute": 8,
        "observation": (
            "While you were unavailable, I corrected the pharmacy billing "
            "profile so it uses the active plan."
        ),
        "effects": [
            {"target": "billing_plan", "copy_from": "active_plan"},
            {"target": "causal_alignment", "value": "aligned"},
        ],
    },
    "bank": {
        "action": "update_dispute_card_identifier",
        "at_minute": 10,
        "observation": (
            "While you were unavailable, I updated the dispute so its card "
            "identifier matches the current card record."
        ),
        "effects": [
            {"target": "charge_card", "copy_from": "card_on_file"},
            {"target": "causal_alignment", "value": "aligned"},
        ],
    },
    "clinic": {
        "action": "replace_referral_with_qualifying_source",
        "at_minute": 12,
        "observation": (
            "While you were unavailable, I replaced the referral with one "
            "from the required primary-care source."
        ),
        "effects": [
            {"target": "referral_source", "copy_from": "required_source"},
            {"target": "causal_alignment", "value": "aligned"},
        ],
    },
    "delivery": {
        "action": "correct_parcel_destination",
        "at_minute": 12,
        "observation": (
            "While you were unavailable, I had the parcel destination "
            "corrected to match the current account address."
        ),
        "effects": [
            {"target": "label_address", "copy_from": "account_address"},
            {"target": "causal_alignment", "value": "aligned"},
        ],
    },
    "utility": {
        "action": "register_missing_supply_points",
        "at_minute": 9,
        "observation": (
            "While you were unavailable, I added every property meter to the "
            "supplier account."
        ),
        "effects": [
            {"target": "registered_points", "copy_from": "actual_points"},
            {"target": "causal_alignment", "value": "aligned"},
        ],
    },
    "saas": {
        "action": "redirect_reset_to_active_identity_system",
        "at_minute": 7,
        "observation": (
            "While you were unavailable, I redirected the reset to the "
            "company's active identity system."
        ),
        "effects": [
            {"target": "reset_target", "copy_from": "authentication_mode"},
            {"target": "causal_alignment", "value": "aligned"},
        ],
    },
    "warranty": {
        "action": "switch_to_matching_purchase_route",
        "at_minute": 11,
        "observation": (
            "While you were unavailable, I moved the repair request to the "
            "purchase route that covers the original seller channel."
        ),
        "effects": [
            {"target": "covered_channel", "copy_from": "purchase_channel"},
            {"target": "causal_alignment", "value": "aligned"},
        ],
    },
    "tenancy": {
        "action": "refresh_contractor_access_authority",
        "at_minute": 10,
        "observation": (
            "While you were unavailable, I had the contractor's access "
            "authority updated to the current required credentials."
        ),
        "effects": [
            {"target": "vendor_credentials", "copy_from": "required_credentials"},
            {"target": "causal_alignment", "value": "aligned"},
        ],
    },
    "telecom": {
        "action": "update_transfer_ownership_record",
        "at_minute": 9,
        "observation": (
            "While you were unavailable, I updated the transfer to the "
            "required direct ownership record."
        ),
        "effects": [
            {"target": "ownership_record", "copy_from": "required_record"},
            {"target": "causal_alignment", "value": "aligned"},
        ],
    },
    "college": {
        "action": "complete_prior_study_assessment",
        "at_minute": 10,
        "observation": (
            "While you were unavailable, the records office completed the "
            "required prior-study assessment."
        ),
        "effects": [
            {"target": "prior_study_state", "copy_from": "required_state"},
            {"target": "causal_alignment", "value": "aligned"},
        ],
    },
    "motor": {
        "action": "align_policyholder_record",
        "at_minute": 12,
        "observation": (
            "While you were unavailable, I corrected the policy record so it "
            "matches the registered keeper."
        ),
        "effects": [
            {"target": "policy_name", "copy_from": "keeper_name"},
            {"target": "causal_alignment", "value": "aligned"},
        ],
    },
    "permit": {
        "action": "upload_applicant_named_proof",
        "at_minute": 8,
        "observation": (
            "While you were unavailable, I uploaded replacement proof in the "
            "permit applicant's name."
        ),
        "effects": [
            {"target": "proof_name", "copy_from": "applicant_name"},
            {"target": "causal_alignment", "value": "aligned"},
        ],
    },
}


def validate_design_registry(template_names: set[str]) -> None:
    """Fail loudly when a benchmark template lacks a causal v0.5 design."""

    configured = set(CAUSAL_DESIGNS)
    if configured != template_names:
        raise ValueError(
            f"v0.5 causal designs mismatch templates: missing={template_names - configured}, "
            f"extra={configured - template_names}"
        )
    for name, design in CAUSAL_DESIGNS.items():
        branches = design["branches"]
        if {branch["id"] for branch in branches} != {"misaligned", "aligned"}:
            raise ValueError(f"{name}: expected balanced aligned/misaligned branches")
        if len({branch["expected_post_action"] for branch in branches}) != 2:
            raise ValueError(f"{name}: branches must require different post-gap actions")
