#!/usr/bin/env bash
# E1. Oracle-state baseline: 3 models x 84 scenarios x 2 passes = 504 trajectories.
#
# Each model runs 6 shards in parallel; models run sequentially so a rate-limit
# stall on one does not cascade. The turn-audio cache is shared across all three
# models because user-turn audio depends only on text, voice and prosody; replay
# caches are per model because the concatenated WAV includes that model's own
# agent turns.
#
# Cost from the paid smoke test: $0.0062/trajectory for gpt-audio-mini and about
# $0.024 for either Gemini, so roughly $9 total against a $25 cap.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"

OUTDIR="paper_results/v05/raw/oracle_state"
LOGDIR="$OUTDIR/logs"
mkdir -p "$LOGDIR"

SHARDS=6
PASSES=2
SHARED_TURNS="data/runtime_audio/shared_v05/turns"

run_model() {
  local model_id="$1" slug="$2"
  echo "=== $slug ($model_id) starting $(date -u +%FT%TZ) ==="
  local pids=()
  for i in $(seq 0 $((SHARDS - 1))); do
    local shard
    shard=$(printf "%02d" "$i")
    OPENROUTER_MODEL="$model_id" \
    OPENROUTER_USAGE_PATH="$OUTDIR/${slug}_shard${shard}_usage.json" \
    python run_eval.py \
      --model openrouter \
      --conditions oracle_state \
      --passes "$PASSES" \
      --scenarios data/scenarios_v05 \
      --num-shards "$SHARDS" \
      --shard-index "$i" \
      --audio-cache "$SHARED_TURNS" \
      --replay-cache "data/runtime_audio/e1_${slug}/replays" \
      --out "$OUTDIR/${slug}_oracle_shard${shard}-of-$(printf '%02d' $SHARDS).jsonl" \
      > "$LOGDIR/${slug}_shard${shard}.out.log" \
      2> "$LOGDIR/${slug}_shard${shard}.err.log" &
    pids+=($!)
  done
  local failed=0
  for pid in "${pids[@]}"; do
    wait "$pid" || failed=1
  done
  echo "=== $slug finished $(date -u +%FT%TZ) (failed=$failed) ==="
  return 0
}

# run_eval.py only auto-appends the shard suffix when --out is omitted, so each
# shard is given an explicit distinct path here. Six processes appending to one
# file would interleave lines.
run_model "openai/gpt-audio-mini"            "gpt_audio_mini"
run_model "google/gemini-2.5-flash"          "gemini25"
run_model "google/gemini-3-flash-preview"    "gemini3"

echo "=== all models done $(date -u +%FT%TZ) ==="
wc -l "$OUTDIR"/*.jsonl 2>/dev/null | tail -5
