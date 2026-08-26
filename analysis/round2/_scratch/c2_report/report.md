# DUAL-AudioBench evaluation report

- Raw attempt rows: 1512
- Unique completed trajectories: 1512
- Duplicate successful rows ignored in metrics: 0
- API/runtime error attempts: 0
- Models: google/gemini-3-flash-preview

A trajectory passes only when both actions, any scored response style, all belief reports, and all hidden-state top predictions pass.

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
| Full audio - clue removed, immediate belief | 168 | 14 | 19.0% | 7.7% to 30.4% | 0.0093 |
| Full audio - clue removed, full trajectory | 168 | 14 | 11.3% | 4.8% to 17.9% | 0.0117 |
| Hidden user action - full audio, post-gap | 168 | 14 | 32.7% | 19.6% to 45.2% | 0.0012 |
| Hidden user action - full audio, immediate belief | 168 | 14 | 33.9% | 16.1% to 49.4% | 0.0044 |
| Transcript - full audio, pre-gap action | 168 | 14 | 4.2% | -4.2% to 13.7% | 0.4688 |
| Transcript - full audio, post-gap action | 168 | 14 | 11.3% | -0.6% to 23.8% | 0.1274 |
| Transcript - full audio, immediate belief | 168 | 14 | 13.1% | 5.4% to 20.8% | 0.0127 |
| Transcript - full audio, strict trajectory | 168 | 14 | 6.5% | -1.2% to 14.9% | 0.1885 |
| Full audio - no-state-change gap, post-gap | 168 | 14 | -1.2% | -9.5% to 7.1% | 0.8892 |
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

### Joint belief/action outcomes (final checkpoint)

| Condition | Full success | Action fail | Lucky | State fail | Lucky share of correct | Action/belief consistent |
|---|---|---|---|---|---|---|
| full_audio | 44.6% | 19.0% | 2.4% | 33.9% | 5.1% | 61.9% |
| gap_no_state_change | 38.7% | 32.1% | 9.5% | 19.6% | 19.8% | 59.5% |
| state_change_short | 32.7% | 20.2% | 9.5% | 37.5% | 22.5% | 58.9% |
| clue_removed | 22.6% | 11.9% | 4.2% | 61.3% | 15.6% | 44.0% |
| transcript_only | 56.5% | 18.5% | 1.8% | 23.2% | 3.1% | 62.5% |
| neutral_audio | 38.7% | 18.5% | 6.5% | 36.3% | 14.5% | 58.3% |
| hidden_user_action | 78.6% | 12.5% | 1.2% | 7.7% | 1.5% | 86.3% |
| prosody_high | 35.7% | 19.0% | 8.9% | 36.3% | 20.0% | 50.6% |
| prosody_low | 32.7% | 21.4% | 7.7% | 38.1% | 19.1% | 55.1% |

`Lucky` is a correct action on top of an incorrect state belief. `Lucky share of correct` is therefore the fraction of the reported action accuracy that is not backed by a correct state estimate.

### Belief revision across the gap

| Condition | k obs | Revision gain | Reflection gain | Final revision gain | Stale mass | Contributing variables |
|---|---|---|---|---|---|---|
| full_audio | 130 | 0.309 | 0.089 | 0.398 | 0.020 | 130 domain-outcome, no causal_alignment |
| gap_no_state_change | 117 | 0.585 | -0.085 | 0.500 | 0.013 | 117 domain-outcome, no causal_alignment |
| state_change_short | 112 | 0.280 | 0.042 | 0.322 | 0.022 | 112 domain-outcome, no causal_alignment |
| clue_removed | 111 | 0.224 | 0.021 | 0.245 | 0.018 | 111 domain-outcome, no causal_alignment |
| transcript_only | 137 | 0.413 | 0.119 | 0.532 | 0.025 | 137 domain-outcome, no causal_alignment |
| neutral_audio | 127 | 0.336 | 0.032 | 0.368 | 0.028 | 127 domain-outcome, no causal_alignment |
| hidden_user_action | 198 | 0.811 | 0.051 | 0.862 | 0.047 | 126 domain-outcome, 72 causal_alignment |
| prosody_high | 123 | 0.297 | 0.020 | 0.318 | 0.013 | 123 domain-outcome, no causal_alignment |
| prosody_low | 116 | 0.250 | 0.020 | 0.270 | 0.014 | 116 domain-outcome, no causal_alignment |

Revision gain is the probability mass moved onto the new true state by the resumed evidence, pooled over variables whose true state actually changed. Reflection gain is the further movement between the belief-only checkpoint and the final action, where no new evidence arrives. Stale mass is the probability still on the superseded state.

### Difficulty assessment

- No obvious ceiling or ineffective-clue warning fired.

## Interpretation cautions

- Results contain 2 observed run seed(s); pass@k is labeled with the number actually available.
- `transcript_only` is a control; audio conditions replay synthesized alternating turns.
- Human annotation and audible-prosody validation remain separate validation steps and are not replaced by model scores.
