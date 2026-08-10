# Failure-tag guide and current evidence

Failure tags are deterministic diagnostics attached to an incorrect selected
action or an invalid/incorrect belief report. They are not independent model
judgments. A failed trajectory can have multiple tags, so percentages do not
sum to 100%. The denominator is failed trajectories, not all trajectories.

| Tag | Operational meaning |
|---|---|
| `STATE_BELIEF_ERROR` | At least one checkpoint's highest-probability state is wrong. |
| `BELIEF_REPORT_INVALID` | A required distribution or revalidation flag is missing or malformed. |
| `EARLY_CLUE_LOSS` | The selected distractor is attractive when the earlier clue was not retained or used. |
| `STATE_SYNC_FAILURE` | The action treats the pre-gap world as if it still held after time advanced. |
| `TIME_INFERENCE_FAILURE` | The action fails to use the amount of elapsed time. |
| `REPEATED_ACTION` | The model repeats an already attempted step without new support. |
| `PREMATURE_CLOSE` | The model closes an unresolved interaction. |
| `PREMATURE_ESCALATION` | The model escalates before supported steps are exhausted. |
| `ACTION_SELECTION_FAILURE` | The action is wrong but no narrower action tag applies. |
| `OFF_MENU_RESPONSE` | The output does not select a permitted public option. |
| `PROSODY_GROUNDING_FAILURE` | Technical reasoning may be correct, but the selected response approach does not match the delivery. |

## Frozen schema-v0.3 pilot

| Tag | Gemini 2.5 Flash | Gemini 3 Flash |
|---|---:|---:|
| `STATE_BELIEF_ERROR` | 280 (77.8%) | 129 (53.8%) |
| `EARLY_CLUE_LOSS` | 112 (31.1%) | 93 (38.8%) |
| `TIME_INFERENCE_FAILURE` | 74 (20.6%) | 26 (10.8%) |
| `STATE_SYNC_FAILURE` | 60 (16.7%) | 27 (11.2%) |
| `BELIEF_REPORT_INVALID` | 40 (11.1%) | 18 (7.5%) |
| `REPEATED_ACTION` | 21 (5.8%) | 18 (7.5%) |
| `ACTION_SELECTION_FAILURE` | 17 (4.7%) | 5 (2.1%) |
| `PREMATURE_CLOSE` | 14 (3.9%) | 9 (3.8%) |
| `PREMATURE_ESCALATION` | 7 (1.9%) | 1 (0.4%) |
| `OFF_MENU_RESPONSE` | 1 (0.3%) | 0 (0.0%) |

The v0.3 model-specific reports are in
`paper_results/scores/gemini_paper84_score_report.txt` and
`paper_results/scores/gemini3flash_paper84_score_report.txt`.

## Schema-v0.4 expectations, not results

The defensible prior expectation is that belief errors remain the largest
failure family (roughly 50–80% of failed trajectories), clue-loss tags occur
on roughly one third, and state/time errors each occur on roughly 10–25%.
Strict JSON Schema should reduce `BELIEF_REPORT_INVALID` substantially; below
2% is the engineering target. There is no defensible numerical projection for
`PROSODY_GROUNDING_FAILURE` before the matched high/low experiment completes.

The full v0.4 fake-agent run and the paid compatibility gates are systems
checks and are deliberately excluded from empirical claims. Final v0.4 rates
will be generated only after both 840-trajectory paid runs complete.
