# DUAL-AudioBench evaluation report

- Raw attempt rows: 4368
- Unique completed trajectories: 4368
- Duplicate successful rows ignored in metrics: 0
- API/runtime error attempts: 0
- Models: google/gemini-2.5-flash, google/gemini-3-flash-preview, openai/gpt-audio-mini

A trajectory passes only when both actions, any scored response style, all belief reports, and all hidden-state top predictions pass.

## google/gemini-2.5-flash

- Coverage: 1512/1512 trajectories (100.0%)
- Overall partial outcomes: 66.5% pre-gap, 38.1% post-gap, 26.7% both actions, 5.1% strict trajectory
- API calls: 22,717 (22,717 metered)
- Tokens: 31,898,271 (31,137,067 prompt + 761,204 completion)
- Reported API cost: $31.0290
- API request time: 2596.4 minutes

### Condition metrics

| Condition | n | Full pass | Pre | Post | Belief valid | Belief pre | Belief post | Cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| full_audio | 168 | 1.2% | 69.6% | 35.1% | 99.0% | 6.0% | 39.3% | $4.4706 |
| gap_no_state_change | 168 | 8.9% | 67.9% | 38.7% | 98.2% | 31.5% | 60.7% | $3.6533 |
| state_change_short | 168 | 1.8% | 63.7% | 35.7% | 98.2% | 29.8% | 35.7% | $3.5409 |
| clue_removed | 168 | 1.2% | 59.5% | 25.0% | 98.6% | 10.1% | 29.8% | $4.3725 |
| transcript_only | 168 | 10.1% | 77.4% | 35.7% | 100.0% | 51.8% | 51.8% | $0.4524 |
| neutral_audio | 168 | 0.6% | 64.9% | 31.5% | 98.0% | 29.8% | 32.7% | $3.6152 |
| hidden_user_action | 168 | 17.9% | 63.7% | 72.0% | 98.2% | 33.9% | 72.6% | $3.6248 |
| prosody_high | 168 | 0.6% | 68.5% | 36.9% | 98.2% | 30.4% | 37.5% | $3.6344 |
| prosody_low | 168 | 3.6% | 63.7% | 32.1% | 98.4% | 25.0% | 35.7% | $3.6648 |

### Belief probability metrics

| Condition | Brier | NLL | Normalized entropy | ECE | Revision gain | Stale mass |
|---|---:|---:|---:|---:|---:|---:|
| full_audio | 0.787 | 6.745 | 0.225 | 0.362 | -0.009 | 0.021 |
| gap_no_state_change | 0.550 | 4.392 | 0.212 | 0.242 | 0.596 | 0.028 |
| state_change_short | 0.675 | 6.193 | 0.173 | 0.314 | 0.142 | 0.017 |
| clue_removed | 1.006 | 8.036 | 0.309 | 0.457 | 0.147 | 0.022 |
| transcript_only | 0.472 | 4.174 | 0.218 | 0.171 | 0.282 | 0.018 |
| neutral_audio | 0.705 | 5.928 | 0.213 | 0.321 | 0.236 | 0.013 |
| hidden_user_action | 0.395 | 3.156 | 0.150 | 0.174 | 0.750 | 0.052 |
| prosody_high | 0.690 | 6.331 | 0.190 | 0.315 | 0.194 | 0.016 |
| prosody_low | 0.715 | 6.057 | 0.208 | 0.327 | 0.046 | 0.023 |

### Matched controls

| Control | Paired n | Domains | Effect | 95% CI | p |
|---|---:|---:|---:|---:|---:|
| Full audio - clue removed, post-gap | 168 | 14 | 10.1% | 3.6% to 17.3% | 0.0195 |
| Full audio - clue removed, immediate belief | 168 | 14 | 9.5% | 1.8% to 17.3% | 0.0532 |
| Full audio - clue removed, full trajectory | 168 | 14 | 0.0% | -2.4% to 2.4% | 1.0000 |
| Hidden user action - full audio, post-gap | 168 | 14 | 36.9% | 21.4% to 51.2% | 0.0015 |
| Hidden user action - full audio, immediate belief | 168 | 14 | 33.3% | 18.5% to 47.0% | 0.0022 |
| Transcript - full audio, pre-gap action | 168 | 14 | 7.7% | -2.4% to 17.9% | 0.2197 |
| Transcript - full audio, post-gap action | 168 | 14 | 0.6% | -7.7% to 8.9% | 1.0000 |
| Transcript - full audio, immediate belief | 168 | 14 | 12.5% | -0.6% to 25.6% | 0.1104 |
| Transcript - full audio, strict trajectory | 168 | 14 | 8.9% | 3.0% to 16.7% | 0.0312 |
| Full audio - no-state-change gap, post-gap | 168 | 14 | -3.6% | -19.6% to 13.7% | 0.7412 |
| No-state-change gap - full audio, immediate belief | 168 | 14 | 21.4% | 4.8% to 36.3% | 0.0297 |
| Short clue - full audio, post-gap action | 168 | 14 | 0.6% | -8.3% to 9.5% | 1.0000 |
| Short clue - full audio, immediate belief | 168 | 14 | -3.6% | -18.5% to 12.5% | 0.7231 |
| Neutral audio - full audio, immediate belief | 168 | 14 | -6.5% | -18.5% to 6.0% | 0.3696 |

### Prosody selectivity

- Identical-transcript pairs: 123; unique stimuli: 80.
- High-affect style accuracy: 13.5% [7.1%, 20.1%].
- Low-affect style accuracy: 43.4% [32.9%, 53.6%].
- Both deliveries correct: 1.4% [0.0%, 3.4%] (random pair chance 6.2%).
- Directional style contrast: -4.9% [-9.7%, 0.1%].
- Technical-action invariance: 62.8% [52.0%, 74.3%].
- Post-observation top-belief invariance: 46.3% [38.9%, 53.4%].
- Post-observation belief JSD: 0.279 [0.236, 0.321].
- Pre-final belief JSD: 0.303 [0.240, 0.365].

### Causal clue counterfactuals

Each pair changes only the early clue and corresponding hidden branch. Gold post-gap actions differ. After clue removal, a deterministic policy cannot exceed 50% post-gap accuracy across balanced indistinguishable branches.

| Condition | Pairs | Post | Strict | Both post-correct | Both strict | Action changes |
|---|---:|---:|---:|---:|---:|---:|
| full_audio | 84 | 35.1% | 1.2% | 11.9% | 0.0% | 64.3% |
| transcript_only | 84 | 35.7% | 10.1% | 8.3% | 1.2% | 60.7% |
| clue_removed | 84 | 25.0% | 1.2% | 1.2% | 0.0% | 53.6% |

### Full-audio slices

| Slice | n | Full pass | Two-action pass | Pre | Post |
|---|---:|---:|---:|---:|---:|
| domain: account_access | 12 | 0.0% | 25.0% | 75.0% | 25.0% |
| domain: banking | 12 | 0.0% | 41.7% | 100.0% | 41.7% |
| domain: education | 12 | 0.0% | 25.0% | 66.7% | 25.0% |
| domain: energy | 12 | 8.3% | 58.3% | 91.7% | 58.3% |
| domain: housing | 12 | 0.0% | 58.3% | 91.7% | 58.3% |
| domain: logistics | 12 | 0.0% | 0.0% | 8.3% | 0.0% |
| domain: mobile_service | 12 | 0.0% | 16.7% | 58.3% | 25.0% |
| domain: motor_insurance | 12 | 8.3% | 58.3% | 100.0% | 58.3% |
| domain: permits | 12 | 0.0% | 25.0% | 75.0% | 25.0% |
| domain: pharmacy | 12 | 0.0% | 25.0% | 66.7% | 25.0% |
| domain: repair | 12 | 0.0% | 16.7% | 25.0% | 33.3% |
| domain: scheduling | 12 | 0.0% | 25.0% | 75.0% | 25.0% |
| domain: tech_support | 12 | 0.0% | 41.7% | 75.0% | 50.0% |
| domain: travel | 12 | 0.0% | 41.7% | 66.7% | 41.7% |
| bucket: 1-2 | 56 | 1.8% | 41.1% | 71.4% | 41.1% |
| bucket: 12-20 | 56 | 1.8% | 25.0% | 67.9% | 28.6% |
| bucket: 5-8 | 56 | 0.0% | 32.1% | 69.6% | 35.7% |

### Failure tags

- `STATE_BELIEF_ERROR`: 1349 (94.0% of failed trajectories)
- `EARLY_CLUE_LOSS`: 492 (34.3% of failed trajectories)
- `TIME_INFERENCE_FAILURE`: 253 (17.6% of failed trajectories)
- `PROSODY_GROUNDING_FAILURE`: 241 (16.8% of failed trajectories)
- `PREMATURE_CLOSE`: 174 (12.1% of failed trajectories)
- `STATE_SYNC_FAILURE`: 126 (8.8% of failed trajectories)
- `PREMATURE_ESCALATION`: 104 (7.2% of failed trajectories)
- `BELIEF_REPORT_INVALID`: 65 (4.5% of failed trajectories)
- `ACTION_SELECTION_FAILURE`: 34 (2.4% of failed trajectories)
- `REPEATED_ACTION`: 8 (0.6% of failed trajectories)
- `OFF_MENU_RESPONSE`: 3 (0.2% of failed trajectories)

### Difficulty assessment

- No obvious ceiling or ineffective-clue warning fired.

## google/gemini-3-flash-preview

- Coverage: 1512/1512 trajectories (100.0%)
- Overall partial outcomes: 74.7% pre-gap, 48.1% post-gap, 38.2% both actions, 12.1% strict trajectory
- API calls: 22,934 (22,934 metered)
- Tokens: 39,273,546 (38,435,081 prompt + 838,465 completion)
- Reported API cost: $38.8486
- API request time: 3304.1 minutes

### Condition metrics

| Condition | n | Full pass | Pre | Post | Belief valid | Belief pre | Belief post | Cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| full_audio | 168 | 14.9% | 80.4% | 47.0% | 99.8% | 54.2% | 51.2% | $4.5797 |
| gap_no_state_change | 168 | 21.4% | 75.0% | 48.2% | 100.0% | 51.2% | 78.6% | $4.9085 |
| state_change_short | 168 | 11.9% | 66.1% | 42.3% | 100.0% | 48.8% | 50.6% | $4.7591 |
| clue_removed | 168 | 3.6% | 66.7% | 26.8% | 100.0% | 24.4% | 32.1% | $4.5812 |
| transcript_only | 168 | 21.4% | 84.5% | 58.3% | 100.0% | 57.1% | 64.3% | $0.7953 |
| neutral_audio | 168 | 10.7% | 78.0% | 45.2% | 99.8% | 51.2% | 54.2% | $4.7424 |
| hidden_user_action | 168 | 22.0% | 75.0% | 79.8% | 100.0% | 42.3% | 85.1% | $4.8394 |
| prosody_high | 168 | 0.6% | 74.4% | 44.6% | 100.0% | 48.2% | 51.2% | $4.8476 |
| prosody_low | 168 | 2.4% | 72.0% | 40.5% | 99.8% | 52.4% | 53.0% | $4.7954 |

### Belief probability metrics

| Condition | Brier | NLL | Normalized entropy | ECE | Revision gain | Stale mass |
|---|---:|---:|---:|---:|---:|---:|
| full_audio | 0.459 | 4.833 | 0.142 | 0.200 | 0.309 | 0.020 |
| gap_no_state_change | 0.325 | 2.592 | 0.168 | 0.125 | 0.585 | 0.013 |
| state_change_short | 0.489 | 5.166 | 0.150 | 0.207 | 0.280 | 0.022 |
| clue_removed | 0.896 | 8.816 | 0.268 | 0.391 | 0.224 | 0.018 |
| transcript_only | 0.320 | 2.811 | 0.123 | 0.142 | 0.413 | 0.025 |
| neutral_audio | 0.476 | 4.614 | 0.167 | 0.199 | 0.336 | 0.028 |
| hidden_user_action | 0.270 | 2.499 | 0.120 | 0.108 | 0.795 | 0.057 |
| prosody_high | 0.500 | 4.827 | 0.158 | 0.211 | 0.297 | 0.013 |
| prosody_low | 0.487 | 4.660 | 0.166 | 0.203 | 0.250 | 0.014 |

### Matched controls

| Control | Paired n | Domains | Effect | 95% CI | p |
|---|---:|---:|---:|---:|---:|
| Full audio - clue removed, post-gap | 168 | 14 | 20.2% | 9.5% to 30.4% | 0.0059 |
| Full audio - clue removed, immediate belief | 168 | 14 | 19.0% | 8.3% to 30.4% | 0.0093 |
| Full audio - clue removed, full trajectory | 168 | 14 | 11.3% | 4.8% to 17.9% | 0.0117 |
| Hidden user action - full audio, post-gap | 168 | 14 | 32.7% | 19.6% to 45.2% | 0.0012 |
| Hidden user action - full audio, immediate belief | 168 | 14 | 33.9% | 16.1% to 49.4% | 0.0044 |
| Transcript - full audio, pre-gap action | 168 | 14 | 4.2% | -4.2% to 13.7% | 0.4688 |
| Transcript - full audio, post-gap action | 168 | 14 | 11.3% | -0.6% to 23.8% | 0.1274 |
| Transcript - full audio, immediate belief | 168 | 14 | 13.1% | 5.4% to 20.8% | 0.0127 |
| Transcript - full audio, strict trajectory | 168 | 14 | 6.5% | -1.2% to 14.9% | 0.1885 |
| Full audio - no-state-change gap, post-gap | 168 | 14 | -1.2% | -9.5% to 6.5% | 0.8892 |
| No-state-change gap - full audio, immediate belief | 168 | 14 | 27.4% | 17.3% to 37.5% | 0.0010 |
| Short clue - full audio, post-gap action | 168 | 14 | -4.8% | -13.7% to 2.4% | 0.4062 |
| Short clue - full audio, immediate belief | 168 | 14 | -0.6% | -8.9% to 7.7% | 1.0000 |
| Neutral audio - full audio, immediate belief | 168 | 14 | 3.0% | -4.2% to 9.5% | 0.5107 |

### Prosody selectivity

- Identical-transcript pairs: 137; unique stimuli: 80.
- High-affect style accuracy: 18.6% [6.2%, 32.9%].
- Low-affect style accuracy: 38.8% [27.4%, 50.5%].
- Both deliveries correct: 6.0% [0.9%, 12.3%] (random pair chance 6.2%).
- Directional style contrast: 0.1% [-7.2%, 7.9%].
- Technical-action invariance: 61.9% [48.9%, 73.8%].
- Post-observation top-belief invariance: 53.6% [42.8%, 64.3%].
- Post-observation belief JSD: 0.238 [0.193, 0.286].
- Pre-final belief JSD: 0.242 [0.186, 0.299].

### Causal clue counterfactuals

Each pair changes only the early clue and corresponding hidden branch. Gold post-gap actions differ. After clue removal, a deterministic policy cannot exceed 50% post-gap accuracy across balanced indistinguishable branches.

| Condition | Pairs | Post | Strict | Both post-correct | Both strict | Action changes |
|---|---:|---:|---:|---:|---:|---:|
| full_audio | 84 | 47.0% | 14.9% | 16.7% | 3.6% | 75.0% |
| transcript_only | 84 | 58.3% | 21.4% | 32.1% | 6.0% | 59.5% |
| clue_removed | 84 | 26.8% | 3.6% | 3.6% | 1.2% | 40.5% |

### Full-audio slices

| Slice | n | Full pass | Two-action pass | Pre | Post |
|---|---:|---:|---:|---:|---:|
| domain: account_access | 12 | 8.3% | 50.0% | 100.0% | 50.0% |
| domain: banking | 12 | 25.0% | 66.7% | 100.0% | 66.7% |
| domain: education | 12 | 25.0% | 58.3% | 75.0% | 58.3% |
| domain: energy | 12 | 8.3% | 33.3% | 58.3% | 33.3% |
| domain: housing | 12 | 41.7% | 58.3% | 100.0% | 58.3% |
| domain: logistics | 12 | 16.7% | 25.0% | 50.0% | 33.3% |
| domain: mobile_service | 12 | 0.0% | 25.0% | 50.0% | 25.0% |
| domain: motor_insurance | 12 | 25.0% | 33.3% | 91.7% | 41.7% |
| domain: permits | 12 | 33.3% | 75.0% | 83.3% | 75.0% |
| domain: pharmacy | 12 | 16.7% | 66.7% | 91.7% | 66.7% |
| domain: repair | 12 | 8.3% | 33.3% | 58.3% | 33.3% |
| domain: scheduling | 12 | 0.0% | 25.0% | 75.0% | 33.3% |
| domain: tech_support | 12 | 0.0% | 41.7% | 100.0% | 41.7% |
| domain: travel | 12 | 0.0% | 41.7% | 91.7% | 41.7% |
| bucket: 1-2 | 56 | 10.7% | 41.1% | 75.0% | 42.9% |
| bucket: 12-20 | 56 | 19.6% | 48.2% | 82.1% | 48.2% |
| bucket: 5-8 | 56 | 14.3% | 46.4% | 83.9% | 50.0% |

### Failure tags

- `STATE_BELIEF_ERROR`: 1110 (83.5% of failed trajectories)
- `EARLY_CLUE_LOSS`: 415 (31.2% of failed trajectories)
- `PROSODY_GROUNDING_FAILURE`: 237 (17.8% of failed trajectories)
- `TIME_INFERENCE_FAILURE`: 146 (11.0% of failed trajectories)
- `PREMATURE_CLOSE`: 140 (10.5% of failed trajectories)
- `STATE_SYNC_FAILURE`: 91 (6.8% of failed trajectories)
- `PREMATURE_ESCALATION`: 75 (5.6% of failed trajectories)
- `ACTION_SELECTION_FAILURE`: 14 (1.1% of failed trajectories)
- `REPEATED_ACTION`: 4 (0.3% of failed trajectories)
- `BELIEF_REPORT_INVALID`: 3 (0.2% of failed trajectories)

### Difficulty assessment

- No obvious ceiling or ineffective-clue warning fired.

## openai/gpt-audio-mini

- Coverage: 1344/1344 trajectories (100.0%)
- Overall partial outcomes: 62.4% pre-gap, 26.6% post-gap, 19.7% both actions, 1.9% strict trajectory
- API calls: 20,227 (20,227 metered)
- Tokens: 19,568,263 (18,670,900 prompt + 897,363 completion)
- Reported API cost: $13.3562
- API request time: 2434.0 minutes

### Condition metrics

| Condition | n | Full pass | Pre | Post | Belief valid | Belief pre | Belief post | Cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| full_audio | 168 | 0.0% | 65.5% | 22.0% | 99.4% | 17.9% | 31.0% | $1.6853 |
| gap_no_state_change | 168 | 3.0% | 61.3% | 21.4% | 99.8% | 19.0% | 63.1% | $1.6647 |
| state_change_short | 168 | 1.2% | 66.7% | 20.8% | 100.0% | 15.5% | 32.7% | $1.6197 |
| clue_removed | 168 | 0.6% | 55.4% | 26.8% | 99.8% | 15.5% | 17.3% | $1.6656 |
| neutral_audio | 168 | 0.6% | 63.1% | 19.0% | 99.4% | 16.1% | 32.1% | $1.6807 |
| hidden_user_action | 168 | 8.9% | 65.5% | 63.1% | 99.8% | 19.6% | 67.9% | $1.6765 |
| prosody_high | 168 | 0.0% | 60.7% | 19.6% | 100.0% | 19.6% | 30.4% | $1.6766 |
| prosody_low | 168 | 0.6% | 60.7% | 20.2% | 99.8% | 20.8% | 40.5% | $1.6871 |

### Belief probability metrics

| Condition | Brier | NLL | Normalized entropy | ECE | Revision gain | Stale mass |
|---|---:|---:|---:|---:|---:|---:|
| full_audio | 0.559 | 1.326 | 0.803 | 0.078 | -0.010 | 0.103 |
| gap_no_state_change | 0.452 | 0.967 | 0.768 | 0.081 | 0.272 | 0.126 |
| state_change_short | 0.568 | 1.548 | 0.771 | 0.066 | -0.057 | 0.114 |
| clue_removed | 0.678 | 1.228 | 0.888 | 0.148 | 0.045 | 0.115 |
| neutral_audio | 0.561 | 1.135 | 0.801 | 0.057 | -0.008 | 0.117 |
| hidden_user_action | 0.394 | 0.991 | 0.652 | 0.083 | 0.435 | 0.120 |
| prosody_high | 0.579 | 1.367 | 0.795 | 0.069 | -0.027 | 0.111 |
| prosody_low | 0.541 | 1.425 | 0.804 | 0.047 | -0.010 | 0.119 |

### Matched controls

| Control | Paired n | Domains | Effect | 95% CI | p |
|---|---:|---:|---:|---:|---:|
| Full audio - clue removed, post-gap | 168 | 14 | -4.8% | -14.3% to 5.4% | 0.4336 |
| Full audio - clue removed, immediate belief | 168 | 14 | 13.7% | 6.0% to 21.4% | 0.0088 |
| Full audio - clue removed, full trajectory | 168 | 14 | -0.6% | -1.8% to 0.0% | 1.0000 |
| Hidden user action - full audio, post-gap | 168 | 14 | 41.1% | 22.0% to 57.1% | 0.0022 |
| Hidden user action - full audio, immediate belief | 168 | 14 | 36.9% | 19.0% to 52.4% | 0.0032 |
| Transcript - full audio, pre-gap action | 0 | 0 | N/A | N/A to N/A | N/A |
| Transcript - full audio, post-gap action | 0 | 0 | N/A | N/A to N/A | N/A |
| Transcript - full audio, immediate belief | 0 | 0 | N/A | N/A to N/A | N/A |
| Transcript - full audio, strict trajectory | 0 | 0 | N/A | N/A to N/A | N/A |
| Full audio - no-state-change gap, post-gap | 168 | 14 | 0.6% | -13.1% to 14.9% | 1.0000 |
| No-state-change gap - full audio, immediate belief | 168 | 14 | 32.1% | 19.0% to 44.6% | 0.0011 |
| Short clue - full audio, post-gap action | 168 | 14 | -1.2% | -6.5% to 4.8% | 0.8516 |
| Short clue - full audio, immediate belief | 168 | 14 | 1.8% | -6.0% to 8.9% | 0.7554 |
| Neutral audio - full audio, immediate belief | 168 | 14 | 1.2% | -5.4% to 7.7% | 0.8657 |

### Prosody selectivity

- Identical-transcript pairs: 119; unique stimuli: 71.
- High-affect style accuracy: 36.3% [24.6%, 48.4%].
- Low-affect style accuracy: 9.1% [5.8%, 12.5%].
- Both deliveries correct: 2.2% [0.0%, 4.6%] (random pair chance 6.2%).
- Directional style contrast: 6.5% [-6.5%, 19.9%].
- Technical-action invariance: 62.6% [50.1%, 75.2%].
- Post-observation top-belief invariance: 46.4% [35.9%, 56.7%].
- Post-observation belief JSD: 0.064 [0.054, 0.075].
- Pre-final belief JSD: 0.056 [0.046, 0.066].

### Causal clue counterfactuals

Each pair changes only the early clue and corresponding hidden branch. Gold post-gap actions differ. After clue removal, a deterministic policy cannot exceed 50% post-gap accuracy across balanced indistinguishable branches.

| Condition | Pairs | Post | Strict | Both post-correct | Both strict | Action changes |
|---|---:|---:|---:|---:|---:|---:|
| full_audio | 84 | 22.0% | 0.0% | 1.2% | 0.0% | 36.9% |
| clue_removed | 84 | 26.8% | 0.6% | 0.0% | 0.0% | 31.0% |

### Full-audio slices

| Slice | n | Full pass | Two-action pass | Pre | Post |
|---|---:|---:|---:|---:|---:|
| domain: account_access | 12 | 0.0% | 0.0% | 100.0% | 0.0% |
| domain: banking | 12 | 0.0% | 50.0% | 91.7% | 50.0% |
| domain: education | 12 | 0.0% | 8.3% | 58.3% | 8.3% |
| domain: energy | 12 | 0.0% | 16.7% | 66.7% | 16.7% |
| domain: housing | 12 | 0.0% | 50.0% | 100.0% | 50.0% |
| domain: logistics | 12 | 0.0% | 8.3% | 25.0% | 8.3% |
| domain: mobile_service | 12 | 0.0% | 16.7% | 66.7% | 16.7% |
| domain: motor_insurance | 12 | 0.0% | 0.0% | 25.0% | 8.3% |
| domain: permits | 12 | 0.0% | 8.3% | 58.3% | 16.7% |
| domain: pharmacy | 12 | 0.0% | 0.0% | 50.0% | 8.3% |
| domain: repair | 12 | 0.0% | 25.0% | 83.3% | 33.3% |
| domain: scheduling | 12 | 0.0% | 0.0% | 41.7% | 8.3% |
| domain: tech_support | 12 | 0.0% | 25.0% | 58.3% | 33.3% |
| domain: travel | 12 | 0.0% | 50.0% | 91.7% | 50.0% |
| bucket: 1-2 | 56 | 0.0% | 14.3% | 64.3% | 17.9% |
| bucket: 12-20 | 56 | 0.0% | 19.6% | 69.6% | 23.2% |
| bucket: 5-8 | 56 | 0.0% | 21.4% | 62.5% | 25.0% |

### Failure tags

- `STATE_BELIEF_ERROR`: 1265 (95.9% of failed trajectories)
- `EARLY_CLUE_LOSS`: 696 (52.8% of failed trajectories)
- `PROSODY_GROUNDING_FAILURE`: 257 (19.5% of failed trajectories)
- `STATE_SYNC_FAILURE`: 169 (12.8% of failed trajectories)
- `TIME_INFERENCE_FAILURE`: 93 (7.1% of failed trajectories)
- `PREMATURE_ESCALATION`: 52 (3.9% of failed trajectories)
- `PREMATURE_CLOSE`: 38 (2.9% of failed trajectories)
- `REPEATED_ACTION`: 30 (2.3% of failed trajectories)
- `BELIEF_REPORT_INVALID`: 10 (0.8% of failed trajectories)
- `ACTION_SELECTION_FAILURE`: 3 (0.2% of failed trajectories)

### Difficulty assessment

- The domain-clustered clue-ablation interval crosses zero; construct validity is not established for this model.

## Interpretation cautions

- Results contain 2 observed run seed(s); pass@k is labeled with the number actually available.
- `transcript_only` is a control; audio conditions replay synthesized alternating turns.
- Human annotation and audible-prosody validation remain separate validation steps and are not replaced by model scores.
