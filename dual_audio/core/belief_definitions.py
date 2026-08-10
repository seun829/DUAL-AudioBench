"""Operational definitions for every benchmark belief-state value.

Definitions are public task semantics, not hidden answers.  They explain what
each ontology label means while leaving the model to infer which value holds
from the conversation and elapsed-world evidence.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence


BELIEF_VALUE_DEFINITIONS: dict[str, dict[str, str]] = {
    "firmware_status": {
        "not_started": "the maintenance update has not begun",
        "updating": "the update is actively progressing within its expected window",
        "stuck": "the update remains incomplete after the expected progress window",
        "completed": "the update finished successfully",
        "interrupted": "the update began but was stopped before completion",
    },
    "claim_status": {
        "not_submitted": "the claim has not entered the processor",
        "processing": "the claim is currently being processed",
        "rejected": "the processor denied the submitted claim",
        "approved": "the processor accepted the claim",
    },
    "connection_status": {
        "at_risk_if_delayed": "the connection is currently possible but a sufficiently long departure delay would break it",
        "missed": "the departure delay is at least the layover time, so the planned connection cannot be made",
        "protected": "confirmed protection/rebooking preserves the onward journey despite disruption",
        "viable": "the planned connection remains feasible with the current timing",
    },
    "dispute_status": {
        "not_filed": "the disputed charge has not been submitted for review",
        "under_review": "the dispute is in the automated review process",
        "returned_unmatched": "review returned because the submitted details did not match the stored record",
        "approved": "the dispute was accepted",
    },
    "authorization_status": {
        "not_requested": "coverage authorization has not been requested",
        "pending": "the authorization request is awaiting a decision",
        "declined": "the authorization request was refused",
        "granted": "the authorization request was approved",
    },
    "shipment_status": {
        "at_facility": "the shipment is held at a carrier facility",
        "out_for_delivery": "the shipment is on an active delivery run",
        "returned_to_sender": "delivery failed and the shipment is being sent back",
        "delivered": "the shipment reached its destination",
    },
    "reading_status": {
        "not_submitted": "the meter reading has not been submitted",
        "validating": "the submitted reading is undergoing validation",
        "flagged_incomplete": "validation found that the submitted reading omits required supply information",
        "accepted": "the reading passed validation",
    },
    "access_status": {
        "locked": "the user cannot currently access the account",
        "reset_pending": "a credential reset has started but has not resolved access",
        "still_locked": "the reset completed or timed out without restoring access",
        "restored": "account access is working again",
    },
    "claim_state": {
        "not_opened": "the repair-cover claim has not been opened",
        "in_assessment": "the claim is being assessed",
        "outside_terms": "assessment found that the claim does not fit the submitted cover route",
        "authorised": "the repair claim was approved",
    },
    "work_order_status": {
        "not_created": "no maintenance work order has been created",
        "dispatched": "a contractor has been sent to the property",
        "access_refused": "the contractor could not enter under the available authority",
        "completed": "the maintenance visit finished the work",
    },
    "port_status": {
        "not_started": "the number transfer has not been submitted",
        "in_progress": "the transfer is in the porting queue",
        "rejected": "the transfer was refused by the porting process",
        "completed": "the number transfer finished successfully",
    },
    "enrolment_status": {
        "not_submitted": "the enrolment has not been submitted",
        "processing": "the enrolment is being processed",
        "held_for_review": "processing paused for manual review of prior study",
        "confirmed": "the enrolment was accepted and confirmed",
    },
    "claim_progress": {
        "not_lodged": "the motor claim has not been lodged",
        "assessing": "the lodged claim is being assessed",
        "held_for_proof": "assessment paused until ownership or vehicle evidence is supplied",
        "settled": "the motor claim reached a final accepted settlement",
    },
    "permit_status": {
        "not_applied": "the permit application has not been submitted",
        "in_check": "the application is undergoing eligibility checks",
        "refused": "the eligibility check denied the application",
        "issued": "the permit was approved and issued",
    },
}


def definitions_for(
    schema: Mapping[str, Sequence[str]],
    supplied: Mapping[str, Mapping[str, str]] | None = None,
) -> dict[str, dict[str, str]]:
    """Return complete public descriptions for the values in ``schema``.

    Explicit task-provided definitions take precedence. Unknown extension
    values are retained with an empty description rather than assigned an
    invented meaning.
    """

    result: dict[str, dict[str, str]] = {}
    for variable, values in schema.items():
        known = BELIEF_VALUE_DEFINITIONS.get(variable, {})
        declared = (supplied or {}).get(variable, {})
        result[variable] = {
            value: str(declared.get(value) or known.get(value) or "")
            for value in values
        }
    return result
