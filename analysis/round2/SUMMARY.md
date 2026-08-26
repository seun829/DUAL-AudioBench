# DUAL-AudioBench round-2 reanalysis: summary

Scope: Phase 0 guardrails, Phase 1 reanalysis (V1, V2, R1-R11), Phase 2 code changes (C1-C4), Phase 3 oracle-state run (E1). Every table below is regenerated from `analysis/round2/<task>/results.csv`; per-task `README.md` files carry the full breakdowns and the plain reading.

## 0. Guardrail status

| Guardrail | Status |
|---|---|
| G1 protected files unchanged | PASS -- 978-file SHA-256 manifest verified after every task (`analysis/round2/_integrity/`) |
| G2 `paper_results/` unmodified | PASS, after one self-inflicted violation that was caught and reverted (see note) |
| G3 work on a branch | PASS with a caveat: the directory was **not a git repository**, so a repo was initialised and branch `round2-baselines` created; commits carry task ids |
| G4 no invented numbers | PASS -- every figure below is read back from a committed results.csv |
| G5 API budget $25 | PASS -- E1 spend reported in section 5 |
| G6 scenario freeze | **PASS only after diagnosis** -- see below |

### G6: the freeze hash does not match, and that is benign

Running the repo's own hash routine (`scripts/run_paid_v05.ps1:16-34`) over `data/scenarios_v05/` in this checkout gives `0ac5d4ae2314662a4bed453a62088fffde024f441cc593ffe88d4d722d7e3077`, not the recorded `e16319a791ab4600f88a33f7957e66eec18be262649caac03845c161119044b9`.

**The scenarios have not drifted.** Re-hashing the same 84 files with `\n` normalised to `\r\n` reproduces the recorded hash exactly. The paid runs were made on a Windows checkout with CRLF line endings (`C:\Users\shlee\...` in every `launch_manifest.json`); this copy has LF. Content is byte-identical modulo line endings, so every number below is valid. All seven v0.5 launch manifests agree on the recorded hash.

Recommendation: change the freeze check to hash LF-normalised content, otherwise it will keep failing on any non-Windows checkout while detecting nothing.

### G2 note

`score.py closed_loop` writes its plots next to the input file. Running it against a file inside `paper_results/` created two PNGs there. Both were deleted and the 978-file manifest re-verified clean; no stored trajectory or report was touched. All later `score.py` runs use a copy under `analysis/round2/_scratch/`. Worth fixing in `score.py` so the frozen tree cannot be written to by accident.

## 1. Verdict on R1: does the belief metric survive?

**No, not as a level measurement -- and the failure is worse than the one already found in the action metric. The mechanism claim survives intact and is in fact strengthened.** The two belief variables are perfectly correlated by construction in the seven ordinary conditions: `causal_alignment` predicts the outcome role in 100% of the 84 scenarios, and the gold joint state takes only two values across the whole benchmark, `misaligned_terminal + misaligned` on 42 scenarios and `aligned_terminal + aligned` on the other 42. A single constant guess is therefore correct on exactly half the set, and a policy that also knows the domain (as every model does, since the domain is stated aloud) reaches 47.0%. `score.py` reported chance for the same cell as 12.3%. Against the corrected floor, **0 of 3 models clear their belief baseline under ordinary audio** (Gemini 2.5 39.3 vs 48.2, Gemini 3 51.2 vs 47.0, GPT Audio Mini 31.0 vs 48.2), while **3 of 3 clear it under no state change** (Gemini 2.5 60.7 vs 45.2, Gemini 3 78.6 vs 45.2, GPT Audio Mini 63.1 vs 46.4). The headline no-change effect is therefore not two above-chance conditions with one higher; it is the only condition in which post-gap belief is distinguishable from a constant answer at all. That is a cleaner statement of the paper's thesis than the current draft makes, and it should replace the level claims rather than soften them.

## 2. What changed, at a glance

| # | Finding | Consequence |
|---|---|---|
| V1 | All 104 cells of Table 6 reproduce exactly from the raw JSONL | Nothing downstream is in doubt |
| V2 | 42/42 causal pairs matched; zero critical differences | The causal design is sound; add the regression test |
| R1 | Belief baseline is ~47%, not 12.5%; ordinary audio clears for 0/3 models | Rewrite belief level claims; effect claims survive |
| R2 | Misaligned-branch final action is 50.0 / 60.7 / 39.3, **above** 20% uniform; aligned branch is 20.2 / 33.3 / 4.8 | Retire the "models default to closure" reading -- they default to non-closure |
| R3 | Branch-pair accuracy reproduces the paper's four published figures and fills in GPT Audio Mini | Promote to headline |
| R4 | Up to 51.4% of GPT Audio Mini's correct actions rest on a wrong belief | Quantifies the "action overstates state" claim |
| R5 | Ordinary-audio revision gain is -0.0091 / 0.3091 / -0.0102; user-update is 0.7783 / 0.811 / 0.4563 | Best single figure available for the paper's thesis |
| R6 | Alignment recovered 76.2 / 90.5 / 84.5%, outcome only 42.3 / 51.8 / 35.1% | Bottleneck is rule application, not clue retrieval |
| R7 | First action is answerable from the domain alone (100% domain-conditional majority) | Reframe as a menu-competence check |
| R8 | Fixed-position mean 19.99%; GPT Audio Mini below its own best fixed letter on 6/8 conditions | Shuffle is clean; that model carries no action signal |
| R9 | No-change belief effect holds and strengthens without travel | One-line sensitivity footnote closes the hole |
| R10 | 72 of 84 user actions overwrite `causal_alignment` | Explicit-user-update needs an explicit qualification |
| R11 | 54 of 84 prosody pairs are not higher on both axes; listening audit 2/21 done | Prosody cannot be pooled; report per contrast |

## 3. Sentences in `paper/main.tex` these results contradict

Quoted verbatim with line numbers. I have not edited `main.tex`; these are for the separate paper edit.

### `main.tex:252`

> We completed 4,368 trajectories with no API or runtime failures.

4,368 non-error trajectories is correct, but the raw files hold 44 error rows. 20 were retried successfully inside the same shard file (`load_done` excludes error rows so a later invocation retries them) and affect nothing. The other 24 are all `openai/gpt-audio-mini` x `transcript_only`, abandoned after `OpenRouter HTTP 400: Provider returned error`. Suggested: *"We completed 4,368 trajectories with no API or runtime failures in any reported cell. A further 24 attempts to run the transcript control through GPT Audio Mini failed at the provider and that cell is not reported."*

### `main.tex:71`

> Fixed transition rules, plain-language action descriptions, shuffled labels, appropriate chance baselines, and inspectable records make failures reproducible and attributable.

"appropriate chance baselines" was not true of the shipped code: `score.py` reported only uniform `1/menu_size` (20%) for actions and `1/|S|` (12.3%) for belief, while the real constant-policy floors are ~49% and ~47%. C1 adds `majority_class_action_chance`, `fixed_position_action_chance` and `majority_class_belief_chance` and makes majority class the primary plotted reference line, so the claim is now supportable. It was not at submission time.

### `main.tex:61`

> Removing that fact makes the paired public histories identical and limits a clue-independent policy to 50\% expected post-gap accuracy.

This sentence is **correct** and R2/R16 confirm it -- but it sits in direct tension with the 20% chance line the tables and figures reported. Worth making the connection explicit: the same 50% is both the ceiling for a clue-independent policy and the floor for a constant one, and no model's pooled final-action accuracy (22.0-47.0%) exceeds it.

### `main.tex:278`

> This pattern is consistent with the benchmark targeting meaningful post-gap difficulty rather than uniformly difficult action menus.

Survives, but the first-action figure needs its baseline stated. The gold pre-gap action is constant within each domain, so the domain-conditional majority is 100.0% -- the pre-gap checkpoint is answerable from the domain name alone. The global majority is 7.1% and best fixed position 26.2%, so 55-85% is a real result against those. Recommend describing the first action as a domain-appropriate-action check that establishes menu competence, not as evidence of state tracking.

### `main.tex:286`

> Because the no-change observation truthfully states that processing remains unresolved, the comparison captures the combined burden of a changing world and a less explicit outcome.

True for 78 of 84 scenarios, false for the 6 travel ones. Travel's gap event (`departure_delay`) has no in-flight guard, so suppressing it means the delay never arrived: the utterance says *"I checked again after forty-five minutes and the flight still shows on time"* and the gold action flips from `continue_monitoring` to `close_case`. R9 shows the belief effect survives exclusion and strengthens slightly, so a sensitivity footnote is sufficient.

### `main.tex:329`

> The contrast changes both the event source and how directly its outcome is described, so it supports an evidence-availability interpretation rather than a claim that user-driven events are intrinsically easier.

The hedge is right but incomplete. In 72 of 84 scenarios the hidden user action also **overwrites `causal_alignment`** -- the variable the early clue exists to determine and which the model is scored on reporting. In those scenarios the condition does not test clue retention at all. Add: *"in 72 of 84 scenarios the hidden user action also sets the causal-alignment variable, so this condition measures response to plainly stated evidence rather than retention of the earlier clue."*

### `main.tex:361`

> Because the one-author listening audit is not complete, these results cannot distinguish model insensitivity from an insufficiently recognizable synthetic-speech manipulation.

Understates the problem. It is not that the manipulation may be too subtle: it is **not single-directional**. Of 84 scenarios, 30 have the high member higher on both pitch and speed and 54 do not -- 30 `frustrated`/`calm` pairs have the high member 20 pitch units *lower*, and 18 `confused`/`confident` pairs have it 15 wpm *slower*. Pooling five heterogeneous contrasts into one high-vs-low comparison is not well defined, so any prosody claim must be made per contrast (n=30/24/18/6/6). The listening packet has 2 of 21 rows answered.

### `main.tex:252`

> Each supported model--condition cell contains two runs of all 84 scenarios.

Correct, and worth a variance caveat. With 2 passes a per-scenario score is one of {0, 50, 100}; the two passes disagree on final-action correctness in 16.7-47.6% of scenarios depending on the cell, and on belief correctness in 14.3-44.0%. Domain clustering handles between-domain variation, not between-pass variation, so effects smaller than roughly 10 points should not be read as established. The effects the paper leans on are far outside that band.

### `main.tex:280`

> Models frequently selected plausible actions while assigning their highest confidence to at least one incorrect state.

Now quantifiable rather than qualitative, from `belief_action_outcome` which was already being logged. Under ordinary audio, `LUCKY_ACTION` accounts for 5.1% (Gemini 3), 15.3% (Gemini 2.5) and 51.4% (GPT Audio Mini) of each model's *correct* final actions. Under `clue_removed` GPT Audio Mini reaches 71.1%.

### `main.tex:363`

> Across all conditions, the automatic diagnostics marked an incorrect state belief in 83.5--95.9\% of failed trajectories.

Not contradicted; R6 sharpens it. The missed variable is almost always the domain outcome, not the branch: under ordinary audio `causal_alignment` is recovered 76.2/90.5/84.5% while the outcome variable is recovered only 42.3/51.8/35.1%. The dominant single failure mode is *alignment right, outcome wrong* (36.9/39.3/53.6% of all trajectories), i.e. the bottleneck is applying the completion rule to a clue the model has already retrieved, not losing the clue.

### Additional statement the paper should add (no existing sentence to fix)

GPT Audio Mini's post-gap action carries no measurable signal on 6 of its 8 conditions: its final-action accuracy is at or below the score of a policy that presses one fixed letter for the whole benchmark (ordinary audio 22.0 vs 23.2, neutral audio 19.0 vs 22.6, high prosody 19.6 vs 22.0, low prosody 20.2 vs 23.2, short clue 20.8 vs 21.4, no state change 21.4 vs 23.2). The exceptions are `clue_removed` and `hidden_user_action`. This is a simpler and stronger statement than the majority-class comparison and belongs in the results.

## 4. Paste-ready LaTeX tables

All use the `\dualcolhead` macro already defined at `main.tex:33` and `booktabs`, both already loaded. Numbers are percentages unless noted.

### R1. Belief accuracy against the corrected baseline

```latex
% R1: belief accuracy against a corrected constant-policy baseline.
% Paste into paper/main.tex. Columns use the \dualcolhead macro already defined there.
\begin{table}[htbp]
  \centering
  \footnotesize
  \setlength{\tabcolsep}{5pt}
  \renewcommand{\arraystretch}{1.08}
  \caption{Post-gap belief accuracy against a corrected baseline. Uniform chance is $1/|\mathcal{S}|$ as reported by the scoring code. Majority class is the best constant state assignment available to a policy that knows only the domain. Clears is whether the domain-clustered 95\% interval lies strictly above the majority-class rate.}
  \label{tab:belief-baseline}
  \begin{tabular}{@{}llrrrrl@{}}
    \toprule
    \dualcolhead{Model} & \dualcolhead{Condition} & \dualcolhead{Belief} & \dualcolhead{95\% CI} & \dualcolhead{Uniform} & \dualcolhead{Majority} & \dualcolhead{Clears} \\
    \midrule
    Gemini 2.5 & Ordinary audio & 39.3 & [28.0, 50.6] & 12.3 & 48.2 & unclear \\
    Gemini 2.5 & No state change & 60.7 & [48.2, 73.2] & 12.3 & 45.2 & yes \\
    Gemini 2.5 & Short clue & 35.7 & [26.8, 45.8] & 12.3 & 48.2 & \textbf{no} \\
    Gemini 2.5 & Clue removed & 29.8 & [23.2, 36.3] & 12.3 & 43.5 & \textbf{no} \\
    Gemini 2.5 & Transcript & 51.8 & [43.5, 59.5] & 12.3 & 48.2 & unclear \\
    Gemini 2.5 & Neutral audio & 32.7 & [24.4, 41.1] & 12.3 & 44.0 & \textbf{no} \\
    Gemini 2.5 & Explicit user update & 72.6 & [61.9, 83.3] & 12.3 & 69.6 & unclear \\
    Gemini 2.5 & High prosody & 37.5 & [29.2, 46.4] & 12.3 & 44.0 & unclear \\
    Gemini 2.5 & Low prosody & 35.7 & [28.6, 42.9] & 12.3 & 46.4 & \textbf{no} \\
    \addlinespace
    Gemini 3 & Ordinary audio & 51.2 & [43.5, 57.7] & 12.3 & 47.0 & unclear \\
    Gemini 3 & No state change & 78.6 & [69.0, 87.5] & 12.3 & 45.2 & yes \\
    Gemini 3 & Short clue & 50.6 & [45.8, 56.0] & 12.3 & 47.0 & unclear \\
    Gemini 3 & Clue removed & 32.1 & [22.0, 41.7] & 12.3 & 44.0 & \textbf{no} \\
    Gemini 3 & Transcript & 64.3 & [55.4, 73.8] & 12.3 & 48.8 & yes \\
    Gemini 3 & Neutral audio & 54.2 & [47.6, 60.7] & 12.3 & 48.2 & unclear \\
    Gemini 3 & Explicit user update & 85.1 & [71.4, 95.8] & 12.3 & 72.0 & unclear \\
    Gemini 3 & High prosody & 51.2 & [44.0, 58.9] & 12.3 & 47.0 & unclear \\
    Gemini 3 & Low prosody & 53.0 & [43.5, 63.1] & 12.3 & 47.6 & unclear \\
    \addlinespace
    GPT Audio Mini & Ordinary audio & 31.0 & [21.4, 41.1] & 12.3 & 48.2 & \textbf{no} \\
    GPT Audio Mini & No state change & 63.1 & [49.4, 76.2] & 12.3 & 46.4 & yes \\
    GPT Audio Mini & Short clue & 32.7 & [25.6, 41.7] & 12.3 & 47.6 & \textbf{no} \\
    GPT Audio Mini & Clue removed & 17.3 & [10.1, 25.0] & 12.3 & 41.7 & \textbf{no} \\
    GPT Audio Mini & Neutral audio & 32.1 & [21.4, 43.5] & 12.3 & 45.8 & \textbf{no} \\
    GPT Audio Mini & Explicit user update & 67.9 & [50.6, 82.1] & 12.3 & 69.6 & unclear \\
    GPT Audio Mini & High prosody & 30.4 & [20.8, 39.3] & 12.3 & 44.6 & \textbf{no} \\
    GPT Audio Mini & Low prosody & 40.5 & [30.4, 51.2] & 12.3 & 44.6 & unclear \\
    \bottomrule
  \end{tabular}
\end{table}
```

### R2. Accuracy split by causal branch

```latex
% R2: action and belief accuracy split by causal branch.
% On the misaligned branch the always-close policy scores 0, so these
% numbers cannot be inflated by the answer skew documented in R16.
\begin{table*}[htbp]
  \centering
  \scriptsize
  \setlength{\tabcolsep}{5pt}
  \renewcommand{\arraystretch}{1.04}
  \caption{Accuracy split by causal branch (percent). On the misaligned branch the gold final action is always the domain repair action, so a constant close-the-case policy scores 0 and uniform chance is 20. Effect is the paired misaligned-minus-aligned difference with a domain-clustered 95\% interval.}
  \label{tab:branch-split}
  \begin{tabular}{@{}ll rrr rrr r@{}}
    \toprule
    & & \multicolumn{3}{c}{\dualcolhead{Misaligned}} & \multicolumn{3}{c}{\dualcolhead{Aligned}} & \\
    \cmidrule(lr){3-5}\cmidrule(lr){6-8}
    \dualcolhead{Model} & \dualcolhead{Condition} & \dualcolhead{First} & \dualcolhead{Final} & \dualcolhead{Belief} & \dualcolhead{First} & \dualcolhead{Final} & \dualcolhead{Belief} & \dualcolhead{$\Delta$ Final} \\
    \midrule
    Gemini 2.5 & Ordinary audio & 59.5 & 50.0 & 53.6 & 79.8 & 20.2 & 25.0 & 29.8 \\
    Gemini 2.5 & No state change & 54.8 & 25.0 & 45.2 & 81.0 & 52.4 & 76.2 & -27.4 \\
    Gemini 2.5 & Short clue & 47.6 & 45.2 & 51.2 & 79.8 & 26.2 & 20.2 & 19.0 \\
    Gemini 2.5 & Clue removed & 54.8 & 44.0 & 56.0 & 64.3 & 6.0 & 3.6 & 38.1 \\
    Gemini 2.5 & Transcript & 66.7 & 63.1 & 77.4 & 88.1 & 8.3 & 26.2 & 54.8 \\
    Gemini 2.5 & Neutral audio & 54.8 & 50.0 & 48.8 & 75.0 & 13.1 & 16.7 & 36.9 \\
    Gemini 2.5 & Explicit user update & 56.0 & 70.2 & 69.0 & 71.4 & 73.8 & 76.2 & -3.6 \\
    Gemini 2.5 & High prosody & 64.3 & 60.7 & 56.0 & 72.6 & 13.1 & 19.0 & 47.6 \\
    Gemini 2.5 & Low prosody & 51.2 & 52.4 & 56.0 & 76.2 & 11.9 & 15.5 & 40.5 \\
    \addlinespace
    Gemini 3 & Ordinary audio & 69.0 & 60.7 & 70.2 & 91.7 & 33.3 & 32.1 & 27.4 \\
    Gemini 3 & No state change & 64.3 & 22.6 & 65.5 & 85.7 & 73.8 & 91.7 & -51.2 \\
    Gemini 3 & Short clue & 46.4 & 48.8 & 70.2 & 85.7 & 35.7 & 31.0 & 13.1 \\
    Gemini 3 & Clue removed & 65.5 & 44.0 & 48.8 & 67.9 & 9.5 & 15.5 & 34.5 \\
    Gemini 3 & Transcript & 75.0 & 72.6 & 91.7 & 94.0 & 44.0 & 36.9 & 28.6 \\
    Gemini 3 & Neutral audio & 61.9 & 58.3 & 72.6 & 94.0 & 32.1 & 35.7 & 26.2 \\
    Gemini 3 & Explicit user update & 69.0 & 83.3 & 86.9 & 81.0 & 76.2 & 83.3 & 7.1 \\
    Gemini 3 & High prosody & 59.5 & 59.5 & 67.9 & 89.3 & 29.8 & 34.5 & 29.8 \\
    Gemini 3 & Low prosody & 57.1 & 57.1 & 73.8 & 86.9 & 23.8 & 32.1 & 33.3 \\
    \addlinespace
    GPT Audio Mini & Ordinary audio & 44.0 & 39.3 & 45.2 & 86.9 & 4.8 & 16.7 & 34.5 \\
    GPT Audio Mini & No state change & 46.4 & 15.5 & 52.4 & 76.2 & 27.4 & 73.8 & -11.9 \\
    GPT Audio Mini & Short clue & 44.0 & 38.1 & 46.4 & 89.3 & 3.6 & 19.0 & 34.5 \\
    GPT Audio Mini & Clue removed & 56.0 & 46.4 & 20.2 & 54.8 & 7.1 & 14.3 & 39.3 \\
    GPT Audio Mini & Neutral audio & 46.4 & 35.7 & 40.5 & 79.8 & 2.4 & 23.8 & 33.3 \\
    GPT Audio Mini & Explicit user update & 47.6 & 51.2 & 59.5 & 83.3 & 75.0 & 76.2 & -23.8 \\
    GPT Audio Mini & High prosody & 42.9 & 35.7 & 41.7 & 78.6 & 3.6 & 19.0 & 32.1 \\
    GPT Audio Mini & Low prosody & 44.0 & 38.1 & 54.8 & 77.4 & 2.4 & 26.2 & 35.7 \\
    \bottomrule
  \end{tabular}
\end{table*}
```

### R3. Branch-pair accuracy (suggested headline table)

```latex
% R3: branch-pair accuracy. A constant policy scores 0 here and uniform
% random scores 4 percent for actions, so this metric was never inflated.
\begin{table}[htbp]
  \centering
  \footnotesize
  \setlength{\tabcolsep}{5pt}
  \renewcommand{\arraystretch}{1.08}
  \caption{Branch-pair accuracy (percent of 42 causal pairs, pooled over both passes). A pair counts only if both branches are correct in the same pass, so a constant policy scores 0 and uniform random scores 4.0 for actions. Intervals are domain-clustered over the 14 domains.}
  \label{tab:branch-pair}
  \begin{tabular}{@{}llrrrr@{}}
    \toprule
    \dualcolhead{Model} & \dualcolhead{Condition} & \dualcolhead{$n$} & \dualcolhead{Both actions} & \dualcolhead{Both beliefs} & \dualcolhead{Both, both} \\
    \midrule
    Gemini 2.5 & Ordinary audio & 84 & 11.9 & 16.7 & 4.8 \\
    Gemini 2.5 & No state change & 84 & 17.9 & 39.3 & 6.0 \\
    Gemini 2.5 & Short clue & 84 & 15.5 & 9.5 & 0.0 \\
    Gemini 2.5 & Clue removed & 84 & 1.2 & 2.4 & 0.0 \\
    Gemini 2.5 & Transcript & 84 & 8.3 & 20.2 & 3.6 \\
    Gemini 2.5 & Neutral audio & 84 & 6.0 & 7.1 & 2.4 \\
    Gemini 2.5 & Explicit user update & 84 & 57.1 & 54.8 & 39.3 \\
    Gemini 2.5 & High prosody & 84 & 8.3 & 9.5 & 0.0 \\
    Gemini 2.5 & Low prosody & 84 & 6.0 & 9.5 & 1.2 \\
    \addlinespace
    Gemini 3 & Ordinary audio & 84 & 16.7 & 23.8 & 10.7 \\
    Gemini 3 & No state change & 84 & 15.5 & 60.7 & 7.1 \\
    Gemini 3 & Short clue & 84 & 15.5 & 19.0 & 4.8 \\
    Gemini 3 & Clue removed & 84 & 3.6 & 8.3 & 1.2 \\
    Gemini 3 & Transcript & 84 & 32.1 & 32.1 & 16.7 \\
    Gemini 3 & Neutral audio & 84 & 17.9 & 27.4 & 8.3 \\
    Gemini 3 & Explicit user update & 84 & 69.0 & 76.2 & 60.7 \\
    Gemini 3 & High prosody & 84 & 13.1 & 27.4 & 8.3 \\
    Gemini 3 & Low prosody & 84 & 11.9 & 26.2 & 6.0 \\
    \addlinespace
    GPT Audio Mini & Ordinary audio & 84 & 1.2 & 4.8 & 0.0 \\
    GPT Audio Mini & No state change & 84 & 8.3 & 41.7 & 1.2 \\
    GPT Audio Mini & Short clue & 84 & 1.2 & 11.9 & 0.0 \\
    GPT Audio Mini & Clue removed & 84 & 0.0 & 3.6 & 0.0 \\
    GPT Audio Mini & Neutral audio & 84 & 1.2 & 11.9 & 0.0 \\
    GPT Audio Mini & Explicit user update & 84 & 44.0 & 54.8 & 39.3 \\
    GPT Audio Mini & High prosody & 84 & 0.0 & 10.7 & 0.0 \\
    GPT Audio Mini & Low prosody & 84 & 1.2 & 17.9 & 0.0 \\
    \bottomrule
  \end{tabular}
\end{table}
```

### R4. Joint belief/action outcomes at the final checkpoint

```latex
% R4: the four-way belief/action split at the final checkpoint.
% Computed from belief_action_outcome, already stored in every trajectory.
\begin{table}[htbp]
  \centering
  \footnotesize
  \setlength{\tabcolsep}{4pt}
  \renewcommand{\arraystretch}{1.08}
  \caption{Joint belief/action outcomes at the final checkpoint (percent of 168 trajectories). Lucky action is a correct action on top of an incorrect state belief, so it measures how much reported action accuracy is unearned. Consistent is the rate at which the selected action matches the action implied by the model's own top belief.}
  \label{tab:belief-action-split}
  \begin{tabular}{@{}llrrrrr@{}}
    \toprule
    \dualcolhead{Model} & \dualcolhead{Condition} & \dualcolhead{Full} & \dualcolhead{Action fail} & \dualcolhead{Lucky} & \dualcolhead{State fail} & \dualcolhead{Consistent} \\
    \midrule
    Gemini 2.5 & Ordinary audio & 29.8 & 10.1 & 5.4 & 54.8 & 57.5 \\
    Gemini 2.5 & No state change & 27.4 & 17.3 & 11.3 & 44.0 & 56.5 \\
    Gemini 2.5 & Short clue & 21.4 & 16.7 & 14.3 & 47.6 & 45.5 \\
    Gemini 2.5 & Clue removed & 18.5 & 10.1 & 6.5 & 64.9 & 44.6 \\
    Gemini 2.5 & Transcript & 32.7 & 18.5 & 3.0 & 45.8 & 50.6 \\
    Gemini 2.5 & Neutral audio & 26.2 & 12.5 & 5.4 & 56.0 & 52.7 \\
    Gemini 2.5 & Explicit user update & 63.7 & 8.3 & 8.3 & 19.6 & 79.6 \\
    Gemini 2.5 & High prosody & 29.8 & 7.1 & 7.1 & 56.0 & 56.3 \\
    Gemini 2.5 & Low prosody & 25.6 & 12.5 & 6.5 & 55.4 & 47.9 \\
    \addlinespace
    Gemini 3 & Ordinary audio & 44.6 & 19.0 & 2.4 & 33.9 & 61.9 \\
    Gemini 3 & No state change & 38.7 & 32.1 & 9.5 & 19.6 & 59.5 \\
    Gemini 3 & Short clue & 32.7 & 20.2 & 9.5 & 37.5 & 58.9 \\
    Gemini 3 & Clue removed & 22.6 & 11.9 & 4.2 & 61.3 & 44.0 \\
    Gemini 3 & Transcript & 56.5 & 18.5 & 1.8 & 23.2 & 62.5 \\
    Gemini 3 & Neutral audio & 38.7 & 18.5 & 6.5 & 36.3 & 58.3 \\
    Gemini 3 & Explicit user update & 78.6 & 12.5 & 1.2 & 7.7 & 86.3 \\
    Gemini 3 & High prosody & 35.7 & 19.0 & 8.9 & 36.3 & 50.6 \\
    Gemini 3 & Low prosody & 32.7 & 21.4 & 7.7 & 38.1 & 55.1 \\
    \addlinespace
    GPT Audio Mini & Ordinary audio & 10.7 & 19.6 & 11.3 & 58.3 & 25.6 \\
    GPT Audio Mini & No state change & 13.1 & 42.3 & 8.3 & 36.3 & 32.7 \\
    GPT Audio Mini & Short clue & 11.9 & 15.5 & 8.9 & 63.7 & 31.0 \\
    GPT Audio Mini & Clue removed & 7.7 & 13.1 & 19.0 & 60.1 & 28.1 \\
    GPT Audio Mini & Neutral audio & 11.3 & 22.6 & 7.7 & 58.3 & 34.3 \\
    GPT Audio Mini & Explicit user update & 53.6 & 8.3 & 9.5 & 28.6 & 69.0 \\
    GPT Audio Mini & High prosody & 10.7 & 14.9 & 8.9 & 65.5 & 32.1 \\
    GPT Audio Mini & Low prosody & 10.1 & 22.0 & 10.1 & 57.7 & 31.0 \\
    \bottomrule
  \end{tabular}
\end{table}
```

### R5. Belief revision across the gap

```latex
% R5: belief revision gain and stale mass, pooled over changed variables.
% Computed from belief_revision, already stored in every trajectory.
\begin{table}[htbp]
  \centering
  \footnotesize
  \setlength{\tabcolsep}{5pt}
  \renewcommand{\arraystretch}{1.08}
  \caption{Belief revision across the gap, pooled over variables whose true state changed. Revision gain is the probability mass moved onto the new true state by the resumed evidence; reflection gain is the further movement between the belief-only checkpoint and the final action; stale mass is the probability still on the superseded state after the resumed evidence. $k$ is the number of contributing variable observations.}
  \label{tab:revision-gain}
  \begin{tabular}{@{}llrrrrr@{}}
    \toprule
    \dualcolhead{Model} & \dualcolhead{Condition} & \dualcolhead{$k$} & \dualcolhead{Revision} & \dualcolhead{Reflection} & \dualcolhead{Final} & \dualcolhead{Stale} \\
    \midrule
    Gemini 2.5 & Ordinary audio & 116 & -0.009 & 0.006 & -0.003 & 0.021 \\
    Gemini 2.5 & No state change & 108 & 0.596 & -0.298 & 0.298 & 0.028 \\
    Gemini 2.5 & Short clue & 105 & 0.142 & 0.039 & 0.181 & 0.017 \\
    Gemini 2.5 & Clue removed & 100 & 0.147 & 0.008 & 0.155 & 0.022 \\
    Gemini 2.5 & Transcript & 125 & 0.282 & 0.007 & 0.289 & 0.018 \\
    Gemini 2.5 & Neutral audio & 108 & 0.236 & 0.009 & 0.245 & 0.013 \\
    Gemini 2.5 & Explicit user update & 184 & 0.778 & 0.016 & 0.795 & 0.044 \\
    Gemini 2.5 & High prosody & 114 & 0.194 & 0.020 & 0.214 & 0.016 \\
    Gemini 2.5 & Low prosody & 105 & 0.046 & 0.051 & 0.097 & 0.023 \\
    \addlinespace
    Gemini 3 & Ordinary audio & 130 & 0.309 & 0.089 & 0.398 & 0.020 \\
    Gemini 3 & No state change & 117 & 0.585 & -0.085 & 0.500 & 0.013 \\
    Gemini 3 & Short clue & 112 & 0.280 & 0.042 & 0.322 & 0.022 \\
    Gemini 3 & Clue removed & 111 & 0.224 & 0.021 & 0.245 & 0.018 \\
    Gemini 3 & Transcript & 137 & 0.413 & 0.119 & 0.532 & 0.025 \\
    Gemini 3 & Neutral audio & 127 & 0.336 & 0.032 & 0.368 & 0.028 \\
    Gemini 3 & Explicit user update & 198 & 0.811 & 0.051 & 0.862 & 0.047 \\
    Gemini 3 & High prosody & 123 & 0.297 & 0.020 & 0.318 & 0.013 \\
    Gemini 3 & Low prosody & 116 & 0.250 & 0.020 & 0.270 & 0.014 \\
    \addlinespace
    GPT Audio Mini & Ordinary audio & 105 & -0.010 & 0.038 & 0.028 & 0.103 \\
    GPT Audio Mini & No state change & 91 & 0.272 & -0.060 & 0.212 & 0.126 \\
    GPT Audio Mini & Short clue & 108 & -0.057 & 0.010 & -0.048 & 0.114 \\
    GPT Audio Mini & Clue removed & 87 & 0.045 & 0.043 & 0.088 & 0.115 \\
    GPT Audio Mini & Neutral audio & 102 & -0.008 & 0.025 & 0.017 & 0.117 \\
    GPT Audio Mini & Explicit user update & 183 & 0.456 & 0.017 & 0.474 & 0.113 \\
    GPT Audio Mini & High prosody & 97 & -0.027 & 0.009 & -0.019 & 0.111 \\
    GPT Audio Mini & Low prosody & 96 & -0.010 & -0.016 & -0.026 & 0.119 \\
    \bottomrule
  \end{tabular}
\end{table}
```

### R9. No-change effect with travel excluded (sensitivity)

```latex
% R9: no-change effect with the six travel scenarios excluded.
\begin{table}[htbp]
  \centering
  \footnotesize
  \setlength{\tabcolsep}{5pt}
  \renewcommand{\arraystretch}{1.08}
  \caption{Sensitivity of the no-change effect to the travel domain. In thirteen domains suppressing the gap event leaves the process unfinished; in travel it means the delay never arrived, and the gold action flips. Effects are paired no-change minus ordinary audio with domain-clustered 95\% intervals.}
  \label{tab:nochange-sensitivity}
  \begin{tabular}{@{}lllrl@{}}
    \toprule
    \dualcolhead{Model} & \dualcolhead{Scope} & \dualcolhead{Metric} & \dualcolhead{$\Delta$} & \dualcolhead{95\% CI} \\
    \midrule
    Gemini 2.5 & all 14 domains & belief after gap & 21.4 & [4.8, 36.3] \\
    Gemini 2.5 & all 14 domains & final action & 3.6 & [-13.7, 20.2] \\
    Gemini 2.5 & 13 domains, travel excluded & belief after gap & 23.7 & [7.1, 39.1] \\
    Gemini 2.5 & 13 domains, travel excluded & final action & 5.8 & [-12.8, 22.4] \\
    \addlinespace
    Gemini 3 & all 14 domains & belief after gap & 27.4 & [17.3, 37.5] \\
    Gemini 3 & all 14 domains & final action & 1.2 & [-7.1, 9.5] \\
    Gemini 3 & 13 domains, travel excluded & belief after gap & 29.5 & [19.2, 39.7] \\
    Gemini 3 & 13 domains, travel excluded & final action & 2.6 & [-5.8, 10.9] \\
    \addlinespace
    GPT Audio Mini & all 14 domains & belief after gap & 32.1 & [19.0, 44.6] \\
    GPT Audio Mini & all 14 domains & final action & -0.6 & [-14.9, 13.1] \\
    GPT Audio Mini & 13 domains, travel excluded & belief after gap & 33.3 & [19.9, 46.2] \\
    GPT Audio Mini & 13 domains, travel excluded & final action & 3.2 & [-10.3, 15.4] \\
    \bottomrule
  \end{tabular}
\end{table}
```

### R11. The acoustic contrasts behind high/low prosody

```latex
% R11: the acoustic contrast behind the high/low prosody conditions.
\begin{table}[htbp]
  \centering
  \footnotesize
  \setlength{\tabcolsep}{5pt}
  \renewcommand{\arraystretch}{1.08}
  \caption{The five distinct acoustic contrasts behind the high and low prosody conditions. Pitch and speed are the eSpeak-NG \texttt{-p} and \texttt{-s} arguments; within a pair the words and voice are identical. A positive delta means the high member is higher. The manipulation has no consistent direction: in 54 of 84 scenarios the high member is lower in pitch or slower.}
  \label{tab:prosody-contrast}
  \begin{tabular}{@{}llllrrl@{}}
    \toprule
    \dualcolhead{High} & \dualcolhead{$p$/$s$} & \dualcolhead{Low} & \dualcolhead{$p$/$s$} & \dualcolhead{$\Delta p$} & \dualcolhead{$\Delta s$} & \dualcolhead{$n$} \\
    \midrule
    frustrated & 30/185 & calm & 50/160 & -20 & +25 & 30 \\
    urgent & 65/190 & calm & 50/160 & +15 & +30 & 24 \\
    confused & 60/150 & confident & 55/165 & +5 & -15 & 18 \\
    urgent & 65/190 & confident & 55/165 & +10 & +25 & 6 \\
    confused & 60/150 & calm & 50/160 & +10 & -10 & 6 \\
    \bottomrule
  \end{tabular}
\end{table}
```

## 5. Phase 3: the oracle-state run (E1)

**NOT YET COMPLETE** at the time this summary was generated.

## 6. Code changes (Phase 2)

| Task | Change | Acceptance |
|---|---|---|
| C1 | `score.py`: added `majority_class_action_chance`, `fixed_position_action_chance` (+ coverage), `majority_class_belief_chance`; new printed baseline block; majority class is now the primary plotted reference line and uniform the secondary | **PASS** -- 0 pre-existing `summarize()` fields changed, 0 text lines removed or altered, exactly 4 fields added (`analysis/round2/C1/`) |
| C2 | `report_results.py`: new per-condition `belief_action_outcomes` and `belief_revision` blocks in `metrics.json`, plus two markdown sections | Reproduces R4 and R5 to 3 decimals from an independent implementation |
| C3 | `oracle_state` condition: 2 new `Condition` fields, 1 new `Observation` field, checkpoint-1 gate, oracle sentence builder, prompt change (belief request and `state_belief` example key both dropped so the derived `response_format` stays consistent) | **PASS** -- 108 MockAgent trajectories over all 9 pre-existing conditions are byte-identical before and after (SHA-256 `39891860e2c6f749...`) |
| C4 | `tests/test_round2_baselines.py`: 17 tests covering the paired-scenario invariant, majority-class-vs-uniform, and oracle injection | 17/17 pass; full suite 83 tests, 1 pre-existing unrelated failure |

The one pre-existing test failure is `test_openrouter.test_missing_key_fails_before_network_request`, which fails identically on the pre-round-2 commit: the test clears the environment but `_api_key()` falls back to reading `.env`, which holds a real key in this checkout, so the adapter attempts a network call instead of raising. Environmental, not a regression. Worth fixing by having the test point `_api_key` at a temporary directory.

## 7. NOT FOUND / not computed

- **Whether the two answered prosody-audit rows match the intended high member.** The intended-high mapping lives in `paper_results/v05/internal_audit/prosody/private/`, which `.gitignore` excludes and which is absent from this checkout. With 2 of 21 rows answered the comparison would be uninformative anyway. (R11)
- **Whether the auditor `author_01` is an author who did not write the scenarios.** The repo records only the opaque id; there is no contributor file and no scenario-authorship field, and the paper is anonymised. Nothing in the repo can establish independence from scenario authorship.
- **Travel-only no-change effects** are reported in R9's CSV but are one domain cluster, so `paired_cluster_effect` has nothing to bootstrap and the intervals are degenerate by construction. They must not be quoted as an effect.

Nothing else in the work order was unresolvable. V1's acceptance criterion "zero rows with a non-null error" is the one stated expectation that turned out to be false as written; the corrected version is in section 3.

