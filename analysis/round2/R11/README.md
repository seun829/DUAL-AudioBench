# R11. Prosody parameter audit

The only acoustic difference between the high and low conditions is the eSpeak-NG `-p` (pitch, 0-99) and `-s` (speed, words/min) pair looked up from `PROSODY` in `dual_audio/modalities/audio.py:12-19`. No amplitude, word-gap, or voice change; within a pair the words and voice are identical.

## The five distinct contrasts

| High name | pitch/speed | Low name | pitch/speed | delta pitch | delta speed | n | Direction |
|---|---|---|---|---|---|---|---|
| frustrated | 30/185 | calm | 50/160 | -20 | +25 | 30 | higher on one |
| urgent | 65/190 | calm | 50/160 | +15 | +30 | 24 | higher on both |
| confused | 60/150 | confident | 55/165 | +5 | -15 | 18 | higher on one |
| urgent | 65/190 | confident | 55/165 | +10 | +25 | 6 | higher on both |
| confused | 60/150 | calm | 50/160 | +10 | -10 | 6 | higher on one |

## Direction summary

| Direction | scenarios | share |
|---|---|---|
| higher on one | 54 | 64% |
| higher on both | 30 | 36% |

## Listening packet completion

`paper_results/v05/internal_audit/prosody/public/01_prosody_responses.csv` contains **21 rows, of which 2 have a non-empty `more_intense_clip`**.

| Item | more intense | clip A tone | clip B tone | clarity | confidence |
|---|---|---|---|---|---|
| PROSODY-01 | A | confused | urgent | both_clear | 4 |
| PROSODY-02 | B | confident | (blank) | both_clear | 4 |
| PROSODY-03 | (blank) | (blank) | (blank) | (blank) | 4 |
| PROSODY-04 | (blank) | (blank) | (blank) | (blank) | 4 |
| PROSODY-05 | (blank) | (blank) | (blank) | (blank) | 4 |
| PROSODY-06 | (blank) | (blank) | (blank) | (blank) | 4 |
| PROSODY-07 | (blank) | (blank) | (blank) | (blank) | 4 |
| PROSODY-08 | (blank) | (blank) | (blank) | (blank) | 4 |
| PROSODY-09 | (blank) | (blank) | (blank) | (blank) | 4 |
| PROSODY-10 | (blank) | (blank) | (blank) | (blank) | 4 |
| PROSODY-11 | (blank) | (blank) | (blank) | (blank) | 4 |
| PROSODY-12 | (blank) | (blank) | (blank) | (blank) | 4 |
| PROSODY-13 | (blank) | (blank) | (blank) | (blank) | 4 |
| PROSODY-14 | (blank) | (blank) | (blank) | (blank) | 4 |
| PROSODY-15 | (blank) | (blank) | (blank) | (blank) | 4 |
| PROSODY-16 | (blank) | (blank) | (blank) | (blank) | 4 |
| PROSODY-17 | (blank) | (blank) | (blank) | (blank) | 4 |
| PROSODY-18 | (blank) | (blank) | (blank) | (blank) | 4 |
| PROSODY-19 | (blank) | (blank) | (blank) | (blank) | 4 |
| PROSODY-20 | (blank) | (blank) | (blank) | (blank) | 4 |
| PROSODY-21 | (blank) | (blank) | (blank) | (blank) | 4 |

**Whether the two answered choices match the intended high member: NOT FOUND.** The intended-high mapping lives in the nested `private/` directory, which `.gitignore` excludes (`paper_results/v05/internal_audit/**/private/`) and which is absent from this checkout. The public booklet does not state it either. With 2 of 21 rows answered the comparison would be uninformative regardless.

## Reading

**The manipulation has no consistent acoustic direction, and this is the finding that should change the paper.** Of 84 scenarios, 30 have the high member higher on both pitch and speed, 54 on only one axis, and 0 on neither.

Two specific problems. In the 30 `frustrated` vs `calm` pairs the high member is **20 pitch units lower** than the low member (30 against 50), compensated only by being 25 wpm faster. In the 18 `confused` vs `confident` pairs the high member is 5 pitch units higher but **15 wpm slower** -- the smallest and most ambiguous contrast in the set. `high` and `low` name an expected *response style* (`acknowledge_impact`, `acknowledge_urgency`, `clarify_and_reassure` against `proceed_directly`), not an acoustic intensity, and the `PROSODY` table encodes no monotone intensity ordering.

Consequences for the paper. The existing hedge at `main.tex:361` ("cannot distinguish model insensitivity from an insufficiently recognizable synthetic-speech manipulation") is correct but understates the problem: it is not that the manipulation might be too subtle, it is that it is not a single-directional manipulation at all, so pooling the five contrasts into one high-versus-low contrast is not well defined. Any prosody claim has to be made per contrast, with n=30/24/18/6/6. The listening audit at 2 of 21 rows cannot settle it either way.

A third, separate confound worth noting: the two prosody conditions also change the **words**, via `PROSODY_TRANSCRIPT_FRAMES` (`dual_audio/users/scripted.py:7-11`), with 28 scenarios on each of the three carrier frames. So prosody-versus-ordinary is not a pure acoustic contrast; high-versus-low within a scenario is, because both members share that scenario's frame.
