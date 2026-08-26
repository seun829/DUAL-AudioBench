# R10. `causal_alignment` rewrites in the gap user actions

## Answer

**72 of 84** user-action specs include an effect targeting `causal_alignment` (72 of the 72 declarative specs; the 12 domain-coded specs have no effects list and rewrite nothing declaratively). That is **86% of the benchmark**.

## By domain

| Domain | n | declarative specs | rewrites alignment | share | user action(s) | effect targets |
|---|---|---|---|---|---|---|
| account_access | 6 | 6 | 6 | 100% | redirect_reset_to_active_identity_system | causal_alignment=6; reset_target=6 |
| banking | 6 | 6 | 6 | 100% | update_dispute_card_identifier | causal_alignment=6; charge_card=6 |
| education | 6 | 6 | 6 | 100% | complete_prior_study_assessment | causal_alignment=6; prior_study_state=6 |
| energy | 6 | 6 | 6 | 100% | register_missing_supply_points | causal_alignment=6; registered_points=6 |
| housing | 6 | 6 | 6 | 100% | refresh_contractor_access_authority | causal_alignment=6; vendor_credentials=6 |
| logistics | 6 | 6 | 6 | 100% | correct_parcel_destination | causal_alignment=6; label_address=6 |
| mobile_service | 6 | 6 | 6 | 100% | update_transfer_ownership_record | causal_alignment=6; ownership_record=6 |
| motor_insurance | 6 | 6 | 6 | 100% | align_policyholder_record | causal_alignment=6; policy_name=6 |
| permits | 6 | 6 | 6 | 100% | upload_applicant_named_proof | causal_alignment=6; proof_name=6 |
| pharmacy | 6 | 6 | 6 | 100% | correct_pharmacy_billing_profile | billing_plan=6; causal_alignment=6 |
| repair | 6 | 6 | 6 | 100% | switch_to_matching_purchase_route | causal_alignment=6; covered_channel=6 |
| scheduling | 6 | 6 | 6 | 100% | replace_referral_with_qualifying_source | causal_alignment=6; referral_source=6 |
| tech_support | 6 | 0 | 0 | 0% | power_cycle_during_maintenance |  |
| travel | 6 | 0 | 0 | 0% | self_protect_onward_segment |  |

## Cross-check against the realized state

Independently of the spec text, comparing `initial_state.causal_alignment` with `state_after_gap.causal_alignment` in the 504 stored `hidden_user_action` trajectories: alignment actually changed in the domains account_access, banking, education, energy, housing, logistics, mobile_service, motor_insurance, permits, pharmacy, repair, scheduling.

## Reading

**The paper has to qualify the explicit-user-update condition substantially.** In 72 of 84 scenarios the hidden user action overwrites `causal_alignment` -- the variable that the early clue exists to determine and that the model is scored on reporting. In those scenarios the condition is not testing whether the model retained and applied the clue; it is testing whether the model can read a plainly-stated outcome that has made the clue irrelevant.

This interacts with R5. The user-update revision gain of 0.78 / 0.81 / 0.46 is the largest effect in the benchmark, and `causal_alignment` is a contributing changed variable *only* in this condition (R5's k column jumps from ~110 to ~190). Part of that gain is therefore the model tracking a variable the intervention itself set, announced in the same utterance. The effect is still real -- the domain outcome variable also moves -- but the headline number should either be quoted for the outcome variable alone or carry an explicit note.

Suggested wording for the limitations paragraph: *in 72 of 84 scenarios the hidden user action also sets the causal-alignment variable, so the explicit-user-update condition measures response to plainly stated evidence rather than retention of the earlier clue.*
