# R4. The four-way belief/action split

All four categories come straight out of `belief_action_outcome`, which `_belief_checkpoint()` (`dual_audio/interaction/runner.py:170`) already writes into every trajectory. Nothing here is newly defined.

- `FULL_SUCCESS` -- belief correct on every variable and action correct
- `ACTION_SELECTION_FAILURE` -- belief correct, action wrong
- `LUCKY_ACTION` -- belief wrong, action right
- `STATE_SYNCHRONIZATION_FAILURE` -- both wrong

## Final checkpoint

| Model | Condition | Full success | Action fail | Lucky | State fail | Action/belief consistent | Risk calib. consistent |
|---|---|---|---|---|---|---|---|
| Gemini 2.5 | Ordinary audio | 29.8 | 10.1 | **5.4** | 54.8 | 57.5 | 87.5 |
| Gemini 2.5 | No state change | 27.4 | 17.3 | **11.3** | 44.0 | 56.5 | 82.1 |
| Gemini 2.5 | Short clue | 21.4 | 16.7 | **14.3** | 47.6 | 45.5 | 80.4 |
| Gemini 2.5 | Clue removed | 18.5 | 10.1 | **6.5** | 64.9 | 44.6 | 78.6 |
| Gemini 2.5 | Transcript | 32.7 | 18.5 | **3.0** | 45.8 | 50.6 | 77.4 |
| Gemini 2.5 | Neutral audio | 26.2 | 12.5 | **5.4** | 56.0 | 52.7 | 80.4 |
| Gemini 2.5 | Explicit user update | 63.7 | 8.3 | **8.3** | 19.6 | 79.6 | 94.0 |
| Gemini 2.5 | High prosody | 29.8 | 7.1 | **7.1** | 56.0 | 56.3 | 79.2 |
| Gemini 2.5 | Low prosody | 25.6 | 12.5 | **6.5** | 55.4 | 47.9 | 79.8 |
| Gemini 3 | Ordinary audio | 44.6 | 19.0 | **2.4** | 33.9 | 61.9 | 81.0 |
| Gemini 3 | No state change | 38.7 | 32.1 | **9.5** | 19.6 | 59.5 | 75.6 |
| Gemini 3 | Short clue | 32.7 | 20.2 | **9.5** | 37.5 | 58.9 | 78.6 |
| Gemini 3 | Clue removed | 22.6 | 11.9 | **4.2** | 61.3 | 44.0 | 62.5 |
| Gemini 3 | Transcript | 56.5 | 18.5 | **1.8** | 23.2 | 62.5 | 81.0 |
| Gemini 3 | Neutral audio | 38.7 | 18.5 | **6.5** | 36.3 | 58.3 | 76.2 |
| Gemini 3 | Explicit user update | 78.6 | 12.5 | **1.2** | 7.7 | 86.3 | 90.5 |
| Gemini 3 | High prosody | 35.7 | 19.0 | **8.9** | 36.3 | 50.6 | 62.5 |
| Gemini 3 | Low prosody | 32.7 | 21.4 | **7.7** | 38.1 | 55.1 | 67.9 |
| GPT Audio Mini | Ordinary audio | 10.7 | 19.6 | **11.3** | 58.3 | 25.6 | 57.1 |
| GPT Audio Mini | No state change | 13.1 | 42.3 | **8.3** | 36.3 | 32.7 | 63.7 |
| GPT Audio Mini | Short clue | 11.9 | 15.5 | **8.9** | 63.7 | 31.0 | 64.3 |
| GPT Audio Mini | Clue removed | 7.7 | 13.1 | **19.0** | 60.1 | 28.1 | 76.8 |
| GPT Audio Mini | Neutral audio | 11.3 | 22.6 | **7.7** | 58.3 | 34.3 | 57.7 |
| GPT Audio Mini | Explicit user update | 53.6 | 8.3 | **9.5** | 28.6 | 69.0 | 79.2 |
| GPT Audio Mini | High prosody | 10.7 | 14.9 | **8.9** | 65.5 | 32.1 | 58.9 |
| GPT Audio Mini | Low prosody | 10.1 | 22.0 | **10.1** | 57.7 | 31.0 | 58.3 |

## Pre-gap checkpoint

| Model | Condition | Full success | Action fail | Lucky | State fail | Action/belief consistent | Risk calib. consistent |
|---|---|---|---|---|---|---|---|
| Gemini 2.5 | Ordinary audio | 4.2 | 1.8 | 65.5 | 28.6 | 9.8 | 83.3 |
| Gemini 2.5 | No state change | 23.8 | 7.7 | 44.0 | 24.4 | 33.1 | 85.7 |
| Gemini 2.5 | Short clue | 19.0 | 10.7 | 44.6 | 25.6 | 26.2 | 78.0 |
| Gemini 2.5 | Clue removed | 6.0 | 4.2 | 53.6 | 36.3 | 24.1 | 60.7 |
| Gemini 2.5 | Transcript | 38.7 | 13.1 | 38.7 | 9.5 | 39.9 | 83.3 |
| Gemini 2.5 | Neutral audio | 17.9 | 11.9 | 47.0 | 23.2 | 28.6 | 77.4 |
| Gemini 2.5 | Explicit user update | 22.0 | 11.9 | 41.7 | 24.4 | 33.1 | 73.8 |
| Gemini 2.5 | High prosody | 20.8 | 9.5 | 47.6 | 22.0 | 34.0 | 82.7 |
| Gemini 2.5 | Low prosody | 20.8 | 4.2 | 42.9 | 32.1 | 30.2 | 80.4 |
| Gemini 3 | Ordinary audio | 43.5 | 10.7 | 36.9 | 8.9 | 48.5 | 89.9 |
| Gemini 3 | No state change | 38.1 | 13.1 | 36.9 | 11.9 | 41.7 | 85.7 |
| Gemini 3 | Short clue | 36.9 | 11.9 | 29.2 | 22.0 | 39.3 | 83.3 |
| Gemini 3 | Clue removed | 14.9 | 9.5 | 51.8 | 23.8 | 38.7 | 61.9 |
| Gemini 3 | Transcript | 46.4 | 10.7 | 38.1 | 4.8 | 47.0 | 83.3 |
| Gemini 3 | Neutral audio | 38.1 | 13.1 | 39.9 | 8.9 | 40.7 | 83.3 |
| Gemini 3 | Explicit user update | 29.2 | 13.1 | 45.8 | 11.9 | 31.0 | 83.9 |
| Gemini 3 | High prosody | 37.5 | 10.7 | 36.9 | 14.9 | 40.5 | 90.5 |
| Gemini 3 | Low prosody | 35.1 | 17.3 | 36.9 | 10.7 | 38.7 | 85.7 |
| GPT Audio Mini | Ordinary audio | 10.1 | 7.7 | 55.4 | 26.8 | 15.0 | 61.3 |
| GPT Audio Mini | No state change | 8.9 | 10.1 | 52.4 | 28.6 | 16.2 | 62.5 |
| GPT Audio Mini | Short clue | 7.7 | 7.7 | 58.9 | 25.6 | 11.9 | 61.9 |
| GPT Audio Mini | Clue removed | 8.9 | 6.5 | 46.4 | 38.1 | 22.0 | 75.0 |
| GPT Audio Mini | Neutral audio | 11.3 | 4.8 | 51.8 | 32.1 | 16.1 | 58.3 |
| GPT Audio Mini | Explicit user update | 10.1 | 9.5 | 55.4 | 25.0 | 16.2 | 65.5 |
| GPT Audio Mini | High prosody | 11.3 | 8.3 | 49.4 | 31.0 | 19.6 | 67.3 |
| GPT Audio Mini | Low prosody | 8.9 | 11.9 | 51.8 | 27.4 | 15.6 | 60.1 |

## Lucky action by causal branch (final checkpoint)

`share of correct` is the fraction of the model's *correct* final actions that rested on a wrong belief. That is the unearned fraction of the reported action accuracy.

| Model | Condition | Misaligned: % rows | Misaligned: share of correct | Aligned: % rows | Aligned: share of correct | All: % rows | All: share of correct |
|---|---|---|---|---|---|---|---|
| Gemini 2.5 | Ordinary audio | 7.1 | 14.3 | 3.6 | 17.6 | 5.4 | 15.3 |
| Gemini 2.5 | No state change | 13.1 | 52.4 | 9.5 | 18.2 | 11.3 | 29.2 |
| Gemini 2.5 | Short clue | 16.7 | 36.8 | 11.9 | 45.5 | 14.3 | 40.0 |
| Gemini 2.5 | Clue removed | 11.9 | 27.0 | 1.2 | 20.0 | 6.5 | 26.2 |
| Gemini 2.5 | Transcript | 3.6 | 5.7 | 2.4 | 28.6 | 3.0 | 8.3 |
| Gemini 2.5 | Neutral audio | 7.1 | 14.3 | 3.6 | 27.3 | 5.4 | 17.0 |
| Gemini 2.5 | Explicit user update | 11.9 | 16.9 | 4.8 | 6.5 | 8.3 | 11.6 |
| Gemini 2.5 | High prosody | 11.9 | 19.6 | 2.4 | 18.2 | 7.1 | 19.4 |
| Gemini 2.5 | Low prosody | 10.7 | 20.5 | 2.4 | 20.0 | 6.5 | 20.4 |
| Gemini 3 | Ordinary audio | 4.8 | 7.8 | 0.0 | 0.0 | 2.4 | 5.1 |
| Gemini 3 | No state change | 16.7 | 73.7 | 2.4 | 3.2 | 9.5 | 19.8 |
| Gemini 3 | Short clue | 11.9 | 24.4 | 7.1 | 20.0 | 9.5 | 22.5 |
| Gemini 3 | Clue removed | 7.1 | 16.2 | 1.2 | 12.5 | 4.2 | 15.6 |
| Gemini 3 | Transcript | 2.4 | 3.3 | 1.2 | 2.7 | 1.8 | 3.1 |
| Gemini 3 | Neutral audio | 8.3 | 14.3 | 4.8 | 14.8 | 6.5 | 14.5 |
| Gemini 3 | Explicit user update | 0.0 | 0.0 | 2.4 | 3.1 | 1.2 | 1.5 |
| Gemini 3 | High prosody | 15.5 | 26.0 | 2.4 | 8.0 | 8.9 | 20.0 |
| Gemini 3 | Low prosody | 9.5 | 16.7 | 6.0 | 25.0 | 7.7 | 19.1 |
| GPT Audio Mini | Ordinary audio | 22.6 | 57.6 | 0.0 | 0.0 | 11.3 | 51.4 |
| GPT Audio Mini | No state change | 13.1 | 84.6 | 3.6 | 13.0 | 8.3 | 38.9 |
| GPT Audio Mini | Short clue | 16.7 | 43.8 | 1.2 | 33.3 | 8.9 | 42.9 |
| GPT Audio Mini | Clue removed | 32.1 | 69.2 | 6.0 | 83.3 | 19.0 | 71.1 |
| GPT Audio Mini | Neutral audio | 13.1 | 36.7 | 2.4 | 100.0 | 7.7 | 40.6 |
| GPT Audio Mini | Explicit user update | 14.3 | 27.9 | 4.8 | 6.3 | 9.5 | 15.1 |
| GPT Audio Mini | High prosody | 15.5 | 43.3 | 2.4 | 66.7 | 8.9 | 45.5 |
| GPT Audio Mini | Low prosody | 19.0 | 50.0 | 1.2 | 50.0 | 10.1 | 50.0 |

## Reading

Under ordinary audio the final-checkpoint split is dominated by joint failure: `STATE_SYNCHRONIZATION_FAILURE` accounts for 54.8/33.9/58.3 of all trajectories, against `FULL_SUCCESS` at 29.8/44.6/10.7.

**Lucky actions are a small share of the total but a large share of the successes.** Under ordinary audio, 15.3%/5.1%/51.4% of every correct final action rests on an incorrect state belief (Gemini 2.5 / Gemini 3 / GPT Audio Mini). That is the quantity to quote when the paper says action accuracy overstates state competence.

Action/belief consistency -- whether the chosen action matches the action implied by the model's own top belief -- is 57.5/61.9/25.6 under ordinary audio. The gap between that and 100 is the model contradicting its own stated belief, which is a different failure from getting the belief wrong.

Risk calibration consistency -- whether `needs_revalidation` matches whether mean confidence actually fell below the scenario threshold -- is 87.5/81.0/57.1. This is the weakest of the derived diagnostics and worth reporting only as a calibration footnote.
