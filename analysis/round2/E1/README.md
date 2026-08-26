# E1. Oracle-state baseline

**Partial run.** GPT Audio Mini n=39. Figures below are computed on what completed; a full cell is n=168 (84 scenarios x 2 passes) per model.

Scored on `post_gap_success` only. The belief-only checkpoint is suppressed by `elicit_belief=False`, so `belief_reporting_success` is false by construction and `trajectory_success` is not meaningful for this condition.

## Result

| Model | n | Oracle final action | 95% CI | Ordinary audio | Oracle - ordinary | 95% CI | p | Majority baseline | Uniform |
|---|---|---|---|---|---|---|---|---|---|
| GPT Audio Mini | 39 | **48.7** | [8.3, 70.8] | 22.0 | +22.9 | [4.2, 52.1] | 0.2500 | 53.8 | 20.0 |

## Split by causal branch

| Model | Oracle misaligned | Oracle aligned | Ordinary misaligned | Ordinary aligned |
|---|---|---|---|---|
| GPT Audio Mini | 30.0 | 68.4 | 39.3 | 4.8 |

## Reading

Oracle final-action accuracy is 48.7 against ordinary audio at 22.0, a paired gain of +22.9 points.

**Mixed, and the paper should report it as mixed.** The paired gains are +22.9 points and 0 of 1 models clear their majority-class baseline under the oracle. State inference is part of the bottleneck but not all of it: a substantial residual failure remains after the state is handed to the model, which is rule-to-action mapping rather than synchronization.

The branch split is the sharper diagnostic. Under ordinary audio the aligned branch is where models fail (they refuse to close a resolved case, R2); the oracle condition tells us whether that refusal is a state error or a policy preference. Compare the aligned columns above: if aligned accuracy stays low with the state supplied, the models are not misreading the world, they are declining to act on it.

## Cost

39 trajectories, 546 API calls, **$0.23** total (against a $25 cap and a $11 estimate).
