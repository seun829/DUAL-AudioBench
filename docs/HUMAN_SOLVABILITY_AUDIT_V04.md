# Human-solvability audit for schema v0.4

## Status

This is a structural expert audit, not an empirical human baseline. It checks
whether every gold decision follows from information visible to a careful
reader/listener and whether the public labels have operational meanings. Human
participants have not yet been tested.

## Finding

All 14 domain templates are solvable in principle. Every gold path provides:

1. an explicit problem and an early clue;
2. five distinct public actions, including one state-appropriate action;
3. a deterministic elapsed-time transition;
4. a resumed observation that directly describes the resulting outcome; and
5. operational definitions for every allowed belief value.

The previous human-solvability concern was chiefly that labels such as
`missed`, `protected`, and `viable` were presented without meanings. Schema
v0.4 now shows those meanings in both belief prompts. Gold action and state
contracts are covered by `tests/test_v04_quality.py`.

| Domain | Correct pre-gap step | Explicit resumed state | Correct post-gap step |
|---|---|---|---|
| Banking | File dispute | Details returned unmatched | Reconcile card records |
| Scheduling | Request authorization | Authorization declined | Obtain qualifying referral |
| Education | Submit enrolment | Held for review | Request prior-study assessment |
| Logistics | Schedule redelivery | Returned to sender | Correct destination record |
| Travel | Enable monitoring | Connection missed | Protect onward segment |
| Motor insurance | Lodge claim | Held for proof | Align policy records |
| Permits | Submit application | Refused | Supply alternative proof |
| Pharmacy | Submit claim | Rejected | Review account configuration |
| Tech support | Run maintenance | Firmware stuck | Inspect persistent state |
| Account access | Initiate reset | Still locked | Engage identity provider |
| Mobile service | Submit port | Port rejected | Align ownership record |
| Housing | Dispatch visit | Access refused | Reissue access authority |
| Energy | Submit reading | Flagged incomplete | Register all supply points |
| Repair | Open cover claim | Outside terms | Use retailer route |

## Empirical acceptance targets

For a workshop benchmark, target at least 90% human action accuracy and 85%
top-state belief accuracy at each checkpoint. Clue-question accuracy should be
at least 90%. Strict trajectory accuracy is conjunctive and can reasonably be
lower; 70% or higher is a useful target. Results below 80% on either action
stage should trigger item-level revision rather than being explained as task
difficulty.

The blinded prosody check is separate. Target at least 80% correct delivery
category, at least 90% intelligibility, and no systematic naturalness
difference between high- and low-affect members. These thresholds must be
measured with people before making a perceptual-validity claim.

## Remaining limitation

The 84 scenarios are 14 mechanism templates crossed with distance, filler,
transcript, and voice variants. The audit therefore supports 14 independent
state mechanisms, not 84 independent human reasoning problems. Inference is
clustered by domain to avoid treating sibling variants as independent.

