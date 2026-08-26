# R3. Branch-pair accuracy, all models, all conditions

A pair scores 1 only if the model chose correctly on **both** branches within the **same pass**. A constant policy scores exactly 0 because the two branches have different gold answers; uniform random scores 1/25 = 4.0% for actions. This metric was therefore never affected by the answer skew, which is why it is the natural headline.

## Pooled over both passes (n=84 pair-passes per cell)

| Model | Condition | n | Both actions | 95% CI | Both beliefs | 95% CI | Both + both |
|---|---|---|---|---|---|---|---|
| Gemini 2.5 | Ordinary audio | 84 | 11.9 | [7.1, 16.7] | 16.7 | [9.5, 25.0] | 4.8 |
| Gemini 2.5 | No state change | 84 | 17.9 | [8.3, 27.4] | 39.3 | [23.8, 56.0] | 6.0 |
| Gemini 2.5 | Short clue | 84 | 15.5 | [9.5, 21.4] | 9.5 | [1.2, 20.2] | 0.0 |
| Gemini 2.5 | Clue removed | 84 | 1.2 | [0.0, 3.6] | 2.4 | [0.0, 6.0] | 0.0 |
| Gemini 2.5 | Transcript | 84 | 8.3 | [1.2, 16.7] | 20.2 | [11.9, 29.8] | 3.6 |
| Gemini 2.5 | Neutral audio | 84 | 6.0 | [2.4, 10.7] | 7.1 | [2.4, 13.1] | 2.4 |
| Gemini 2.5 | Explicit user update | 84 | 57.1 | [40.5, 71.4] | 54.8 | [38.1, 71.4] | 39.3 |
| Gemini 2.5 | High prosody | 84 | 8.3 | [2.4, 16.7] | 9.5 | [2.4, 16.7] | 0.0 |
| Gemini 2.5 | Low prosody | 84 | 6.0 | [1.2, 11.9] | 9.5 | [3.6, 16.7] | 1.2 |
| Gemini 3 | Ordinary audio | 84 | 16.7 | [6.0, 28.6] | 23.8 | [13.1, 34.5] | 10.7 |
| Gemini 3 | No state change | 84 | 15.5 | [7.1, 25.0] | 60.7 | [44.0, 76.2] | 7.1 |
| Gemini 3 | Short clue | 84 | 15.5 | [7.1, 23.8] | 19.0 | [11.9, 26.2] | 4.8 |
| Gemini 3 | Clue removed | 84 | 3.6 | [0.0, 9.5] | 8.3 | [3.6, 14.3] | 1.2 |
| Gemini 3 | Transcript | 84 | 32.1 | [15.5, 48.8] | 32.1 | [15.5, 50.0] | 16.7 |
| Gemini 3 | Neutral audio | 84 | 17.9 | [8.3, 27.4] | 27.4 | [16.7, 38.1] | 8.3 |
| Gemini 3 | Explicit user update | 84 | 69.0 | [52.4, 84.5] | 76.2 | [58.3, 91.7] | 60.7 |
| Gemini 3 | High prosody | 84 | 13.1 | [7.1, 20.2] | 27.4 | [16.7, 39.3] | 8.3 |
| Gemini 3 | Low prosody | 84 | 11.9 | [3.6, 22.6] | 26.2 | [14.3, 40.5] | 6.0 |
| GPT Audio Mini | Ordinary audio | 84 | 1.2 | [0.0, 3.6] | 4.8 | [0.0, 13.1] | 0.0 |
| GPT Audio Mini | No state change | 84 | 8.3 | [2.4, 15.5] | 41.7 | [26.2, 58.3] | 1.2 |
| GPT Audio Mini | Short clue | 84 | 1.2 | [0.0, 3.6] | 11.9 | [4.8, 20.2] | 0.0 |
| GPT Audio Mini | Clue removed | 84 | 0.0 | [0.0, 0.0] | 3.6 | [0.0, 9.5] | 0.0 |
| GPT Audio Mini | Neutral audio | 84 | 1.2 | [0.0, 3.6] | 11.9 | [2.4, 23.8] | 0.0 |
| GPT Audio Mini | Explicit user update | 84 | 44.0 | [31.0, 57.1] | 54.8 | [38.1, 70.2] | 39.3 |
| GPT Audio Mini | High prosody | 84 | 0.0 | [0.0, 0.0] | 10.7 | [3.6, 19.0] | 0.0 |
| GPT Audio Mini | Low prosody | 84 | 1.2 | [0.0, 3.6] | 17.9 | [8.3, 28.6] | 0.0 |

## Per pass

| Model | Condition | Pass | n | Both actions | Both beliefs | Both + both |
|---|---|---|---|---|---|---|
| Gemini 2.5 | Ordinary audio | seed=0 | 42 | 9.5 | 9.5 | 4.8 |
| Gemini 2.5 | Ordinary audio | seed=1 | 42 | 14.3 | 23.8 | 4.8 |
| Gemini 2.5 | No state change | seed=0 | 42 | 11.9 | 42.9 | 4.8 |
| Gemini 2.5 | No state change | seed=1 | 42 | 23.8 | 35.7 | 7.1 |
| Gemini 2.5 | Short clue | seed=0 | 42 | 11.9 | 4.8 | 0.0 |
| Gemini 2.5 | Short clue | seed=1 | 42 | 19.0 | 14.3 | 0.0 |
| Gemini 2.5 | Clue removed | seed=0 | 42 | 2.4 | 2.4 | 0.0 |
| Gemini 2.5 | Clue removed | seed=1 | 42 | 0.0 | 2.4 | 0.0 |
| Gemini 2.5 | Transcript | seed=0 | 42 | 7.1 | 19.0 | 4.8 |
| Gemini 2.5 | Transcript | seed=1 | 42 | 9.5 | 21.4 | 2.4 |
| Gemini 2.5 | Neutral audio | seed=0 | 42 | 7.1 | 9.5 | 2.4 |
| Gemini 2.5 | Neutral audio | seed=1 | 42 | 4.8 | 4.8 | 2.4 |
| Gemini 2.5 | Explicit user update | seed=0 | 42 | 52.4 | 57.1 | 40.5 |
| Gemini 2.5 | Explicit user update | seed=1 | 42 | 61.9 | 52.4 | 38.1 |
| Gemini 2.5 | High prosody | seed=0 | 42 | 11.9 | 14.3 | 0.0 |
| Gemini 2.5 | High prosody | seed=1 | 42 | 4.8 | 4.8 | 0.0 |
| Gemini 2.5 | Low prosody | seed=0 | 42 | 9.5 | 9.5 | 2.4 |
| Gemini 2.5 | Low prosody | seed=1 | 42 | 2.4 | 9.5 | 0.0 |
| Gemini 3 | Ordinary audio | seed=0 | 42 | 21.4 | 31.0 | 16.7 |
| Gemini 3 | Ordinary audio | seed=1 | 42 | 11.9 | 16.7 | 4.8 |
| Gemini 3 | No state change | seed=0 | 42 | 16.7 | 59.5 | 9.5 |
| Gemini 3 | No state change | seed=1 | 42 | 14.3 | 61.9 | 4.8 |
| Gemini 3 | Short clue | seed=0 | 42 | 14.3 | 14.3 | 2.4 |
| Gemini 3 | Short clue | seed=1 | 42 | 16.7 | 23.8 | 7.1 |
| Gemini 3 | Clue removed | seed=0 | 42 | 7.1 | 9.5 | 2.4 |
| Gemini 3 | Clue removed | seed=1 | 42 | 0.0 | 7.1 | 0.0 |
| Gemini 3 | Transcript | seed=0 | 42 | 31.0 | 28.6 | 16.7 |
| Gemini 3 | Transcript | seed=1 | 42 | 33.3 | 35.7 | 16.7 |
| Gemini 3 | Neutral audio | seed=0 | 42 | 21.4 | 23.8 | 11.9 |
| Gemini 3 | Neutral audio | seed=1 | 42 | 14.3 | 31.0 | 4.8 |
| Gemini 3 | Explicit user update | seed=0 | 42 | 66.7 | 76.2 | 59.5 |
| Gemini 3 | Explicit user update | seed=1 | 42 | 71.4 | 76.2 | 61.9 |
| Gemini 3 | High prosody | seed=0 | 42 | 16.7 | 28.6 | 11.9 |
| Gemini 3 | High prosody | seed=1 | 42 | 9.5 | 26.2 | 4.8 |
| Gemini 3 | Low prosody | seed=0 | 42 | 9.5 | 28.6 | 7.1 |
| Gemini 3 | Low prosody | seed=1 | 42 | 14.3 | 23.8 | 4.8 |
| GPT Audio Mini | Ordinary audio | seed=0 | 42 | 2.4 | 4.8 | 0.0 |
| GPT Audio Mini | Ordinary audio | seed=1 | 42 | 0.0 | 4.8 | 0.0 |
| GPT Audio Mini | No state change | seed=0 | 42 | 11.9 | 31.0 | 0.0 |
| GPT Audio Mini | No state change | seed=1 | 42 | 4.8 | 52.4 | 2.4 |
| GPT Audio Mini | Short clue | seed=0 | 42 | 0.0 | 7.1 | 0.0 |
| GPT Audio Mini | Short clue | seed=1 | 42 | 2.4 | 16.7 | 0.0 |
| GPT Audio Mini | Clue removed | seed=0 | 42 | 0.0 | 2.4 | 0.0 |
| GPT Audio Mini | Clue removed | seed=1 | 42 | 0.0 | 4.8 | 0.0 |
| GPT Audio Mini | Neutral audio | seed=0 | 42 | 0.0 | 7.1 | 0.0 |
| GPT Audio Mini | Neutral audio | seed=1 | 42 | 2.4 | 16.7 | 0.0 |
| GPT Audio Mini | Explicit user update | seed=0 | 42 | 42.9 | 59.5 | 40.5 |
| GPT Audio Mini | Explicit user update | seed=1 | 42 | 45.2 | 50.0 | 38.1 |
| GPT Audio Mini | High prosody | seed=0 | 42 | 0.0 | 9.5 | 0.0 |
| GPT Audio Mini | High prosody | seed=1 | 42 | 0.0 | 11.9 | 0.0 |
| GPT Audio Mini | Low prosody | seed=0 | 42 | 2.4 | 16.7 | 0.0 |
| GPT Audio Mini | Low prosody | seed=1 | 42 | 0.0 | 19.0 | 0.0 |

## Comparison with the paper

The paper reports pair accuracy only for the two Gemini models on clue-present and clue-removed: Gemini 2.5 11.9 / 1.2 and Gemini 3 16.7 / 3.6. Recomputed here:

| Model | Condition | Both actions (recomputed) | Paper | Match? |
|---|---|---|---|---|
| Gemini 2.5 | Ordinary audio | 11.9 | 11.9 | yes |
| Gemini 2.5 | Clue removed | 1.2 | 1.2 | yes |
| Gemini 3 | Ordinary audio | 16.7 | 16.7 | yes |
| Gemini 3 | Clue removed | 3.6 | 3.6 | yes |

**GPT Audio Mini, missing from the paper entirely:**

| Condition | Both actions | 95% CI | Both beliefs | Both + both |
|---|---|---|---|---|
| Ordinary audio | 1.2 | [0.0, 3.6] | 4.8 | 0.0 |
| No state change | 8.3 | [2.4, 15.5] | 41.7 | 1.2 |
| Short clue | 1.2 | [0.0, 3.6] | 11.9 | 0.0 |
| Clue removed | 0.0 | [0.0, 0.0] | 3.6 | 0.0 |
| Neutral audio | 1.2 | [0.0, 3.6] | 11.9 | 0.0 |
| Explicit user update | 44.0 | [31.0, 57.1] | 54.8 | 39.3 |
| High prosody | 0.0 | [0.0, 0.0] | 10.7 | 0.0 |
| Low prosody | 1.2 | [0.0, 3.6] | 17.9 | 0.0 |

## Reading

Under ordinary audio, both-action pair accuracy is Gemini 2.5 11.9, Gemini 3 16.7, GPT Audio Mini 1.2 against a 4.0% uniform baseline and a 0.0% constant-policy baseline. All three are above uniform, but the absolute numbers are low: the best model gets both branches of the same pair right in fewer than one case in five.

Both-belief pair accuracy is much lower still (16.7, 23.8, 4.8), and the conjunction of all four correct answers is 4.8, 10.7, 0.0. This is the cleanest statement of the benchmark's difficulty available anywhere in the data, and unlike the pooled single-branch numbers it needs no baseline caveat.

Note that both-belief pair accuracy is the metric R1's baseline problem does *not* touch: a constant belief guess scores 0 here for the same reason a constant action does. Where R1 found that no model's single-branch belief accuracy is distinguishable from a constant guess, the pair version shows the models are nonetheless doing something better than constant -- just not much better.
