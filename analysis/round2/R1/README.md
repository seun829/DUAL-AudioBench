# R1. Is the belief metric inflated the same way the action metric was?

## Answer

**Yes. The suspicion in the work order is correct, and the consequence is worse than for the action metric: under ordinary audio, not one of the three models has a post-gap belief accuracy distinguishable from a constant guess.**

The two belief variables are perfectly correlated by construction in the seven ordinary conditions. `causal_alignment` predicts the outcome role in **100.0% of the 84 scenarios**, and the gold joint state takes only **2 distinct values**: `misaligned_terminal + misaligned` on 42 scenarios and `aligned_terminal + aligned` on the other 42. On the gold pre-gap path a single constant guess is therefore jointly correct on **exactly half the set (50.0%)**. Measured against the realized targets actually stored in the trajectories it lands at 41.1-45.8% across models, and a policy that also knows the domain reaches **47.0%**. `score.py` reports chance for the same cell as **12.3%**.

**Ordinary audio: 0 of 3 models clear the corrected baseline.** Below baseline: GPT Audio Mini (31.0 vs 48.2, CI upper 41.1). Interval spans the baseline: Gemini 2.5 (39.3 vs 48.2), Gemini 3 (51.2 vs 47.0). 

**No state change: 3 of 3 models clear it** (Gemini 2.5 60.7 vs 45.2, Gemini 3 78.6 vs 45.2, GPT Audio Mini 63.1 vs 46.4), even though its baseline is comparable at 45.2%. This is the asymmetry the paper needs. The headline belief effect of no-change over ordinary audio is not a case of both conditions sitting above chance with one higher; it is a case of only the no-change condition being above chance at all.

## Reported belief accuracy against the corrected baseline

| Model | Condition | Belief | 95% CI | Uniform (score.py) | Majority class | Margin | Clears? |
|---|---|---|---|---|---|---|---|
| Gemini 2.5 | Ordinary audio | 39.3 | [28.0, 50.6] | 12.3 | 48.2 | -8.9 | inconclusive |
| Gemini 2.5 | No state change | 60.7 | [48.2, 73.2] | 12.3 | 45.2 | +15.5 | **YES** |
| Gemini 2.5 | Short clue | 35.7 | [26.8, 45.8] | 12.3 | 48.2 | -12.5 | **no** |
| Gemini 2.5 | Clue removed | 29.8 | [23.2, 36.3] | 12.3 | 43.5 | -13.7 | **no** |
| Gemini 2.5 | Transcript | 51.8 | [43.5, 59.5] | 12.3 | 48.2 | +3.6 | inconclusive |
| Gemini 2.5 | Neutral audio | 32.7 | [24.4, 41.1] | 12.3 | 44.0 | -11.3 | **no** |
| Gemini 2.5 | Explicit user update | 72.6 | [61.9, 83.3] | 12.3 | 69.6 | +3.0 | inconclusive |
| Gemini 2.5 | High prosody | 37.5 | [29.2, 46.4] | 12.3 | 44.0 | -6.5 | inconclusive |
| Gemini 2.5 | Low prosody | 35.7 | [28.6, 42.9] | 12.3 | 46.4 | -10.7 | **no** |
| Gemini 3 | Ordinary audio | 51.2 | [43.5, 57.7] | 12.3 | 47.0 | +4.2 | inconclusive |
| Gemini 3 | No state change | 78.6 | [69.0, 87.5] | 12.3 | 45.2 | +33.3 | **YES** |
| Gemini 3 | Short clue | 50.6 | [45.8, 56.0] | 12.3 | 47.0 | +3.6 | inconclusive |
| Gemini 3 | Clue removed | 32.1 | [22.0, 41.7] | 12.3 | 44.0 | -11.9 | **no** |
| Gemini 3 | Transcript | 64.3 | [55.4, 73.8] | 12.3 | 48.8 | +15.5 | **YES** |
| Gemini 3 | Neutral audio | 54.2 | [47.6, 60.7] | 12.3 | 48.2 | +6.0 | inconclusive |
| Gemini 3 | Explicit user update | 85.1 | [71.4, 95.8] | 12.3 | 72.0 | +13.1 | inconclusive |
| Gemini 3 | High prosody | 51.2 | [44.0, 58.9] | 12.3 | 47.0 | +4.2 | inconclusive |
| Gemini 3 | Low prosody | 53.0 | [43.5, 63.1] | 12.3 | 47.6 | +5.4 | inconclusive |
| GPT Audio Mini | Ordinary audio | 31.0 | [21.4, 41.1] | 12.3 | 48.2 | -17.3 | **no** |
| GPT Audio Mini | No state change | 63.1 | [49.4, 76.2] | 12.3 | 46.4 | +16.7 | **YES** |
| GPT Audio Mini | Short clue | 32.7 | [25.6, 41.7] | 12.3 | 47.6 | -14.9 | **no** |
| GPT Audio Mini | Clue removed | 17.3 | [10.1, 25.0] | 12.3 | 41.7 | -24.4 | **no** |
| GPT Audio Mini | Neutral audio | 32.1 | [21.4, 43.5] | 12.3 | 45.8 | -13.7 | **no** |
| GPT Audio Mini | Explicit user update | 67.9 | [50.6, 82.1] | 12.3 | 69.6 | -1.8 | inconclusive |
| GPT Audio Mini | High prosody | 30.4 | [20.8, 39.3] | 12.3 | 44.6 | -14.3 | **no** |
| GPT Audio Mini | Low prosody | 40.5 | [30.4, 51.2] | 12.3 | 44.6 | -4.2 | inconclusive |

## 1. Joint distribution of true post-gap belief values (gold path, n=84)

Outcome values are shown as data-derived roles so the 14 domains are comparable: `misaligned_terminal` is whatever the gold outcome value is on the b0 branch under ordinary audio, `aligned_terminal` the b1 value, `in_progress` the value under no-state-change.

| Condition | aligned_terminal + aligned | aligned_terminal + misaligned | in_progress + aligned | in_progress + misaligned | misaligned_terminal + misaligned | not_started + aligned | not_started + misaligned | majority class % |
|---|---|---|---|---|---|---|---|---|
| Ordinary audio | 42 | 0 | 0 | 0 | 42 | 0 | 0 | 50.0 |
| No state change | 3 | 3 | 39 | 39 | 0 | 0 | 0 | 46.4 |
| Short clue | 42 | 0 | 0 | 0 | 42 | 0 | 0 | 50.0 |
| Clue removed | 42 | 0 | 0 | 0 | 42 | 0 | 0 | 50.0 |
| Transcript | 42 | 0 | 0 | 0 | 42 | 0 | 0 | 50.0 |
| Neutral audio | 42 | 0 | 0 | 0 | 42 | 0 | 0 | 50.0 |
| Explicit user update | 72 | 0 | 0 | 0 | 0 | 6 | 6 | 85.7 |
| High prosody | 42 | 0 | 0 | 0 | 42 | 0 | 0 | 50.0 |
| Low prosody | 42 | 0 | 0 | 0 | 42 | 0 | 0 | 50.0 |

## 2 + 3. Constant-policy baselines (realized targets)

| Model | Condition | Majority joint (domain-conditional) | Majority outcome only | Majority alignment only | Global constant joint | Best single guess |
|---|---|---|---|---|---|---|
| Gemini 2.5 | Ordinary audio | 48.2 | 53.0 | 50.0 | 41.1 | aligned_terminal + aligned |
| Gemini 2.5 | No state change | 45.2 | 76.2 | 50.0 | 38.1 | in_progress + aligned |
| Gemini 2.5 | Short clue | 48.2 | 53.0 | 50.0 | 41.1 | aligned_terminal + aligned |
| Gemini 2.5 | Clue removed | 43.5 | 56.5 | 50.0 | 32.1 | aligned_terminal + aligned |
| Gemini 2.5 | Transcript | 48.2 | 52.4 | 50.0 | 44.0 | aligned_terminal + aligned |
| Gemini 2.5 | Neutral audio | 44.0 | 49.4 | 50.0 | 38.1 | aligned_terminal + aligned |
| Gemini 2.5 | Explicit user update | 69.6 | 75.0 | 92.9 | 54.8 | aligned_terminal + aligned |
| Gemini 2.5 | High prosody | 44.0 | 48.2 | 50.0 | 36.9 | aligned_terminal + aligned |
| Gemini 2.5 | Low prosody | 46.4 | 54.8 | 50.0 | 38.7 | aligned_terminal + aligned |
| Gemini 3 | Ordinary audio | 47.0 | 48.8 | 50.0 | 45.8 | aligned_terminal + aligned |
| Gemini 3 | No state change | 45.2 | 79.2 | 50.0 | 39.9 | in_progress + aligned |
| Gemini 3 | Short clue | 47.0 | 51.2 | 50.0 | 43.5 | aligned_terminal + aligned |
| Gemini 3 | Clue removed | 44.0 | 54.2 | 50.0 | 33.9 | aligned_terminal + aligned |
| Gemini 3 | Transcript | 48.8 | 50.6 | 50.0 | 47.6 | aligned_terminal + aligned |
| Gemini 3 | Neutral audio | 48.2 | 50.0 | 50.0 | 47.0 | aligned_terminal + aligned |
| Gemini 3 | Explicit user update | 72.0 | 78.6 | 92.9 | 61.3 | aligned_terminal + aligned |
| Gemini 3 | High prosody | 47.0 | 48.8 | 50.0 | 44.6 | aligned_terminal + aligned |
| Gemini 3 | Low prosody | 47.6 | 52.4 | 50.0 | 43.5 | aligned_terminal + aligned |
| GPT Audio Mini | Ordinary audio | 48.2 | 53.0 | 50.0 | 44.0 | aligned_terminal + aligned |
| GPT Audio Mini | No state change | 46.4 | 75.6 | 50.0 | 34.5 | in_progress + aligned |
| GPT Audio Mini | Short clue | 47.6 | 50.0 | 50.0 | 45.8 | aligned_terminal + aligned |
| GPT Audio Mini | Clue removed | 41.7 | 57.1 | 50.0 | 28.0 | misaligned_terminal + misaligned |
| GPT Audio Mini | Neutral audio | 45.8 | 52.4 | 50.0 | 41.1 | aligned_terminal + aligned |
| GPT Audio Mini | Explicit user update | 69.6 | 75.6 | 92.9 | 56.5 | aligned_terminal + aligned |
| GPT Audio Mini | High prosody | 44.6 | 52.4 | 50.0 | 39.9 | aligned_terminal + aligned |
| GPT Audio Mini | Low prosody | 44.6 | 52.4 | 50.0 | 38.7 | aligned_terminal + aligned |

## 4. Correlation between the two belief variables (gold path)

| Condition | n | distinct joint cells | outcome predictable from alignment alone (%) | best outcome per alignment value |
|---|---|---|---|---|
| Ordinary audio | 84 | 2 | 100.0 | aligned->aligned_terminal (42/42); misaligned->misaligned_terminal (42/42) |
| No state change | 84 | 4 | 92.9 | aligned->in_progress (39/42); misaligned->in_progress (39/42) |
| Short clue | 84 | 2 | 100.0 | aligned->aligned_terminal (42/42); misaligned->misaligned_terminal (42/42) |
| Clue removed | 84 | 2 | 100.0 | aligned->aligned_terminal (42/42); misaligned->misaligned_terminal (42/42) |
| Transcript | 84 | 2 | 100.0 | aligned->aligned_terminal (42/42); misaligned->misaligned_terminal (42/42) |
| Neutral audio | 84 | 2 | 100.0 | aligned->aligned_terminal (42/42); misaligned->misaligned_terminal (42/42) |
| Explicit user update | 84 | 3 | 92.9 | aligned->aligned_terminal (72/78); misaligned->not_started (6/6) |
| High prosody | 84 | 2 | 100.0 | aligned->aligned_terminal (42/42); misaligned->misaligned_terminal (42/42) |
| Low prosody | 84 | 2 | 100.0 | aligned->aligned_terminal (42/42); misaligned->misaligned_terminal (42/42) |

## Reading

The belief metric and the action metric are inflated by the *same* structural fact, reached by different routes. The action metric collapses because `close_case` is gold on both branches for half the set. The belief metric collapses because the gold joint state takes only two values across the whole 84, one per branch, in equal numbers. Either way a constant answer scores about half, and either way the code reports a uniform figure (12.3% for belief, 20% for action) that is roughly four times too generous.

Two caveats worth carrying into the paper. First, the baselines here are computed against the *realized* belief targets stored in each trajectory, which is why the domain-conditional majority sits at 47.0% rather than exactly 50%: when a model picks the wrong pre-gap action the realized state differs, spreading the targets slightly. Second, the domain-conditional baseline is the fair one to quote, because every model is told the domain in the conversation; the role-abstracted figure is the weaker claim.

`clue_removed` is the one cell where a model is reliably and substantially *below* a constant guess (GPT Audio Mini 17.3 against 41.7). Ablating the clue does not push models toward the majority state; it pushes them somewhere worse than guessing.
