# V2. Matched-pair invariant

Deep-diffed all 42 causal pairs. Every leaf path that differs between the `_b0_s05` (misaligned) and `_b1_s05` (aligned) file is classified as EXPECTED (the clue and what it determines), CRITICAL (public conversation structure, menus, prosody, audio, transition), or UNEXPECTED.

## Verdict

**No critical differences in any of the 42 pairs.** For every pair, turn count, every turn's `speaker` and `kind`, both action menus and their order, `response_styles`, `causal_post_gap_observation`, `prosody_pair`, `audio_profile`, `menu_pairing_id`, `transition`, `belief_schema`, `bucket`, and `clue_turn_distance` are all byte-identical between branches.

No unexpected differences either: every differing field is the clue, a clue-derived initial-state value, the branch label, or prose that describes the branch.

## Which turn texts differ

In all 42 pairs, the only turns whose `text` differs are the ones with `kind` in {`clue`, `clue_prompt`}. Every `setup`, `causal_rule`, `filler`, `pre_gap_action`, and `pre_gap_acknowledgement` turn is identical across branches. The public history the model hears is therefore matched everywhere except the clue exchange, which is what the causal design requires.

## Hidden failure tags (expected to differ, checked separately)

`failure_tags` is the only part of either action menu that differs between branches, and it must: it is a hidden diagnostic label, never shown to the model. In all 42 pairs `close_case` carries `PREMATURE_CLOSE` on the misaligned branch (where it is wrong) and no tag on the aligned branch (where it is gold), and the domain repair action carries `EARLY_CLUE_LOSS` on the aligned branch (where choosing it means the clue was ignored) and no tag on the misaligned branch (where it is gold). The `(action, description)` list -- content and order -- is identical across branches for all 42 pairs at both stages.

## Expected initial-state fields that differ, by domain

| domain | initial_state fields differing |
|---|---|
| account_access | causal_alignment, reset_target |
| banking | causal_alignment, charge_card |
| education | causal_alignment, prior_study_state |
| energy | causal_alignment, registered_points |
| housing | causal_alignment, vendor_credentials |
| logistics | causal_alignment, label_address |
| mobile_service | causal_alignment, ownership_record |
| motor_insurance | causal_alignment, keeper_name |
| permits | causal_alignment, proof_name |
| pharmacy | billing_plan, causal_alignment |
| repair | causal_alignment, purchase_channel |
| scheduling | causal_alignment, referral_source |
| tech_support | causal_alignment, config_integrity |
| travel | causal_alignment, layover_minutes |

## Per-pair counts

| pair_id | domain | bucket | differing | expected | critical | unexpected |
|---|---|---|---|---|---|---|
| bank:1-2:s05 | banking | 1-2 | 17 | 17 | 0 | 0 |
| bank:12-20:s05 | banking | 12-20 | 17 | 17 | 0 | 0 |
| bank:5-8:s05 | banking | 5-8 | 17 | 17 | 0 | 0 |
| clinic:1-2:s05 | scheduling | 1-2 | 17 | 17 | 0 | 0 |
| clinic:12-20:s05 | scheduling | 12-20 | 17 | 17 | 0 | 0 |
| clinic:5-8:s05 | scheduling | 5-8 | 17 | 17 | 0 | 0 |
| college:1-2:s05 | education | 1-2 | 17 | 17 | 0 | 0 |
| college:12-20:s05 | education | 12-20 | 17 | 17 | 0 | 0 |
| college:5-8:s05 | education | 5-8 | 17 | 17 | 0 | 0 |
| delivery:1-2:s05 | logistics | 1-2 | 17 | 17 | 0 | 0 |
| delivery:12-20:s05 | logistics | 12-20 | 17 | 17 | 0 | 0 |
| delivery:5-8:s05 | logistics | 5-8 | 17 | 17 | 0 | 0 |
| flight:1-2:s05 | travel | 1-2 | 16 | 16 | 0 | 0 |
| flight:12-20:s05 | travel | 12-20 | 16 | 16 | 0 | 0 |
| flight:5-8:s05 | travel | 5-8 | 16 | 16 | 0 | 0 |
| motor:1-2:s05 | motor_insurance | 1-2 | 17 | 17 | 0 | 0 |
| motor:12-20:s05 | motor_insurance | 12-20 | 17 | 17 | 0 | 0 |
| motor:5-8:s05 | motor_insurance | 5-8 | 17 | 17 | 0 | 0 |
| permit:1-2:s05 | permits | 1-2 | 17 | 17 | 0 | 0 |
| permit:12-20:s05 | permits | 12-20 | 17 | 17 | 0 | 0 |
| permit:5-8:s05 | permits | 5-8 | 17 | 17 | 0 | 0 |
| pharmacy:1-2:s05 | pharmacy | 1-2 | 17 | 17 | 0 | 0 |
| pharmacy:12-20:s05 | pharmacy | 12-20 | 17 | 17 | 0 | 0 |
| pharmacy:5-8:s05 | pharmacy | 5-8 | 17 | 17 | 0 | 0 |
| router:1-2:s05 | tech_support | 1-2 | 17 | 17 | 0 | 0 |
| router:12-20:s05 | tech_support | 12-20 | 17 | 17 | 0 | 0 |
| router:5-8:s05 | tech_support | 5-8 | 17 | 17 | 0 | 0 |
| saas:1-2:s05 | account_access | 1-2 | 17 | 17 | 0 | 0 |
| saas:12-20:s05 | account_access | 12-20 | 17 | 17 | 0 | 0 |
| saas:5-8:s05 | account_access | 5-8 | 17 | 17 | 0 | 0 |
| telecom:1-2:s05 | mobile_service | 1-2 | 17 | 17 | 0 | 0 |
| telecom:12-20:s05 | mobile_service | 12-20 | 17 | 17 | 0 | 0 |
| telecom:5-8:s05 | mobile_service | 5-8 | 17 | 17 | 0 | 0 |
| tenancy:1-2:s05 | housing | 1-2 | 17 | 17 | 0 | 0 |
| tenancy:12-20:s05 | housing | 12-20 | 17 | 17 | 0 | 0 |
| tenancy:5-8:s05 | housing | 5-8 | 17 | 17 | 0 | 0 |
| utility:1-2:s05 | energy | 1-2 | 17 | 17 | 0 | 0 |
| utility:12-20:s05 | energy | 12-20 | 17 | 17 | 0 | 0 |
| utility:5-8:s05 | energy | 5-8 | 17 | 17 | 0 | 0 |
| warranty:1-2:s05 | repair | 1-2 | 17 | 17 | 0 | 0 |
| warranty:12-20:s05 | repair | 12-20 | 17 | 17 | 0 | 0 |
| warranty:5-8:s05 | repair | 5-8 | 17 | 17 | 0 | 0 |
