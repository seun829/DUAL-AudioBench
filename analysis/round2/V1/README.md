# V1. Reproduce the paper's complete condition table (Table 6)

Recomputed from every non-error row under `paper_results/v05/raw/`. Paper values transcribed from `paper/main.tex` Table 6 (`tab:all-results`, lines 452-481).

## Cell comparison (percent; `=` means the recomputed value matches)

| Model | Condition | n | First | Final | Belief | Strict |
|---|---|---|---|---|---|---|
| Gemini 2.5 | Ordinary audio | 168 | 69.6 = | 35.1 = | 39.3 = | 1.2 = |
| Gemini 2.5 | No state change | 168 | 67.9 = | 38.7 = | 60.7 = | 8.9 = |
| Gemini 2.5 | Short clue | 168 | 63.7 = | 35.7 = | 35.7 = | 1.8 = |
| Gemini 2.5 | Clue removed | 168 | 59.5 = | 25.0 = | 29.8 = | 1.2 = |
| Gemini 2.5 | Transcript | 168 | 77.4 = | 35.7 = | 51.8 = | 10.1 = |
| Gemini 2.5 | Neutral audio | 168 | 64.9 = | 31.5 = | 32.7 = | 0.6 = |
| Gemini 2.5 | Explicit user update | 168 | 63.7 = | 72.0 = | 72.6 = | 17.9 = |
| Gemini 2.5 | High prosody | 168 | 68.5 = | 36.9 = | 37.5 = | 0.6 = |
| Gemini 2.5 | Low prosody | 168 | 63.7 = | 32.1 = | 35.7 = | 3.6 = |
| Gemini 3 | Ordinary audio | 168 | 80.4 = | 47.0 = | 51.2 = | 14.9 = |
| Gemini 3 | No state change | 168 | 75.0 = | 48.2 = | 78.6 = | 21.4 = |
| Gemini 3 | Short clue | 168 | 66.1 = | 42.3 = | 50.6 = | 11.9 = |
| Gemini 3 | Clue removed | 168 | 66.7 = | 26.8 = | 32.1 = | 3.6 = |
| Gemini 3 | Transcript | 168 | 84.5 = | 58.3 = | 64.3 = | 21.4 = |
| Gemini 3 | Neutral audio | 168 | 78.0 = | 45.2 = | 54.2 = | 10.7 = |
| Gemini 3 | Explicit user update | 168 | 75.0 = | 79.8 = | 85.1 = | 22.0 = |
| Gemini 3 | High prosody | 168 | 74.4 = | 44.6 = | 51.2 = | 0.6 = |
| Gemini 3 | Low prosody | 168 | 72.0 = | 40.5 = | 53.0 = | 2.4 = |
| GPT Audio Mini | Ordinary audio | 168 | 65.5 = | 22.0 = | 31.0 = | 0.0 = |
| GPT Audio Mini | No state change | 168 | 61.3 = | 21.4 = | 63.1 = | 3.0 = |
| GPT Audio Mini | Short clue | 168 | 66.7 = | 20.8 = | 32.7 = | 1.2 = |
| GPT Audio Mini | Clue removed | 168 | 55.4 = | 26.8 = | 17.3 = | 0.6 = |
| GPT Audio Mini | Neutral audio | 168 | 63.1 = | 19.0 = | 32.1 = | 0.6 = |
| GPT Audio Mini | Explicit user update | 168 | 65.5 = | 63.1 = | 67.9 = | 8.9 = |
| GPT Audio Mini | High prosody | 168 | 60.7 = | 19.6 = | 30.4 = | 0.0 = |
| GPT Audio Mini | Low prosody | 168 | 60.7 = | 20.2 = | 40.5 = | 0.6 = |

## Integrity audit

| check | value | verdict |
|---|---|---|
| total non-error rows | 4368 | PASS |
| total rows in files | 4412 | PASS |
| error rows in files | 44 | FAIL (expected 0) |
| error rows never retried | 24 | FAIL (expected 0) |
| conditions for Gemini 2.5 | 9 | PASS |
| conditions for Gemini 3 | 9 | PASS |
| conditions for GPT Audio Mini | 8 | PASS |
| populated cells with n!=168 | 0 | PASS |
| populated cells | 26 | PASS |

Error rows with no successful retry, by cell:

| model | condition | count |
|---|---|---|
| GPT Audio Mini | Transcript | 24 |

## Reading

All 104 compared cells (26 populated model-condition cells x 4 metrics) match `paper/main.tex` Table 6 to one decimal place. Every populated cell has exactly n=168, there are 26 populated cells (9 + 9 + 8), and 4,368 non-error rows in total, as the work order states.

One correction to the work order's acceptance list: the raw files contain **44 error rows**, not zero. 20 of them were retried successfully within the same shard file (`load_done` in `run_eval.py` deliberately excludes error rows so a later invocation retries them), so they do not affect any reported number. The remaining 24 are all `openai/gpt-audio-mini` x `transcript_only`, an abandoned attempt that failed with `OpenRouter HTTP 400: Provider returned error` -- that model cannot serve the text-only endpoint used by the transcript control. That is why GPT Audio Mini has 8 conditions rather than 9, and why the paper's Table 6 correctly omits the cell. The accurate claim is *zero error rows among the 26 reported cells*.
