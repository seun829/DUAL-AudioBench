# R6. Per-variable belief accuracy

`outcome variable` is the domain state variable (`dispute_status`, `firmware_status`, `connection_status`, ...); `causal_alignment` is the two-valued branch variable. `both correct` is exactly the `all_correct` figure the paper reports as belief accuracy.

## After the gap (the checkpoint the paper reports)

| Model | Condition | Outcome var | Alignment | Both (= reported) | Alignment only | Outcome only | Neither |
|---|---|---|---|---|---|---|---|
| Gemini 2.5 | Ordinary audio | 42.3 | 76.2 | **39.3** | 36.9 | 3.0 | 20.8 |
| Gemini 2.5 | No state change | 68.5 | 85.1 | **60.7** | 24.4 | 7.7 | 7.1 |
| Gemini 2.5 | Short clue | 39.3 | 81.5 | **35.7** | 45.8 | 3.6 | 14.9 |
| Gemini 2.5 | Clue removed | 38.1 | 51.8 | **29.8** | 22.0 | 8.3 | 39.9 |
| Gemini 2.5 | Transcript | 53.6 | 94.0 | **51.8** | 42.3 | 1.8 | 4.2 |
| Gemini 2.5 | Neutral audio | 39.3 | 75.0 | **32.7** | 42.3 | 6.5 | 18.5 |
| Gemini 2.5 | Explicit user update | 75.0 | 91.7 | **72.6** | 19.0 | 2.4 | 6.0 |
| Gemini 2.5 | High prosody | 42.9 | 79.8 | **37.5** | 42.3 | 5.4 | 14.9 |
| Gemini 2.5 | Low prosody | 38.1 | 80.4 | **35.7** | 44.6 | 2.4 | 17.3 |
| Gemini 3 | Ordinary audio | 51.8 | 90.5 | **51.2** | 39.3 | 0.6 | 8.9 |
| Gemini 3 | No state change | 87.5 | 90.5 | **78.6** | 11.9 | 8.9 | 0.6 |
| Gemini 3 | Short clue | 50.6 | 95.8 | **50.6** | 45.2 | 0.0 | 4.2 |
| Gemini 3 | Clue removed | 48.8 | 48.2 | **32.1** | 16.1 | 16.7 | 35.1 |
| Gemini 3 | Transcript | 65.5 | 94.0 | **64.3** | 29.8 | 1.2 | 4.8 |
| Gemini 3 | Neutral audio | 55.4 | 91.1 | **54.2** | 36.9 | 1.2 | 7.7 |
| Gemini 3 | Explicit user update | 87.5 | 96.4 | **85.1** | 11.3 | 2.4 | 1.2 |
| Gemini 3 | High prosody | 53.0 | 92.9 | **51.2** | 41.7 | 1.8 | 5.4 |
| Gemini 3 | Low prosody | 56.0 | 91.7 | **53.0** | 38.7 | 3.0 | 5.4 |
| GPT Audio Mini | Ordinary audio | 35.1 | 84.5 | **31.0** | 53.6 | 4.2 | 11.3 |
| GPT Audio Mini | No state change | 75.0 | 84.5 | **63.1** | 21.4 | 11.9 | 3.6 |
| GPT Audio Mini | Short clue | 33.3 | 92.3 | **32.7** | 59.5 | 0.6 | 7.1 |
| GPT Audio Mini | Clue removed | 40.5 | 46.4 | **17.3** | 29.2 | 23.2 | 30.4 |
| GPT Audio Mini | Neutral audio | 38.7 | 82.7 | **32.1** | 50.6 | 6.5 | 10.7 |
| GPT Audio Mini | Explicit user update | 70.2 | 93.5 | **67.9** | 25.6 | 2.4 | 4.2 |
| GPT Audio Mini | High prosody | 34.5 | 85.1 | **30.4** | 54.8 | 4.2 | 10.7 |
| GPT Audio Mini | Low prosody | 43.5 | 89.3 | **40.5** | 48.8 | 3.0 | 7.7 |

## Which variable is missed, as a share of conjunction failures

| Model | Condition | % of failures missing alignment | % of failures missing outcome |
|---|---|---|---|
| Gemini 2.5 | Ordinary audio | 39.2 | 95.1 |
| Gemini 2.5 | No state change | 37.9 | 80.3 |
| Gemini 2.5 | Short clue | 28.7 | 94.4 |
| Gemini 2.5 | Clue removed | 68.6 | 88.1 |
| Gemini 2.5 | Transcript | 12.3 | 96.3 |
| Gemini 2.5 | Neutral audio | 37.2 | 90.3 |
| Gemini 2.5 | Explicit user update | 30.4 | 91.3 |
| Gemini 2.5 | High prosody | 32.4 | 91.4 |
| Gemini 2.5 | Low prosody | 30.6 | 96.3 |
| Gemini 3 | Ordinary audio | 19.5 | 98.8 |
| Gemini 3 | No state change | 44.4 | 58.3 |
| Gemini 3 | Short clue | 8.4 | 100.0 |
| Gemini 3 | Clue removed | 76.3 | 75.4 |
| Gemini 3 | Transcript | 16.7 | 96.7 |
| Gemini 3 | Neutral audio | 19.5 | 97.4 |
| Gemini 3 | Explicit user update | 24.0 | 84.0 |
| Gemini 3 | High prosody | 14.6 | 96.3 |
| Gemini 3 | Low prosody | 17.7 | 93.7 |
| GPT Audio Mini | Ordinary audio | 22.4 | 94.0 |
| GPT Audio Mini | No state change | 41.9 | 67.7 |
| GPT Audio Mini | Short clue | 11.5 | 99.1 |
| GPT Audio Mini | Clue removed | 64.7 | 71.9 |
| GPT Audio Mini | Neutral audio | 25.4 | 90.4 |
| GPT Audio Mini | Explicit user update | 20.4 | 92.6 |
| GPT Audio Mini | High prosody | 21.4 | 94.0 |
| GPT Audio Mini | Low prosody | 18.0 | 95.0 |

## All three checkpoints

| Model | Condition | Checkpoint | n | Outcome | Alignment | Both | Align only | Outcome only | Neither | fail: missed align | fail: missed outcome |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Gemini 2.5 | Ordinary audio | pre-gap | 168 | 7.1 | 82.7 | 6.0 | 76.8 | 1.2 | 16.1 | 18.4 | 98.7 |
| Gemini 2.5 | Ordinary audio | after gap | 168 | 42.3 | 76.2 | 39.3 | 36.9 | 3.0 | 20.8 | 39.2 | 95.1 |
| Gemini 2.5 | Ordinary audio | final | 168 | 44.0 | 78.6 | 39.9 | 38.7 | 4.2 | 17.3 | 35.6 | 93.1 |
| Gemini 2.5 | No state change | pre-gap | 168 | 33.9 | 89.3 | 31.5 | 57.7 | 2.4 | 8.3 | 15.7 | 96.5 |
| Gemini 2.5 | No state change | after gap | 168 | 68.5 | 85.1 | 60.7 | 24.4 | 7.7 | 7.1 | 37.9 | 80.3 |
| Gemini 2.5 | No state change | final | 168 | 47.6 | 85.7 | 44.6 | 41.1 | 3.0 | 11.3 | 25.8 | 94.6 |
| Gemini 2.5 | Short clue | pre-gap | 168 | 31.5 | 91.7 | 29.8 | 61.9 | 1.8 | 6.5 | 11.9 | 97.5 |
| Gemini 2.5 | Short clue | after gap | 168 | 39.3 | 81.5 | 35.7 | 45.8 | 3.6 | 14.9 | 28.7 | 94.4 |
| Gemini 2.5 | Short clue | final | 168 | 44.0 | 81.0 | 38.1 | 42.9 | 6.0 | 13.1 | 30.8 | 90.4 |
| Gemini 2.5 | Clue removed | pre-gap | 168 | 19.6 | 51.8 | 10.1 | 41.7 | 9.5 | 38.7 | 53.6 | 89.4 |
| Gemini 2.5 | Clue removed | after gap | 168 | 38.1 | 51.8 | 29.8 | 22.0 | 8.3 | 39.9 | 68.6 | 88.1 |
| Gemini 2.5 | Clue removed | final | 168 | 36.3 | 48.8 | 28.6 | 20.2 | 7.7 | 43.5 | 71.7 | 89.2 |
| Gemini 2.5 | Transcript | pre-gap | 168 | 53.6 | 94.0 | 51.8 | 42.3 | 1.8 | 4.2 | 12.3 | 96.3 |
| Gemini 2.5 | Transcript | after gap | 168 | 53.6 | 94.0 | 51.8 | 42.3 | 1.8 | 4.2 | 12.3 | 96.3 |
| Gemini 2.5 | Transcript | final | 168 | 53.6 | 88.1 | 51.2 | 36.9 | 2.4 | 9.5 | 24.4 | 95.1 |
| Gemini 2.5 | Neutral audio | pre-gap | 168 | 33.9 | 83.9 | 29.8 | 54.2 | 4.2 | 11.9 | 22.9 | 94.1 |
| Gemini 2.5 | Neutral audio | after gap | 168 | 39.3 | 75.0 | 32.7 | 42.3 | 6.5 | 18.5 | 37.2 | 90.3 |
| Gemini 2.5 | Neutral audio | final | 168 | 44.0 | 78.0 | 38.7 | 39.3 | 5.4 | 16.7 | 35.9 | 91.3 |
| Gemini 2.5 | Explicit user update | pre-gap | 168 | 37.5 | 87.5 | 33.9 | 53.6 | 3.6 | 8.9 | 18.9 | 94.6 |
| Gemini 2.5 | Explicit user update | after gap | 168 | 75.0 | 91.7 | 72.6 | 19.0 | 2.4 | 6.0 | 30.4 | 91.3 |
| Gemini 2.5 | Explicit user update | final | 168 | 74.4 | 92.9 | 72.0 | 20.8 | 2.4 | 4.8 | 25.5 | 91.5 |
| Gemini 2.5 | High prosody | pre-gap | 168 | 36.9 | 84.5 | 30.4 | 54.2 | 6.5 | 8.9 | 22.2 | 90.6 |
| Gemini 2.5 | High prosody | after gap | 168 | 42.9 | 79.8 | 37.5 | 42.3 | 5.4 | 14.9 | 32.4 | 91.4 |
| Gemini 2.5 | High prosody | final | 168 | 45.2 | 74.4 | 36.9 | 37.5 | 8.3 | 17.3 | 40.6 | 86.8 |
| Gemini 2.5 | Low prosody | pre-gap | 168 | 31.5 | 80.4 | 25.0 | 55.4 | 6.5 | 13.1 | 26.2 | 91.3 |
| Gemini 2.5 | Low prosody | after gap | 168 | 38.1 | 80.4 | 35.7 | 44.6 | 2.4 | 17.3 | 30.6 | 96.3 |
| Gemini 2.5 | Low prosody | final | 168 | 43.5 | 79.8 | 38.1 | 41.7 | 5.4 | 14.9 | 32.7 | 91.3 |
| Gemini 3 | Ordinary audio | pre-gap | 168 | 57.1 | 93.5 | 54.2 | 39.3 | 3.0 | 3.6 | 14.3 | 93.5 |
| Gemini 3 | Ordinary audio | after gap | 168 | 51.8 | 90.5 | 51.2 | 39.3 | 0.6 | 8.9 | 19.5 | 98.8 |
| Gemini 3 | Ordinary audio | final | 168 | 64.3 | 88.1 | 63.7 | 24.4 | 0.6 | 11.3 | 32.8 | 98.4 |
| Gemini 3 | No state change | pre-gap | 168 | 52.4 | 91.7 | 51.2 | 40.5 | 1.2 | 7.1 | 17.1 | 97.6 |
| Gemini 3 | No state change | after gap | 168 | 87.5 | 90.5 | 78.6 | 11.9 | 8.9 | 0.6 | 44.4 | 58.3 |
| Gemini 3 | No state change | final | 168 | 79.8 | 89.9 | 70.8 | 19.0 | 8.9 | 1.2 | 34.7 | 69.4 |
| Gemini 3 | Short clue | pre-gap | 168 | 50.0 | 95.8 | 48.8 | 47.0 | 1.2 | 3.0 | 8.1 | 97.7 |
| Gemini 3 | Short clue | after gap | 168 | 50.6 | 95.8 | 50.6 | 45.2 | 0.0 | 4.2 | 8.4 | 100.0 |
| Gemini 3 | Short clue | final | 168 | 55.4 | 92.9 | 53.0 | 39.9 | 2.4 | 4.8 | 15.2 | 94.9 |
| Gemini 3 | Clue removed | pre-gap | 168 | 53.6 | 45.8 | 24.4 | 21.4 | 29.2 | 25.0 | 71.7 | 61.4 |
| Gemini 3 | Clue removed | after gap | 168 | 48.8 | 48.2 | 32.1 | 16.1 | 16.7 | 35.1 | 76.3 | 75.4 |
| Gemini 3 | Clue removed | final | 168 | 49.4 | 46.4 | 34.5 | 11.9 | 14.9 | 38.7 | 81.8 | 77.3 |
| Gemini 3 | Transcript | pre-gap | 168 | 59.5 | 97.0 | 57.1 | 39.9 | 2.4 | 0.6 | 6.9 | 94.4 |
| Gemini 3 | Transcript | after gap | 168 | 65.5 | 94.0 | 64.3 | 29.8 | 1.2 | 4.8 | 16.7 | 96.7 |
| Gemini 3 | Transcript | final | 168 | 76.2 | 93.5 | 75.0 | 18.5 | 1.2 | 5.4 | 26.2 | 95.2 |
| Gemini 3 | Neutral audio | pre-gap | 168 | 54.2 | 90.5 | 51.2 | 39.3 | 3.0 | 6.5 | 19.5 | 93.9 |
| Gemini 3 | Neutral audio | after gap | 168 | 55.4 | 91.1 | 54.2 | 36.9 | 1.2 | 7.7 | 19.5 | 97.4 |
| Gemini 3 | Neutral audio | final | 168 | 58.3 | 90.5 | 57.1 | 33.3 | 1.2 | 8.3 | 22.2 | 97.2 |
| Gemini 3 | Explicit user update | pre-gap | 168 | 46.4 | 89.9 | 42.3 | 47.6 | 4.2 | 6.0 | 17.5 | 92.8 |
| Gemini 3 | Explicit user update | after gap | 168 | 87.5 | 96.4 | 85.1 | 11.3 | 2.4 | 1.2 | 24.0 | 84.0 |
| Gemini 3 | Explicit user update | final | 168 | 91.7 | 98.2 | 91.1 | 7.1 | 0.6 | 1.2 | 20.0 | 93.3 |
| Gemini 3 | High prosody | pre-gap | 168 | 50.6 | 94.0 | 48.2 | 45.8 | 2.4 | 3.6 | 11.5 | 95.4 |
| Gemini 3 | High prosody | after gap | 168 | 53.0 | 92.9 | 51.2 | 41.7 | 1.8 | 5.4 | 14.6 | 96.3 |
| Gemini 3 | High prosody | final | 168 | 57.7 | 87.5 | 54.8 | 32.7 | 3.0 | 9.5 | 27.6 | 93.4 |
| Gemini 3 | Low prosody | pre-gap | 168 | 57.1 | 89.3 | 52.4 | 36.9 | 4.8 | 6.0 | 22.5 | 90.0 |
| Gemini 3 | Low prosody | after gap | 168 | 56.0 | 91.7 | 53.0 | 38.7 | 3.0 | 5.4 | 17.7 | 93.7 |
| Gemini 3 | Low prosody | final | 168 | 57.1 | 86.3 | 54.2 | 32.1 | 3.0 | 10.7 | 29.9 | 93.5 |
| GPT Audio Mini | Ordinary audio | pre-gap | 168 | 18.5 | 89.3 | 17.9 | 71.4 | 0.6 | 10.1 | 13.0 | 99.3 |
| GPT Audio Mini | Ordinary audio | after gap | 168 | 35.1 | 84.5 | 31.0 | 53.6 | 4.2 | 11.3 | 22.4 | 94.0 |
| GPT Audio Mini | Ordinary audio | final | 168 | 36.9 | 80.4 | 30.4 | 50.0 | 6.5 | 13.1 | 28.2 | 90.6 |
| GPT Audio Mini | No state change | pre-gap | 168 | 21.4 | 88.7 | 19.0 | 69.6 | 2.4 | 8.9 | 14.0 | 97.1 |
| GPT Audio Mini | No state change | after gap | 168 | 75.0 | 84.5 | 63.1 | 21.4 | 11.9 | 3.6 | 41.9 | 67.7 |
| GPT Audio Mini | No state change | final | 168 | 64.3 | 83.3 | 55.4 | 28.0 | 8.9 | 7.7 | 37.3 | 80.0 |
| GPT Audio Mini | Short clue | pre-gap | 168 | 15.5 | 95.2 | 15.5 | 79.8 | 0.0 | 4.8 | 5.6 | 100.0 |
| GPT Audio Mini | Short clue | after gap | 168 | 33.3 | 92.3 | 32.7 | 59.5 | 0.6 | 7.1 | 11.5 | 99.1 |
| GPT Audio Mini | Short clue | final | 168 | 30.4 | 87.5 | 27.4 | 60.1 | 3.0 | 9.5 | 17.2 | 95.9 |
| GPT Audio Mini | Clue removed | pre-gap | 168 | 29.8 | 51.2 | 15.5 | 35.7 | 14.3 | 34.5 | 57.7 | 83.1 |
| GPT Audio Mini | Clue removed | after gap | 168 | 40.5 | 46.4 | 17.3 | 29.2 | 23.2 | 30.4 | 64.7 | 71.9 |
| GPT Audio Mini | Clue removed | final | 168 | 39.9 | 48.2 | 20.8 | 27.4 | 19.0 | 32.7 | 65.4 | 75.9 |
| GPT Audio Mini | Neutral audio | pre-gap | 168 | 16.1 | 93.5 | 16.1 | 77.4 | 0.0 | 6.5 | 7.8 | 100.0 |
| GPT Audio Mini | Neutral audio | after gap | 168 | 38.7 | 82.7 | 32.1 | 50.6 | 6.5 | 10.7 | 25.4 | 90.4 |
| GPT Audio Mini | Neutral audio | final | 168 | 39.3 | 85.1 | 33.9 | 51.2 | 5.4 | 9.5 | 22.5 | 91.9 |
| GPT Audio Mini | Explicit user update | pre-gap | 168 | 22.0 | 92.3 | 19.6 | 72.6 | 2.4 | 5.4 | 9.6 | 97.0 |
| GPT Audio Mini | Explicit user update | after gap | 168 | 70.2 | 93.5 | 67.9 | 25.6 | 2.4 | 4.2 | 20.4 | 92.6 |
| GPT Audio Mini | Explicit user update | final | 168 | 69.0 | 89.3 | 61.9 | 27.4 | 7.1 | 3.6 | 28.1 | 81.2 |
| GPT Audio Mini | High prosody | pre-gap | 168 | 22.0 | 91.7 | 19.6 | 72.0 | 2.4 | 6.0 | 10.4 | 97.0 |
| GPT Audio Mini | High prosody | after gap | 168 | 34.5 | 85.1 | 30.4 | 54.8 | 4.2 | 10.7 | 21.4 | 94.0 |
| GPT Audio Mini | High prosody | final | 168 | 31.0 | 83.3 | 25.6 | 57.7 | 5.4 | 11.3 | 22.4 | 92.8 |
| GPT Audio Mini | Low prosody | pre-gap | 168 | 23.8 | 89.9 | 20.8 | 69.0 | 3.0 | 7.1 | 12.8 | 96.2 |
| GPT Audio Mini | Low prosody | after gap | 168 | 43.5 | 89.3 | 40.5 | 48.8 | 3.0 | 7.7 | 18.0 | 95.0 |
| GPT Audio Mini | Low prosody | final | 168 | 35.7 | 85.7 | 32.1 | 53.6 | 3.6 | 10.7 | 21.1 | 94.7 |

## Reading

Under ordinary audio, `causal_alignment` is recovered far more reliably than the outcome: 76.2/90.5/84.5 against 42.3/51.8/35.1. The dominant failure is therefore **alignment right, outcome wrong** (36.9/39.3/53.6 of all trajectories), which means the models generally do resolve which branch they are in and then fail to apply the completion rule to it.

That is a more specific diagnosis than the paper currently offers, and it matters for the framing: the bottleneck under ordinary audio is not clue retrieval, it is rule application to a retrieved clue. The clue-removed condition confirms the split from the other side -- alignment accuracy falls to 51.8/48.2/46.4 there, and with it the outcome.

`outcome only` -- naming the right outcome without resolving the branch -- is rare (3.0/0.6/4.2), as it should be: on this design the outcome is not guessable independently of the branch.
