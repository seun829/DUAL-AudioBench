# R8. Fixed-position and seed-variance baselines

## Part 1. Fixed-position policy at the post-gap checkpoint

Score of a policy that always answers the same letter. Computed from the menu **as logged in each trajectory**, joined to internal action names by option description, so no dependence on the RNG. The join was verified against `post_gap_action_label` -> `post_gap_action` on all 4368 rows.

| Model | Condition | n | Observed | Always A | Always B | Always C | Always D | Always E | Best fixed | Label | Uniform |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Gemini 2.5 | Ordinary audio | 168 | 35.1 | 19.6 | 19.6 | 19.6 | 21.4 | 19.6 | 21.4 | D | 20.0 |
| Gemini 2.5 | No state change | 168 | 38.7 | 14.3 | 32.1 | 12.5 | 20.8 | 20.2 | 32.1 | B | 20.0 |
| Gemini 2.5 | Short clue | 168 | 35.7 | 19.6 | 17.9 | 22.0 | 20.2 | 20.2 | 22.0 | C | 20.0 |
| Gemini 2.5 | Clue removed | 168 | 25.0 | 22.0 | 19.6 | 18.5 | 20.2 | 19.6 | 22.0 | A | 20.0 |
| Gemini 2.5 | Transcript | 168 | 35.7 | 21.4 | 19.6 | 20.8 | 17.9 | 20.2 | 21.4 | A | 20.0 |
| Gemini 2.5 | Neutral audio | 168 | 31.5 | 25.0 | 19.0 | 17.9 | 18.5 | 19.6 | 25.0 | A | 20.0 |
| Gemini 2.5 | Explicit user update | 168 | 72.0 | 22.6 | 16.1 | 17.9 | 21.4 | 22.0 | 22.6 | A | 20.0 |
| Gemini 2.5 | High prosody | 168 | 36.9 | 22.0 | 20.2 | 22.6 | 17.3 | 17.9 | 22.6 | C | 20.0 |
| Gemini 2.5 | Low prosody | 168 | 32.1 | 20.8 | 19.6 | 20.2 | 19.6 | 19.6 | 20.8 | A | 20.0 |
| Gemini 3 | Ordinary audio | 168 | 47.0 | 25.0 | 16.1 | 17.9 | 18.5 | 22.6 | 25.0 | A | 20.0 |
| Gemini 3 | No state change | 168 | 48.2 | 14.9 | 28.0 | 16.1 | 16.7 | 24.4 | 28.0 | B | 20.0 |
| Gemini 3 | Short clue | 168 | 42.3 | 24.4 | 17.3 | 17.9 | 19.6 | 20.8 | 24.4 | A | 20.0 |
| Gemini 3 | Clue removed | 168 | 26.8 | 23.8 | 19.6 | 16.7 | 17.9 | 22.0 | 23.8 | A | 20.0 |
| Gemini 3 | Transcript | 168 | 58.3 | 19.6 | 19.0 | 18.5 | 22.6 | 20.2 | 22.6 | D | 20.0 |
| Gemini 3 | Neutral audio | 168 | 45.2 | 21.4 | 14.9 | 19.0 | 22.6 | 22.0 | 22.6 | D | 20.0 |
| Gemini 3 | Explicit user update | 168 | 79.8 | 22.6 | 13.1 | 17.3 | 24.4 | 22.6 | 24.4 | D | 20.0 |
| Gemini 3 | High prosody | 168 | 44.6 | 23.2 | 17.9 | 19.0 | 19.6 | 20.2 | 23.2 | A | 20.0 |
| Gemini 3 | Low prosody | 168 | 40.5 | 22.0 | 18.5 | 19.6 | 19.6 | 20.2 | 22.0 | A | 20.0 |
| GPT Audio Mini | Ordinary audio | 168 | 22.0 | 23.2 | 17.9 | 20.8 | 20.2 | 17.9 | 23.2 | A | 20.0 |
| GPT Audio Mini | No state change | 168 | 21.4 | 17.3 | 23.2 | 15.5 | 23.2 | 20.8 | 23.2 | B | 20.0 |
| GPT Audio Mini | Short clue | 168 | 20.8 | 21.4 | 18.5 | 20.2 | 21.4 | 18.5 | 21.4 | A | 20.0 |
| GPT Audio Mini | Clue removed | 168 | 26.8 | 22.0 | 18.5 | 20.8 | 19.0 | 19.6 | 22.0 | A | 20.0 |
| GPT Audio Mini | Neutral audio | 168 | 19.0 | 22.6 | 17.3 | 19.6 | 19.6 | 20.8 | 22.6 | A | 20.0 |
| GPT Audio Mini | Explicit user update | 168 | 63.1 | 20.2 | 17.3 | 18.5 | 22.0 | 22.0 | 22.0 | D | 20.0 |
| GPT Audio Mini | High prosody | 168 | 19.6 | 18.5 | 22.0 | 19.6 | 21.4 | 18.5 | 22.0 | B | 20.0 |
| GPT Audio Mini | Low prosody | 168 | 20.2 | 19.0 | 16.1 | 23.2 | 22.0 | 19.6 | 23.2 | C | 20.0 |

**The shuffle is working.** The mean of all 130 fixed-position rates is 19.99%, against a 20.0% uniform expectation. The maximum is 32.1%, but that is the largest of 130 draws, so it is upward-biased by selection; the range is 12.5-32.1%. No letter is systematically the answer, and none of the reported accuracies can be explained by position bias in the gold.

**But 6 cells score below their own best fixed-position policy**, and all of them are GPT Audio Mini:

| Model | Condition | Observed final action | Best fixed position | Label |
|---|---|---|---|---|
| GPT Audio Mini | Ordinary audio | 22.0 | 23.2 | A |
| GPT Audio Mini | No state change | 21.4 | 23.2 | B |
| GPT Audio Mini | Short clue | 20.8 | 21.4 | A |
| GPT Audio Mini | Neutral audio | 19.0 | 22.6 | A |
| GPT Audio Mini | High prosody | 19.6 | 22.0 | B |
| GPT Audio Mini | Low prosody | 20.2 | 23.2 | C |

On 6 of its 8 conditions, GPT Audio Mini's final-action accuracy is at or below the score obtainable by pressing one fixed letter for the whole benchmark. The two exceptions are `clue_removed` (26.8 against 22.0) and `hidden_user_action` (63.1 against 22.0). This is a stronger and simpler statement than the majority-class comparison, and it belongs in the paper: for that model, on the ordinary audio condition, the post-gap action measurement carries no signal.

## Part 2. Seed variance

| Model | Condition | Scenarios | Final-action flips | % | Belief flips | % | Chosen-action changes | % |
|---|---|---|---|---|---|---|---|---|
| Gemini 2.5 | Ordinary audio | 84 | 29 | 34.5 | 34 | 40.5 | 44 | 52.4 |
| Gemini 2.5 | No state change | 84 | 27 | 32.1 | 22 | 26.2 | 45 | 53.6 |
| Gemini 2.5 | Short clue | 84 | 36 | 42.9 | 26 | 31.0 | 50 | 59.5 |
| Gemini 2.5 | Clue removed | 84 | 24 | 28.6 | 16 | 19.0 | 47 | 56.0 |
| Gemini 2.5 | Transcript | 84 | 16 | 19.0 | 31 | 36.9 | 24 | 28.6 |
| Gemini 2.5 | Neutral audio | 84 | 27 | 32.1 | 25 | 29.8 | 37 | 44.0 |
| Gemini 2.5 | Explicit user update | 84 | 27 | 32.1 | 26 | 31.0 | 33 | 39.3 |
| Gemini 2.5 | High prosody | 84 | 26 | 31.0 | 29 | 34.5 | 42 | 50.0 |
| Gemini 2.5 | Low prosody | 84 | 24 | 28.6 | 36 | 42.9 | 44 | 52.4 |
| Gemini 3 | Ordinary audio | 84 | 29 | 34.5 | 30 | 35.7 | 34 | 40.5 |
| Gemini 3 | No state change | 84 | 23 | 27.4 | 16 | 19.0 | 26 | 31.0 |
| Gemini 3 | Short clue | 84 | 31 | 36.9 | 31 | 36.9 | 30 | 35.7 |
| Gemini 3 | Clue removed | 84 | 17 | 20.2 | 20 | 23.8 | 36 | 42.9 |
| Gemini 3 | Transcript | 84 | 16 | 19.0 | 12 | 14.3 | 14 | 16.7 |
| Gemini 3 | Neutral audio | 84 | 40 | 47.6 | 37 | 44.0 | 37 | 44.0 |
| Gemini 3 | Explicit user update | 84 | 22 | 26.2 | 15 | 17.9 | 34 | 40.5 |
| Gemini 3 | High prosody | 84 | 35 | 41.7 | 34 | 40.5 | 32 | 38.1 |
| Gemini 3 | Low prosody | 84 | 24 | 28.6 | 25 | 29.8 | 32 | 38.1 |
| GPT Audio Mini | Ordinary audio | 84 | 19 | 22.6 | 26 | 31.0 | 29 | 34.5 |
| GPT Audio Mini | No state change | 84 | 28 | 33.3 | 26 | 31.0 | 43 | 51.2 |
| GPT Audio Mini | Short clue | 84 | 19 | 22.6 | 29 | 34.5 | 37 | 44.0 |
| GPT Audio Mini | Clue removed | 84 | 19 | 22.6 | 19 | 22.6 | 27 | 32.1 |
| GPT Audio Mini | Neutral audio | 84 | 14 | 16.7 | 32 | 38.1 | 31 | 36.9 |
| GPT Audio Mini | Explicit user update | 84 | 24 | 28.6 | 20 | 23.8 | 31 | 36.9 |
| GPT Audio Mini | High prosody | 84 | 19 | 22.6 | 35 | 41.7 | 32 | 38.1 |
| GPT Audio Mini | Low prosody | 84 | 16 | 19.0 | 28 | 33.3 | 30 | 35.7 |

## Reading

Fixed position is a non-issue as a *confound* -- the shuffle is uniform to within 0.01 points on average -- but it is a useful *yardstick*, and by that yardstick GPT Audio Mini fails on 6 of 8 conditions (table above).

**Seed variance is substantial and the paper should say so.** Across the 26 cells, the two passes disagree on whether the final action was correct in 28.9% of scenarios on average (worst cell Gemini 3 Neutral audio at 47.6%), and on belief correctness in 31.1%. The *chosen action* changes between passes in 41.3% of scenarios.

With two passes, a per-scenario accuracy is one of {0, 50, 100}, and a third of scenarios landing on 50 means the per-cell point estimate carries real sampling noise beyond what the domain-clustered interval captures -- the clustering handles between-domain variation, not between-pass variation. Two consequences worth stating in the limitations paragraph: the paired effects in the main text are on the optimistic side of their true width, and any effect smaller than roughly 10 points should not be read as established from 2 passes. The effects the paper actually leans on (no-change belief +21 to +32, user-update belief +33 to +37) are far outside that band, so the headline claims are unaffected.
