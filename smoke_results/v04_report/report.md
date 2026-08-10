# DUAL-AudioBench evaluation report

- Raw attempt rows: 756
- Unique completed trajectories: 756
- Duplicate successful rows ignored in metrics: 0
- API/runtime error attempts: 0
- Models: fake

A trajectory passes only when both actions, any scored response style, all belief reports, and all hidden-state top predictions pass.

## fake

- Coverage: 756/756 trajectories (100.0%)
- Overall partial outcomes: 72.1% pre-gap, 68.8% post-gap, 52.0% both actions, 32.8% strict trajectory
- API calls: 0 (0 metered)
- Tokens: 0 (0 prompt + 0 completion)
- Reported API cost: $0.0000
- API request time: 0.0 minutes

### Condition metrics

| Condition | n | Full pass | Pre | Post | Belief valid | Belief pre | Belief post | Cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| full_audio | 84 | 33.3% | 73.8% | 69.0% | 100.0% | 75.0% | 75.0% | $0.0000 |
| gap_no_state_change | 84 | 33.3% | 73.8% | 69.0% | 100.0% | 75.0% | 75.0% | $0.0000 |
| state_change_short | 84 | 72.6% | 94.0% | 92.9% | 100.0% | 94.0% | 94.0% | $0.0000 |
| clue_removed | 84 | 3.6% | 38.1% | 42.9% | 100.0% | 51.2% | 46.4% | $0.0000 |
| transcript_only | 84 | 33.3% | 73.8% | 69.0% | 100.0% | 75.0% | 75.0% | $0.0000 |
| neutral_audio | 84 | 33.3% | 73.8% | 69.0% | 100.0% | 75.0% | 75.0% | $0.0000 |
| hidden_user_action | 84 | 33.3% | 73.8% | 69.0% | 100.0% | 75.0% | 75.0% | $0.0000 |
| prosody_high | 84 | 26.2% | 73.8% | 69.0% | 100.0% | 75.0% | 75.0% | $0.0000 |
| prosody_low | 84 | 26.2% | 73.8% | 69.0% | 100.0% | 75.0% | 75.0% | $0.0000 |

### Matched controls

| Control | Paired n | Domains | Effect | 95% CI | p |
|---|---:|---:|---:|---:|---:|
| Full audio - clue removed, post-gap | 84 | 14 | 26.2% | 14.3% to 38.1% | 0.0029 |
| Full audio - clue removed, full trajectory | 84 | 14 | 29.8% | 21.4% to 38.1% | 0.0002 |
| Hidden user action - full audio, post-gap | 84 | 14 | 0.0% | 0.0% to 0.0% | 1.0000 |

### Prosody selectivity

- Identical-transcript pairs: 84; unique stimuli: 84.
- Both deliveries correct: 79.8%.
- Technical-action invariance: 100.0%.
- Post-observation top-belief invariance: 100.0%.
- Post-observation belief JSD: 0.000.

### Full-audio slices

| Slice | n | Full pass | Two-action pass | Pre | Post |
|---|---:|---:|---:|---:|---:|
| domain: account_access | 6 | 16.7% | 50.0% | 83.3% | 66.7% |
| domain: banking | 6 | 50.0% | 66.7% | 66.7% | 83.3% |
| domain: education | 6 | 33.3% | 50.0% | 83.3% | 50.0% |
| domain: energy | 6 | 33.3% | 33.3% | 66.7% | 50.0% |
| domain: housing | 6 | 16.7% | 66.7% | 66.7% | 66.7% |
| domain: logistics | 6 | 50.0% | 66.7% | 66.7% | 83.3% |
| domain: mobile_service | 6 | 16.7% | 50.0% | 83.3% | 50.0% |
| domain: motor_insurance | 6 | 50.0% | 50.0% | 66.7% | 66.7% |
| domain: permits | 6 | 33.3% | 50.0% | 66.7% | 83.3% |
| domain: pharmacy | 6 | 50.0% | 66.7% | 66.7% | 83.3% |
| domain: repair | 6 | 33.3% | 66.7% | 83.3% | 83.3% |
| domain: scheduling | 6 | 16.7% | 33.3% | 66.7% | 50.0% |
| domain: tech_support | 6 | 33.3% | 66.7% | 83.3% | 83.3% |
| domain: travel | 6 | 33.3% | 50.0% | 83.3% | 66.7% |
| bucket: 1-2 | 28 | 71.4% | 89.3% | 92.9% | 96.4% |
| bucket: 12-20 | 28 | 0.0% | 14.3% | 39.3% | 46.4% |
| bucket: 5-8 | 28 | 28.6% | 60.7% | 89.3% | 64.3% |

### Failure tags

- `STATE_BELIEF_ERROR`: 382 (47.3% of tags)
- `EARLY_CLUE_LOSS`: 124 (15.3% of tags)
- `PREMATURE_CLOSE`: 98 (12.1% of tags)
- `PREMATURE_ESCALATION`: 86 (10.6% of tags)
- `STATE_SYNC_FAILURE`: 43 (5.3% of tags)
- `TIME_INFERENCE_FAILURE`: 37 (4.6% of tags)
- `PROSODY_GROUNDING_FAILURE`: 34 (4.2% of tags)
- `REPEATED_ACTION`: 3 (0.4% of tags)
- `ACTION_SELECTION_FAILURE`: 1 (0.1% of tags)

### Difficulty assessment

- No obvious ceiling or ineffective-clue warning fired in this one-seed run.

## Interpretation cautions

- Results contain 1 observed run seed(s); pass@k is labeled with the number actually available.
- `transcript_only` is a control; audio conditions replay synthesized alternating turns.
- Human annotation and audible-prosody validation remain separate validation steps and are not replaced by model scores.
