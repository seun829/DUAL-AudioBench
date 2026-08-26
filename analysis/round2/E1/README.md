# E1. Oracle-state baseline

Scored on `post_gap_success` only. The belief-only checkpoint is suppressed by `elicit_belief=False`, so `belief_reporting_success` is false by construction and `trajectory_success` is not meaningful for this condition.

## Result

| Model | n | Oracle final action | 95% CI | Ordinary audio | Oracle - ordinary | 95% CI | p | Majority baseline | Uniform |
|---|---|---|---|---|---|---|---|---|---|
| Gemini 2.5 | 168 | **47.0** | [35.1, 58.3] | 35.1 | +11.9 | [-0.0, 23.2] | 0.0958 | 51.2 | 20.0 |
| Gemini 3 | 168 | **68.5** | [58.9, 77.4] | 47.0 | +21.4 | [11.9, 30.4] | 0.0022 | 50.6 | 20.0 |
| GPT Audio Mini | 168 | **52.4** | [38.1, 65.5] | 22.0 | +30.4 | [17.9, 44.0] | 0.0005 | 54.8 | 20.0 |

## Split by causal branch

| Model | Oracle misaligned | Oracle aligned | Ordinary misaligned | Ordinary aligned |
|---|---|---|---|---|
| Gemini 2.5 | 50.0 | 44.0 | 50.0 | 20.2 |
| Gemini 3 | 58.3 | 78.6 | 60.7 | 33.3 |
| GPT Audio Mini | 47.6 | 57.1 | 39.3 | 4.8 |

## Reading

Oracle final-action accuracy is 47.0/68.5/52.4 against ordinary audio at 35.1/47.0/22.0, a paired gain of +11.9/+21.4/+30.4 points.

**Mixed, and the paper should report it as mixed.** The paired gains are +11.9/+21.4/+30.4 points and 1 of 3 models clear their majority-class baseline under the oracle. State inference is part of the bottleneck but not all of it: a substantial residual failure remains after the state is handed to the model, which is rule-to-action mapping rather than synchronization.

### Which models clear their floor

| Model | Oracle | 95% CI | Majority-class floor | Clears? |
|---|---|---|---|---|
| Gemini 2.5 | 47.0 | [35.1, 58.3] | 51.2 | inconclusive |
| Gemini 3 | 68.5 | [58.9, 77.4] | 50.6 | **YES** |
| GPT Audio Mini | 52.4 | [38.1, 65.5] | 54.8 | inconclusive |

This is the qualification the paper needs. Supplying the true state produces a large, significant gain for two of three models, so state inference is genuinely a major part of the bottleneck. But **only Gemini 3 exceeds a domain-aware constant policy even with the state handed to it**. For the other two the oracle condition moves them from clearly below the floor to roughly at it. A substantial residual failure therefore survives the removal of all state uncertainty, and that residual is rule-to-action mapping, not synchronization.

### The aligned branch: a state error, not a policy refusal

R2 found that models fail on the aligned branch because they will not conclude that a resolved case is resolved. The oracle condition settles why. Aligned-branch final action moves from 20.2/33.3/4.8 under ordinary audio to 44.0/78.6/57.1 under the oracle. The refusal was a **state error**: once told the operation completed successfully, all three models close the case at a far higher rate. They were not declining to act on a world they understood; they were misreading the world.

The misaligned branch barely moves by comparison (50.0/60.7/39.3 to 50.0/58.3/47.6), which is consistent: that branch was already the one models handled better, and it is the branch where the remaining work is applying the rule rather than reading the state.

## Cost

504 trajectories, 7148 API calls, **$8.97** total (against a $25 cap and a $11 estimate).
