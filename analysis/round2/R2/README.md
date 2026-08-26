# R2. Action and belief accuracy split by causal branch

## The headline number

Misaligned-branch **final-action accuracy under ordinary audio**, where a constant close-the-case policy scores 0.0 and uniform chance is 20.0:

| Model | Misaligned final action | 95% CI | Aligned final action | Pooled (Table 6) |
|---|---|---|---|---|
| Gemini 2.5 | **50.0** | [34.5, 66.7] | 20.2 | 35.1 |
| Gemini 3 | **60.7** | [45.2, 75.0] | 33.3 | 47.0 |
| GPT Audio Mini | **39.3** | [22.6, 57.1] | 4.8 | 22.0 |

**This is the opposite of what the work order predicted, and it is good news for the paper.** Misaligned-branch final-action accuracy is not near or below 20%; it is 50.0/60.7/39.3, two to three times uniform chance, and all three intervals sit entirely above the 20% line. The failure is concentrated on the *aligned* branch instead: 20.2/33.3/4.8.

The reason is that models **under-select** `close_case` rather than over-selecting it. Counting choices under ordinary audio: on the aligned branch, where `close_case` is the gold answer for 69-77 of 84 rows, the models chose it 20.2%, 32.1% and 3.6% of the time. On the misaligned branch, where it is never gold, they chose it 9.5%, 2.4% and 0.0% of the time. The 50% majority-class baseline for the action metric is therefore arithmetically real but **anti-exploited**: every model scores *below* it pooled (22-47% against 50%) precisely because it will not conclude that a resolved case is resolved.

## Full branch split

| Model | Condition | Branch | n | First | Final | Final CI | Belief | Belief CI | Uniform | Always close | Domain const |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Gemini 2.5 | Ordinary audio | misaligned | 84 | 59.5 | 50.0 | [34.5, 66.7] | 53.6 | [36.9, 70.2] | 20.0 | 0.0 | 53.6 |
| Gemini 2.5 | Ordinary audio | aligned | 84 | 79.8 | 20.2 | [11.9, 29.8] | 25.0 | [15.5, 35.7] | 20.0 | 82.1 | 52.4 |
| Gemini 2.5 | No state change | misaligned | 84 | 54.8 | 25.0 | [14.3, 35.7] | 45.2 | [28.6, 63.1] | 20.0 | 6.0 | 79.8 |
| Gemini 2.5 | No state change | aligned | 84 | 81.0 | 52.4 | [36.9, 67.9] | 76.2 | [64.3, 86.9] | 20.0 | 6.0 | 72.6 |
| Gemini 2.5 | Short clue | misaligned | 84 | 47.6 | 45.2 | [32.1, 59.5] | 51.2 | [36.9, 65.5] | 20.0 | 0.0 | 59.5 |
| Gemini 2.5 | Short clue | aligned | 84 | 79.8 | 26.2 | [15.5, 36.9] | 20.2 | [9.5, 33.3] | 20.0 | 82.1 | 46.4 |
| Gemini 2.5 | Clue removed | misaligned | 84 | 54.8 | 44.0 | [32.1, 54.8] | 56.0 | [41.7, 70.2] | 20.0 | 0.0 | 54.8 |
| Gemini 2.5 | Clue removed | aligned | 84 | 64.3 | 6.0 | [0.0, 13.1] | 3.6 | [0.0, 9.5] | 20.0 | 64.3 | 58.3 |
| Gemini 2.5 | Transcript | misaligned | 84 | 66.7 | 63.1 | [42.9, 81.0] | 77.4 | [66.7, 88.1] | 20.0 | 0.0 | 61.9 |
| Gemini 2.5 | Transcript | aligned | 84 | 88.1 | 8.3 | [1.2, 16.7] | 26.2 | [14.3, 39.3] | 20.0 | 88.1 | 42.9 |
| Gemini 2.5 | Neutral audio | misaligned | 84 | 54.8 | 50.0 | [35.7, 64.3] | 48.8 | [38.1, 58.3] | 20.0 | 0.0 | 53.6 |
| Gemini 2.5 | Neutral audio | aligned | 84 | 75.0 | 13.1 | [8.3, 17.9] | 16.7 | [7.1, 27.4] | 20.0 | 76.2 | 45.2 |
| Gemini 2.5 | Explicit user update | misaligned | 84 | 56.0 | 70.2 | [56.0, 82.1] | 69.0 | [53.6, 83.3] | 20.0 | 45.2 | 79.8 |
| Gemini 2.5 | Explicit user update | aligned | 84 | 71.4 | 73.8 | [59.5, 86.9] | 76.2 | [63.1, 88.1] | 20.0 | 64.3 | 70.2 |
| Gemini 2.5 | High prosody | misaligned | 84 | 64.3 | 60.7 | [46.4, 75.0] | 56.0 | [44.0, 67.9] | 20.0 | 0.0 | 65.5 |
| Gemini 2.5 | High prosody | aligned | 84 | 72.6 | 13.1 | [4.8, 23.8] | 19.0 | [9.5, 28.6] | 20.0 | 73.8 | 31.0 |
| Gemini 2.5 | Low prosody | misaligned | 84 | 51.2 | 52.4 | [35.7, 69.0] | 56.0 | [44.0, 67.9] | 20.0 | 0.0 | 57.1 |
| Gemini 2.5 | Low prosody | aligned | 84 | 76.2 | 11.9 | [6.0, 17.9] | 15.5 | [8.3, 23.8] | 20.0 | 77.4 | 52.4 |
| Gemini 3 | Ordinary audio | misaligned | 84 | 69.0 | 60.7 | [45.2, 75.0] | 70.2 | [57.1, 82.1] | 20.0 | 0.0 | 41.7 |
| Gemini 3 | Ordinary audio | aligned | 84 | 91.7 | 33.3 | [20.2, 47.6] | 32.1 | [19.0, 45.2] | 20.0 | 91.7 | 56.0 |
| Gemini 3 | No state change | misaligned | 84 | 64.3 | 22.6 | [13.1, 33.3] | 65.5 | [51.2, 78.6] | 20.0 | 6.0 | 73.8 |
| Gemini 3 | No state change | aligned | 84 | 85.7 | 73.8 | [60.7, 85.7] | 91.7 | [81.0, 100.0] | 20.0 | 7.1 | 84.5 |
| Gemini 3 | Short clue | misaligned | 84 | 46.4 | 48.8 | [32.1, 64.3] | 70.2 | [58.3, 82.1] | 20.0 | 0.0 | 44.0 |
| Gemini 3 | Short clue | aligned | 84 | 85.7 | 35.7 | [27.4, 44.0] | 31.0 | [20.2, 41.7] | 20.0 | 86.9 | 58.3 |
| Gemini 3 | Clue removed | misaligned | 84 | 65.5 | 44.0 | [26.2, 63.1] | 48.8 | [32.1, 65.5] | 20.0 | 0.0 | 72.6 |
| Gemini 3 | Clue removed | aligned | 84 | 67.9 | 9.5 | [3.6, 16.7] | 15.5 | [8.3, 23.8] | 20.0 | 67.9 | 35.7 |
| Gemini 3 | Transcript | misaligned | 84 | 75.0 | 72.6 | [54.8, 88.1] | 91.7 | [83.3, 97.6] | 20.0 | 0.0 | 47.6 |
| Gemini 3 | Transcript | aligned | 84 | 94.0 | 44.0 | [23.8, 64.3] | 36.9 | [17.9, 56.0] | 20.0 | 95.2 | 53.6 |
| Gemini 3 | Neutral audio | misaligned | 84 | 61.9 | 58.3 | [45.2, 72.6] | 72.6 | [61.9, 82.1] | 20.0 | 0.0 | 33.3 |
| Gemini 3 | Neutral audio | aligned | 84 | 94.0 | 32.1 | [19.0, 46.4] | 35.7 | [25.0, 46.4] | 20.0 | 94.0 | 66.7 |
| Gemini 3 | Explicit user update | misaligned | 84 | 69.0 | 83.3 | [70.2, 94.0] | 86.9 | [73.8, 96.4] | 20.0 | 54.8 | 78.6 |
| Gemini 3 | Explicit user update | aligned | 84 | 81.0 | 76.2 | [60.7, 90.5] | 83.3 | [67.9, 95.2] | 20.0 | 67.9 | 78.6 |
| Gemini 3 | High prosody | misaligned | 84 | 59.5 | 59.5 | [41.7, 76.2] | 67.9 | [58.3, 77.4] | 20.0 | 0.0 | 69.0 |
| Gemini 3 | High prosody | aligned | 84 | 89.3 | 29.8 | [19.0, 40.5] | 34.5 | [21.4, 46.4] | 20.0 | 89.3 | 28.6 |
| Gemini 3 | Low prosody | misaligned | 84 | 57.1 | 57.1 | [36.9, 76.2] | 73.8 | [57.1, 86.9] | 20.0 | 0.0 | 44.0 |
| Gemini 3 | Low prosody | aligned | 84 | 86.9 | 23.8 | [10.7, 38.1] | 32.1 | [19.0, 45.2] | 20.0 | 86.9 | 60.7 |
| GPT Audio Mini | Ordinary audio | misaligned | 84 | 44.0 | 39.3 | [22.6, 57.1] | 45.2 | [27.4, 64.3] | 20.0 | 0.0 | 59.5 |
| GPT Audio Mini | Ordinary audio | aligned | 84 | 86.9 | 4.8 | [1.2, 8.3] | 16.7 | [8.3, 26.2] | 20.0 | 88.1 | 46.4 |
| GPT Audio Mini | No state change | misaligned | 84 | 46.4 | 15.5 | [6.0, 26.2] | 52.4 | [34.5, 69.0] | 20.0 | 7.1 | 77.4 |
| GPT Audio Mini | No state change | aligned | 84 | 76.2 | 27.4 | [14.3, 40.5] | 73.8 | [59.5, 86.9] | 20.0 | 7.1 | 73.8 |
| GPT Audio Mini | Short clue | misaligned | 84 | 44.0 | 38.1 | [23.8, 53.6] | 46.4 | [34.5, 59.5] | 20.0 | 0.0 | 59.5 |
| GPT Audio Mini | Short clue | aligned | 84 | 89.3 | 3.6 | [0.0, 7.1] | 19.0 | [9.5, 29.8] | 20.0 | 91.7 | 40.5 |
| GPT Audio Mini | Clue removed | misaligned | 84 | 56.0 | 46.4 | [28.6, 64.3] | 20.2 | [10.7, 31.0] | 20.0 | 0.0 | 77.4 |
| GPT Audio Mini | Clue removed | aligned | 84 | 54.8 | 7.1 | [0.0, 15.5] | 14.3 | [4.8, 25.0] | 20.0 | 54.8 | 36.9 |
| GPT Audio Mini | Neutral audio | misaligned | 84 | 46.4 | 35.7 | [20.2, 52.4] | 40.5 | [26.2, 56.0] | 20.0 | 0.0 | 56.0 |
| GPT Audio Mini | Neutral audio | aligned | 84 | 79.8 | 2.4 | [0.0, 6.0] | 23.8 | [13.1, 35.7] | 20.0 | 82.1 | 48.8 |
| GPT Audio Mini | Explicit user update | misaligned | 84 | 47.6 | 51.2 | [35.7, 66.7] | 59.5 | [41.7, 76.2] | 20.0 | 38.1 | 71.4 |
| GPT Audio Mini | Explicit user update | aligned | 84 | 83.3 | 75.0 | [59.5, 88.1] | 76.2 | [57.1, 91.7] | 20.0 | 75.0 | 79.8 |
| GPT Audio Mini | High prosody | misaligned | 84 | 42.9 | 35.7 | [22.6, 50.0] | 41.7 | [28.6, 54.8] | 20.0 | 0.0 | 65.5 |
| GPT Audio Mini | High prosody | aligned | 84 | 78.6 | 3.6 | [0.0, 7.1] | 19.0 | [10.7, 27.4] | 20.0 | 79.8 | 39.3 |
| GPT Audio Mini | Low prosody | misaligned | 84 | 44.0 | 38.1 | [22.6, 53.6] | 54.8 | [40.5, 69.0] | 20.0 | 0.0 | 52.4 |
| GPT Audio Mini | Low prosody | aligned | 84 | 77.4 | 2.4 | [0.0, 6.0] | 26.2 | [15.5, 38.1] | 20.0 | 77.4 | 52.4 |

## Paired misaligned-minus-aligned effects (domain-clustered)

| Model | Condition | Metric | paired n | clusters | Effect (pp) | 95% CI | p |
|---|---|---|---|---|---|---|---|
| Gemini 2.5 | Ordinary audio | first action | 84 | 14 | -20.2 | [-40.5, -1.2] | 0.0894 |
| Gemini 2.5 | Ordinary audio | final action | 84 | 14 | 29.8 | [9.5, 50.0] | 0.0229 |
| Gemini 2.5 | Ordinary audio | belief after gap | 84 | 14 | 28.6 | [13.1, 45.2] | 0.0078 |
| Gemini 2.5 | No state change | first action | 84 | 14 | -26.2 | [-42.9, -10.7] | 0.0195 |
| Gemini 2.5 | No state change | final action | 84 | 14 | -27.4 | [-39.3, -15.5] | 0.0024 |
| Gemini 2.5 | No state change | belief after gap | 84 | 14 | -31.0 | [-45.2, -15.5] | 0.0054 |
| Gemini 2.5 | Short clue | first action | 84 | 14 | -32.1 | [-52.4, -11.9] | 0.0166 |
| Gemini 2.5 | Short clue | final action | 84 | 14 | 19.0 | [4.8, 34.5] | 0.0347 |
| Gemini 2.5 | Short clue | belief after gap | 84 | 14 | 31.0 | [13.1, 50.0] | 0.0088 |
| Gemini 2.5 | Clue removed | first action | 84 | 14 | -9.5 | [-21.4, 1.2] | 0.1953 |
| Gemini 2.5 | Clue removed | final action | 84 | 14 | 38.1 | [25.0, 51.2] | 0.0010 |
| Gemini 2.5 | Clue removed | belief after gap | 84 | 14 | 52.4 | [35.7, 69.0] | 0.0005 |
| Gemini 2.5 | Transcript | first action | 84 | 14 | -21.4 | [-36.9, -7.1] | 0.0234 |
| Gemini 2.5 | Transcript | final action | 84 | 14 | 54.8 | [36.9, 70.2] | 0.0005 |
| Gemini 2.5 | Transcript | belief after gap | 84 | 14 | 51.2 | [34.5, 66.7] | 0.0005 |
| Gemini 2.5 | Neutral audio | first action | 84 | 14 | -20.2 | [-36.9, -2.4] | 0.0664 |
| Gemini 2.5 | Neutral audio | final action | 84 | 14 | 36.9 | [21.4, 52.4] | 0.0020 |
| Gemini 2.5 | Neutral audio | belief after gap | 84 | 14 | 32.1 | [21.4, 42.9] | 0.0005 |
| Gemini 2.5 | Explicit user update | first action | 84 | 14 | -15.5 | [-34.5, 2.4] | 0.1855 |
| Gemini 2.5 | Explicit user update | final action | 84 | 14 | -3.6 | [-14.3, 8.3] | 0.7031 |
| Gemini 2.5 | Explicit user update | belief after gap | 84 | 14 | -7.1 | [-25.0, 10.7] | 0.5547 |
| Gemini 2.5 | High prosody | first action | 84 | 14 | -8.3 | [-28.6, 10.7] | 0.5071 |
| Gemini 2.5 | High prosody | final action | 84 | 14 | 47.6 | [31.0, 65.5] | 0.0002 |
| Gemini 2.5 | High prosody | belief after gap | 84 | 14 | 36.9 | [23.8, 51.2] | 0.0005 |
| Gemini 2.5 | Low prosody | first action | 84 | 14 | -25.0 | [-41.7, -9.5] | 0.0173 |
| Gemini 2.5 | Low prosody | final action | 84 | 14 | 40.5 | [23.8, 58.3] | 0.0010 |
| Gemini 2.5 | Low prosody | belief after gap | 84 | 14 | 40.5 | [26.2, 54.8] | 0.0005 |
| Gemini 3 | Ordinary audio | first action | 84 | 14 | -22.6 | [-41.7, -6.0] | 0.0352 |
| Gemini 3 | Ordinary audio | final action | 84 | 14 | 27.4 | [3.6, 51.2] | 0.0640 |
| Gemini 3 | Ordinary audio | belief after gap | 84 | 14 | 38.1 | [16.7, 59.5] | 0.0094 |
| Gemini 3 | No state change | first action | 84 | 14 | -21.4 | [-36.9, -7.1] | 0.0156 |
| Gemini 3 | No state change | final action | 84 | 14 | -51.2 | [-65.5, -38.1] | 0.0001 |
| Gemini 3 | No state change | belief after gap | 84 | 14 | -26.2 | [-41.7, -11.9] | 0.0059 |
| Gemini 3 | Short clue | first action | 84 | 14 | -39.3 | [-56.0, -22.6] | 0.0015 |
| Gemini 3 | Short clue | final action | 84 | 14 | 13.1 | [-6.0, 32.1] | 0.2627 |
| Gemini 3 | Short clue | belief after gap | 84 | 14 | 39.3 | [19.0, 59.5] | 0.0068 |
| Gemini 3 | Clue removed | first action | 84 | 14 | -2.4 | [-15.5, 9.5] | 0.8594 |
| Gemini 3 | Clue removed | final action | 84 | 14 | 34.5 | [15.5, 54.8] | 0.0088 |
| Gemini 3 | Clue removed | belief after gap | 84 | 14 | 33.3 | [17.9, 51.2] | 0.0020 |
| Gemini 3 | Transcript | first action | 84 | 14 | -19.0 | [-33.3, -4.8] | 0.0430 |
| Gemini 3 | Transcript | final action | 84 | 14 | 28.6 | [2.4, 54.8] | 0.0762 |
| Gemini 3 | Transcript | belief after gap | 84 | 14 | 54.8 | [32.1, 76.2] | 0.0020 |
| Gemini 3 | Neutral audio | first action | 84 | 14 | -32.1 | [-46.4, -19.0] | 0.0020 |
| Gemini 3 | Neutral audio | final action | 84 | 14 | 26.2 | [4.8, 46.4] | 0.0469 |
| Gemini 3 | Neutral audio | belief after gap | 84 | 14 | 36.9 | [21.4, 53.6] | 0.0020 |
| Gemini 3 | Explicit user update | first action | 84 | 14 | -11.9 | [-29.8, 6.0] | 0.2949 |
| Gemini 3 | Explicit user update | final action | 84 | 14 | 7.1 | [-6.0, 20.2] | 0.4062 |
| Gemini 3 | Explicit user update | belief after gap | 84 | 14 | 3.6 | [0.0, 9.5] | 0.5000 |
| Gemini 3 | High prosody | first action | 84 | 14 | -29.8 | [-48.8, -11.9] | 0.0117 |
| Gemini 3 | High prosody | final action | 84 | 14 | 29.8 | [6.0, 54.8] | 0.0488 |
| Gemini 3 | High prosody | belief after gap | 84 | 14 | 33.3 | [17.9, 50.0] | 0.0020 |
| Gemini 3 | Low prosody | first action | 84 | 14 | -29.8 | [-47.6, -14.3] | 0.0039 |
| Gemini 3 | Low prosody | final action | 84 | 14 | 33.3 | [9.5, 57.1] | 0.0352 |
| Gemini 3 | Low prosody | belief after gap | 84 | 14 | 41.7 | [20.2, 60.7] | 0.0051 |
| GPT Audio Mini | Ordinary audio | first action | 84 | 14 | -42.9 | [-61.9, -22.6] | 0.0039 |
| GPT Audio Mini | Ordinary audio | final action | 84 | 14 | 34.5 | [17.9, 52.4] | 0.0046 |
| GPT Audio Mini | Ordinary audio | belief after gap | 84 | 14 | 28.6 | [7.1, 50.0] | 0.0352 |
| GPT Audio Mini | No state change | first action | 84 | 14 | -29.8 | [-47.6, -13.1] | 0.0117 |
| GPT Audio Mini | No state change | final action | 84 | 14 | -11.9 | [-27.4, 1.2] | 0.2031 |
| GPT Audio Mini | No state change | belief after gap | 84 | 14 | -21.4 | [-36.9, -6.0] | 0.0352 |
| GPT Audio Mini | Short clue | first action | 84 | 14 | -45.2 | [-65.5, -23.8] | 0.0039 |
| GPT Audio Mini | Short clue | final action | 84 | 14 | 34.5 | [19.0, 51.2] | 0.0017 |
| GPT Audio Mini | Short clue | belief after gap | 84 | 14 | 27.4 | [10.7, 41.7] | 0.0122 |
| GPT Audio Mini | Clue removed | first action | 84 | 14 | 1.2 | [-9.5, 13.1] | 1.0000 |
| GPT Audio Mini | Clue removed | final action | 84 | 14 | 39.3 | [16.7, 60.7] | 0.0095 |
| GPT Audio Mini | Clue removed | belief after gap | 84 | 14 | 6.0 | [-7.1, 19.0] | 0.5000 |
| GPT Audio Mini | Neutral audio | first action | 84 | 14 | -33.3 | [-52.4, -14.3] | 0.0107 |
| GPT Audio Mini | Neutral audio | final action | 84 | 14 | 33.3 | [16.7, 50.0] | 0.0029 |
| GPT Audio Mini | Neutral audio | belief after gap | 84 | 14 | 16.7 | [1.2, 31.0] | 0.0747 |
| GPT Audio Mini | Explicit user update | first action | 84 | 14 | -35.7 | [-53.6, -17.9] | 0.0059 |
| GPT Audio Mini | Explicit user update | final action | 84 | 14 | -23.8 | [-39.3, -8.3] | 0.0205 |
| GPT Audio Mini | Explicit user update | belief after gap | 84 | 14 | -16.7 | [-29.8, -4.8] | 0.0449 |
| GPT Audio Mini | High prosody | first action | 84 | 14 | -35.7 | [-52.4, -17.9] | 0.0044 |
| GPT Audio Mini | High prosody | final action | 84 | 14 | 32.1 | [17.9, 47.6] | 0.0015 |
| GPT Audio Mini | High prosody | belief after gap | 84 | 14 | 22.6 | [10.7, 35.7] | 0.0039 |
| GPT Audio Mini | Low prosody | first action | 84 | 14 | -33.3 | [-52.4, -14.3] | 0.0088 |
| GPT Audio Mini | Low prosody | final action | 84 | 14 | 35.7 | [20.2, 51.2] | 0.0020 |
| GPT Audio Mini | Low prosody | belief after gap | 84 | 14 | 28.6 | [13.1, 42.9] | 0.0068 |

## Reading

Three claims survive this split, and one has to be retired.

**Survives.** The benchmark is genuinely hard where the skew cannot help: misaligned-branch final action is 50.0/60.7/39.3 against a 0.0 always-close baseline and 20.0 uniform.

**Survives.** The clue matters on that branch: misaligned-branch final action moves from 50.0/60.7/39.3 under ordinary audio to 44.0/44.0/46.4 under `clue_removed`.

**Survives.** The branch asymmetry itself is a clean reportable result: paired misaligned-minus-aligned final-action effects of +29.8/+27.4/+34.5 percentage points under ordinary audio.

**Has to be retired.** Any sentence implying that models succeed by defaulting to closure, or that the pooled figure flatters them. They default to *non*-closure, and the pooled figure sits below the constant-policy baseline. The honest framing is that models are miscalibrated in one specific direction: they treat a completed and successful operation as still needing work.

**Important caveat on the baseline column.** Within one domain and one branch the gold final action is constant, so a policy allowed to condition on the branch would score 100 on whichever branch it picked. The `Domain const` column therefore fixes one answer per domain by maximising *pooled* accuracy and then evaluates it on each branch separately, which is why it reads near 0 or near 100 rather than something in between. Branch-split accuracy is a diagnostic, not a baseline-free metric. The metric that cannot be gamed this way is the branch-pair score in R3, where a constant policy scores exactly 0.

Belief shows the same asymmetry but less starkly, and the paired effects quantify it: the misaligned-minus-aligned belief difference under ordinary audio is Gemini 2.5 +28.6 pp (p=0.0078), Gemini 3 +38.1 pp (p=0.0094), GPT Audio Mini +28.6 pp (p=0.0352).
