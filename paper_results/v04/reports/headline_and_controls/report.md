# DUAL-AudioBench evaluation report

- Raw attempt rows: 2352
- Unique completed trajectories: 2352
- Duplicate successful rows ignored in metrics: 0
- API/runtime error attempts: 0
- Models: google/gemini-2.5-flash, google/gemini-3-flash-preview

A trajectory passes only when both actions, any scored response style, all belief reports, and all hidden-state top predictions pass.

## google/gemini-2.5-flash

- Coverage: 1176/1176 trajectories (100.0%)
- Overall partial outcomes: 74.0% pre-gap, 65.7% post-gap, 46.6% both actions, 17.3% strict trajectory
- API calls: 16,519 (16,519 metered)
- Tokens: 21,996,427 (21,604,803 prompt + 391,624 completion)
- Reported API cost: $21.2018
- API request time: 3076.6 minutes

### Condition metrics

| Condition | n | Full pass | Pre | Post | Belief valid | Belief pre | Belief post | Cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| full_audio | 168 | 23.8% | 71.4% | 60.1% | 99.6% | 32.1% | 82.7% | $3.5057 |
| gap_no_state_change | 168 | 11.3% | 75.0% | 59.5% | 99.2% | 28.0% | 76.8% | $3.4499 |
| clue_removed | 168 | 16.7% | 73.2% | 61.9% | 99.2% | 25.0% | 85.7% | $3.4504 |
| transcript_only | 168 | 41.1% | 78.6% | 79.2% | 99.8% | 60.1% | 92.9% | $0.3590 |
| neutral_audio | 168 | 16.1% | 67.9% | 60.7% | 99.6% | 27.4% | 81.5% | $3.4510 |
| prosody_high | 168 | 8.3% | 74.4% | 65.5% | 99.4% | 31.5% | 83.9% | $3.4945 |
| prosody_low | 168 | 3.6% | 77.4% | 73.2% | 99.6% | 24.4% | 88.7% | $3.4913 |

### Matched controls

| Control | Paired n | Domains | Effect | 95% CI | p |
|---|---:|---:|---:|---:|---:|
| Full audio - clue removed, post-gap | 168 | 14 | -1.8% | -8.9% to 6.0% | 0.7622 |
| Full audio - clue removed, full trajectory | 168 | 14 | 7.1% | -4.2% to 22.6% | 0.5000 |
| Hidden user action - full audio, post-gap | 0 | 0 | N/A | N/A to N/A | N/A |
| Transcript - full audio, pre-gap action | 168 | 14 | 7.1% | -7.7% to 22.6% | 0.4238 |
| Transcript - full audio, post-gap action | 168 | 14 | 19.0% | 4.8% to 33.3% | 0.0342 |
| Transcript - full audio, immediate belief | 168 | 14 | 10.1% | -1.8% to 22.0% | 0.1875 |
| Transcript - full audio, strict trajectory | 168 | 14 | 17.3% | 6.5% to 31.0% | 0.0076 |
| Full audio - no-state-change gap, post-gap | 168 | 14 | 0.6% | -14.3% to 17.9% | 1.0000 |
| Neutral audio - full audio, immediate belief | 168 | 14 | -1.2% | -6.0% to 3.6% | 0.8203 |

### Prosody selectivity

- Identical-transcript pairs: 123; unique stimuli: 78.
- High-affect style accuracy: 32.7% [26.6%, 38.6%].
- Low-affect style accuracy: 15.6% [9.1%, 22.1%].
- Both deliveries correct: 3.1% [0.6%, 6.2%] (random pair chance 6.2%).
- Directional style contrast: -2.7% [-8.1%, 3.4%].
- Technical-action invariance: 77.2% [64.4%, 88.8%].
- Post-observation top-belief invariance: 86.2% [71.2%, 98.2%].
- Post-observation belief JSD: 0.124 [0.036, 0.235].
- Pre-final belief JSD: 0.144 [0.050, 0.260].

### Full-audio slices

| Slice | n | Full pass | Two-action pass | Pre | Post |
|---|---:|---:|---:|---:|---:|
| domain: account_access | 12 | 0.0% | 41.7% | 66.7% | 50.0% |
| domain: banking | 12 | 8.3% | 66.7% | 66.7% | 66.7% |
| domain: education | 12 | 0.0% | 50.0% | 91.7% | 50.0% |
| domain: energy | 12 | 33.3% | 91.7% | 91.7% | 91.7% |
| domain: housing | 12 | 58.3% | 83.3% | 83.3% | 83.3% |
| domain: logistics | 12 | 8.3% | 8.3% | 25.0% | 8.3% |
| domain: mobile_service | 12 | 25.0% | 75.0% | 83.3% | 83.3% |
| domain: motor_insurance | 12 | 75.0% | 100.0% | 100.0% | 100.0% |
| domain: permits | 12 | 8.3% | 41.7% | 91.7% | 41.7% |
| domain: pharmacy | 12 | 8.3% | 83.3% | 83.3% | 83.3% |
| domain: repair | 12 | 0.0% | 16.7% | 33.3% | 41.7% |
| domain: scheduling | 12 | 8.3% | 25.0% | 50.0% | 33.3% |
| domain: tech_support | 12 | 8.3% | 8.3% | 33.3% | 16.7% |
| domain: travel | 12 | 91.7% | 91.7% | 100.0% | 91.7% |
| bucket: 1-2 | 56 | 28.6% | 51.8% | 60.7% | 53.6% |
| bucket: 12-20 | 56 | 21.4% | 60.7% | 75.0% | 64.3% |
| bucket: 5-8 | 56 | 21.4% | 55.4% | 78.6% | 62.5% |

### Failure tags

- `STATE_BELIEF_ERROR`: 850 (87.4% of failed trajectories)
- `PROSODY_GROUNDING_FAILURE`: 251 (25.8% of failed trajectories)
- `EARLY_CLUE_LOSS`: 155 (15.9% of failed trajectories)
- `TIME_INFERENCE_FAILURE`: 108 (11.1% of failed trajectories)
- `PREMATURE_CLOSE`: 104 (10.7% of failed trajectories)
- `REPEATED_ACTION`: 55 (5.7% of failed trajectories)
- `STATE_SYNC_FAILURE`: 46 (4.7% of failed trajectories)
- `ACTION_SELECTION_FAILURE`: 43 (4.4% of failed trajectories)
- `PREMATURE_ESCALATION`: 33 (3.4% of failed trajectories)
- `BELIEF_REPORT_INVALID`: 18 (1.8% of failed trajectories)

### Difficulty assessment

- The domain-clustered clue-ablation interval crosses zero; construct validity is not established for this model.

## google/gemini-3-flash-preview

- Coverage: 1176/1176 trajectories (100.0%)
- Overall partial outcomes: 83.7% pre-gap, 74.0% post-gap, 54.3% both actions, 42.2% strict trajectory
- API calls: 16,670 (16,670 metered)
- Tokens: 22,318,086 (21,827,843 prompt + 490,243 completion)
- Reported API cost: $22.2641
- API request time: 3249.7 minutes

### Condition metrics

| Condition | n | Full pass | Pre | Post | Belief valid | Belief pre | Belief post | Cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| full_audio | 168 | 56.5% | 81.5% | 79.8% | 100.0% | 72.0% | 97.6% | $3.5749 |
| gap_no_state_change | 168 | 34.5% | 83.3% | 53.6% | 100.0% | 73.2% | 82.1% | $3.6169 |
| clue_removed | 168 | 53.6% | 79.8% | 78.0% | 100.0% | 78.6% | 85.1% | $3.6101 |
| transcript_only | 168 | 67.9% | 91.7% | 79.8% | 100.0% | 80.4% | 99.4% | $0.6239 |
| neutral_audio | 168 | 57.1% | 85.1% | 76.8% | 100.0% | 72.6% | 96.4% | $3.6021 |
| prosody_high | 168 | 19.6% | 84.5% | 75.0% | 100.0% | 70.8% | 95.8% | $3.6001 |
| prosody_low | 168 | 6.0% | 79.8% | 75.0% | 100.0% | 73.8% | 95.8% | $3.6360 |

### Matched controls

| Control | Paired n | Domains | Effect | 95% CI | p |
|---|---:|---:|---:|---:|---:|
| Full audio - clue removed, post-gap | 168 | 14 | 1.8% | -8.9% to 12.5% | 0.8320 |
| Full audio - clue removed, full trajectory | 168 | 14 | 3.0% | -4.8% to 11.3% | 0.5977 |
| Hidden user action - full audio, post-gap | 0 | 0 | N/A | N/A to N/A | N/A |
| Transcript - full audio, pre-gap action | 168 | 14 | 10.1% | -0.6% to 22.6% | 0.1562 |
| Transcript - full audio, post-gap action | 168 | 14 | -0.0% | -8.9% to 9.5% | 1.0000 |
| Transcript - full audio, immediate belief | 168 | 14 | 1.8% | 0.0% to 4.8% | 0.5000 |
| Transcript - full audio, strict trajectory | 168 | 14 | 11.3% | 0.6% to 23.2% | 0.0957 |
| Full audio - no-state-change gap, post-gap | 168 | 14 | 26.2% | 10.1% to 42.3% | 0.0117 |
| Neutral audio - full audio, immediate belief | 168 | 14 | -1.2% | -3.6% to 1.2% | 0.6250 |

### Prosody selectivity

- Identical-transcript pairs: 142; unique stimuli: 79.
- High-affect style accuracy: 33.5% [23.3%, 43.6%].
- Low-affect style accuracy: 8.1% [3.7%, 13.0%].
- Both deliveries correct: 1.5% [0.0%, 3.9%] (random pair chance 6.2%).
- Directional style contrast: -4.1% [-11.9%, 3.4%].
- Technical-action invariance: 88.3% [76.4%, 97.2%].
- Post-observation top-belief invariance: 96.5% [93.5%, 99.1%].
- Post-observation belief JSD: 0.034 [0.015, 0.056].
- Pre-final belief JSD: 0.037 [0.022, 0.053].

### Full-audio slices

| Slice | n | Full pass | Two-action pass | Pre | Post |
|---|---:|---:|---:|---:|---:|
| domain: account_access | 12 | 58.3% | 91.7% | 91.7% | 91.7% |
| domain: banking | 12 | 91.7% | 100.0% | 100.0% | 100.0% |
| domain: education | 12 | 0.0% | 8.3% | 33.3% | 25.0% |
| domain: energy | 12 | 83.3% | 100.0% | 100.0% | 100.0% |
| domain: housing | 12 | 75.0% | 100.0% | 100.0% | 100.0% |
| domain: logistics | 12 | 25.0% | 25.0% | 58.3% | 33.3% |
| domain: mobile_service | 12 | 83.3% | 100.0% | 100.0% | 100.0% |
| domain: motor_insurance | 12 | 91.7% | 100.0% | 100.0% | 100.0% |
| domain: permits | 12 | 50.0% | 50.0% | 50.0% | 50.0% |
| domain: pharmacy | 12 | 75.0% | 83.3% | 83.3% | 91.7% |
| domain: repair | 12 | 41.7% | 66.7% | 66.7% | 66.7% |
| domain: scheduling | 12 | 100.0% | 100.0% | 100.0% | 100.0% |
| domain: tech_support | 12 | 8.3% | 25.0% | 58.3% | 58.3% |
| domain: travel | 12 | 8.3% | 100.0% | 100.0% | 100.0% |
| bucket: 1-2 | 56 | 50.0% | 71.4% | 75.0% | 80.4% |
| bucket: 12-20 | 56 | 60.7% | 75.0% | 80.4% | 80.4% |
| bucket: 5-8 | 56 | 58.9% | 78.6% | 89.3% | 78.6% |

### Failure tags

- `STATE_BELIEF_ERROR`: 358 (52.6% of failed trajectories)
- `PROSODY_GROUNDING_FAILURE`: 263 (38.7% of failed trajectories)
- `EARLY_CLUE_LOSS`: 200 (29.4% of failed trajectories)
- `TIME_INFERENCE_FAILURE`: 56 (8.2% of failed trajectories)
- `REPEATED_ACTION`: 35 (5.1% of failed trajectories)
- `PREMATURE_CLOSE`: 23 (3.4% of failed trajectories)
- `PREMATURE_ESCALATION`: 16 (2.4% of failed trajectories)
- `ACTION_SELECTION_FAILURE`: 8 (1.2% of failed trajectories)
- `STATE_SYNC_FAILURE`: 7 (1.0% of failed trajectories)

### Difficulty assessment

- The domain-clustered clue-ablation interval crosses zero; construct validity is not established for this model.

## Interpretation cautions

- Results contain 2 observed run seed(s); pass@k is labeled with the number actually available.
- `transcript_only` is a control; audio conditions replay synthesized alternating turns.
- Human annotation and audible-prosody validation remain separate validation steps and are not replaced by model scores.
