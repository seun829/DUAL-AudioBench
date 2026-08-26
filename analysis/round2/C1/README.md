# C1. Corrected chance baselines in `score.py`

## Change

Added three constant-policy baselines alongside the existing uniform ones, plus a
printed block that shows them, and made majority class the primary plotted
reference line with uniform demoted to secondary.

| New `summarize()` field | Meaning |
|---|---|
| `majority_class_action_chance` | Best constant post-gap action for a policy that knows only the domain |
| `fixed_position_action_chance` | Best single-letter policy |
| `fixed_position_coverage` | Share of rows the fixed-position score could be computed on |
| `majority_class_belief_chance` | Best constant joint belief assignment for a domain-aware policy |

All three are computed from the logs alone. The label-to-action mapping needed by
the fixed-position baseline is harvested from rows where the model selected a
valid option (the row records both the chosen label and the action it resolved to,
and the menu supplies that label's description), so nothing depends on CPython's
RNG staying stable. Coverage was 100% on all 4,368 stored rows, and no
description ever resolved to two different actions.

## Acceptance: the change is additive

Run `python analysis/round2/C1/make_baseline.py before` on the pre-patch tree and
`... after` on the patched tree, then diff.

| Check | Result |
|---|---|
| Pre-existing `summarize()` fields changed | **0** |
| Fields added | 4: `fixed_position_action_chance`, `fixed_position_coverage`, `majority_class_action_chance`, `majority_class_belief_chance` |
| Text lines removed or altered in `condition_table` / `belief_report` / `paired_control_report` / `failure_report` | **0** |
| Text lines added | 6 (the new baseline block) |

The one intentional change to previously emitted output is the plot legend in
`retention_curve`, relabelled from `random action chance` to `uniform action
chance` with a new majority-class line above it. The work order asked for this.

## Why it matters

On the full Gemini 3 dataset the printed block reads:

```
condition                  post  majority action  uniform action  fixed position  majority belief  uniform belief
full_audio                47.0%            48.8%           20.0%           25.2%            47.0%           12.3%
clue_removed              26.8%            54.2%           20.0%           24.4%            44.0%           12.3%
hidden_user_action        79.8%            78.6%           20.0%           24.4%            72.0%           12.3%
```

Ordinary-audio final action (47.0%) sits *below* its majority-class floor
(48.8%), which the uniform 20.0% figure completely hid.
