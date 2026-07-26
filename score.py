"""Score closed-loop trajectory JSONL.

Primary metrics are repeated-trial pass@1, scenario-majority accuracy,
between-seed variance, clustered bootstrap confidence intervals, and the
fraction of scenarios that pass every trial. pass@5 is supplemental.
"""

from __future__ import annotations

import json
import math
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path


BUCKETS = ["1-2", "5-8", "12-20"]


def load(path: str | Path) -> list[dict]:
    """Load completed, error-free trajectory rows from a JSONL result file."""

    rows = [
        json.loads(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    valid = [row for row in rows if not row.get("error")]
    if not valid:
        raise SystemExit("No successfully completed trajectories found.")
    return valid


def _mean(values) -> float:
    """Return a numeric mean, or NaN for an empty iterable."""

    values = list(values)
    return sum(values) / len(values) if values else math.nan


def clustered_bootstrap_ci(
    rows: list[dict],
    field: str = "trajectory_success",
    samples: int = 2000,
    seed: int = 8128,
) -> tuple[float, float]:
    """Bootstrap a 95% CI while resampling whole scenarios.

    Repeated seeds from one scenario remain in the same cluster, avoiding the
    overly narrow intervals produced by treating every attempt as independent.
    """

    grouped = defaultdict(list)
    for row in rows:
        grouped[row["scenario_id"]].append(bool(row[field]))
    scenario_rates = [_mean(values) for values in grouped.values()]
    rng = random.Random(seed)
    estimates = []
    for _ in range(samples):
        draw = [rng.choice(scenario_rates) for _ in scenario_rates]
        estimates.append(_mean(draw))
    estimates.sort()
    return estimates[int(samples * 0.025)], estimates[int(samples * 0.975)]


def summarize(rows: list[dict]) -> dict:
    """Compute primary reliability metrics and dynamic chance baselines."""

    by_scenario = defaultdict(list)
    by_seed = defaultdict(list)
    for row in rows:
        by_scenario[row["scenario_id"]].append(bool(row["trajectory_success"]))
        by_seed[row["seed"]].append(bool(row["trajectory_success"]))
    scenario_rates = {key: _mean(values) for key, values in by_scenario.items()}
    seed_rates = [_mean(values) for values in by_seed.values()]
    ci_low, ci_high = clustered_bootstrap_ci(rows)
    first_five = {
        key: [
            success
            for _, success in sorted(
                (
                    row["seed"],
                    bool(row["trajectory_success"]),
                )
                for row in rows
                if row["scenario_id"] == key
            )[:5]
        ]
        for key in by_scenario
    }
    return {
        "n": len(rows),
        "scenarios": len(by_scenario),
        "pass1": _mean(row["trajectory_success"] for row in rows),
        "pre": _mean(row["pre_gap_success"] for row in rows),
        "post": _mean(row["post_gap_success"] for row in rows),
        "majority": _mean(rate > 0.5 for rate in scenario_rates.values()),
        "seed_variance": statistics.variance(seed_rates) if len(seed_rates) > 1 else 0.0,
        "ci": (ci_low, ci_high),
        "all_trials": _mean(rate == 1.0 for rate in scenario_rates.values()),
        "pass_at_5": _mean(any(values) for values in first_five.values()),
        "trajectory_chance": _mean(
            1 / (row["pre_gap_menu_size"] * row["post_gap_menu_size"])
            for row in rows
        ),
        "action_chance": _mean(1 / row["post_gap_menu_size"] for row in rows),
    }


def condition_table(rows: list[dict]) -> None:
    """Print primary and supplemental metrics grouped by condition."""

    groups = defaultdict(list)
    for row in rows:
        groups[row["condition"]].append(row)
    print("\nPrimary closed-loop metrics")
    print(
        f"{'condition':<23}{'n':>5}{'pass@1':>9}{'pre':>8}{'post':>8}"
        f"{'majority':>10}{'seed var':>10}{'95% CI':>17}{'all trials':>12}"
    )
    for condition, group in groups.items():
        stats = summarize(group)
        ci = f"{stats['ci'][0]:.1%}-{stats['ci'][1]:.1%}"
        print(
            f"{condition:<23}{stats['n']:>5}{stats['pass1']:>9.1%}"
            f"{stats['pre']:>8.1%}{stats['post']:>8.1%}"
            f"{stats['majority']:>10.1%}{stats['seed_variance']:>10.4f}"
            f"{ci:>17}{stats['all_trials']:>12.1%}"
        )
    print("\nSupplemental repeated-sampling metric")
    print(
        f"{'condition':<23}{'pass@5':>9}{'action chance':>15}"
        f"{'trajectory chance':>19}"
    )
    for condition, group in groups.items():
        stats = summarize(group)
        print(
            f"{condition:<23}{stats['pass_at_5']:>9.1%}"
            f"{stats['action_chance']:>15.1%}"
            f"{stats['trajectory_chance']:>19.1%}"
        )


def paired_control_report(rows: list[dict]) -> None:
    """Report matched clue-ablation and identical-transcript prosody effects."""

    indexed = {
        (row["scenario_id"], row["seed"], row["condition"]): row for row in rows
    }

    def paired_delta(left: str, right: str, field: str) -> tuple[int, float]:
        """Return matched sample count and mean left-minus-right difference."""

        differences = []
        for scenario_id, seed, condition in indexed:
            if condition != left:
                continue
            other = indexed.get((scenario_id, seed, right))
            if other:
                differences.append(
                    float(indexed[(scenario_id, seed, left)][field])
                    - float(other[field])
                )
        return len(differences), _mean(differences)

    n, clue_delta = paired_delta(
        "full_audio", "clue_removed", "post_gap_success"
    )
    if n:
        print(
            f"\nClue-ablation check: full minus clue-removed post-gap accuracy "
            f"= {clue_delta:+.1%} across {n} paired trials."
        )
        if abs(clue_delta) < 0.05:
            print(
                "WARNING: performance barely changes under clue ablation; "
                "the tasks may not be measuring clue use."
            )

    high = {
        (row["scenario_id"], row["seed"]): row
        for row in rows
        if row["condition"] == "prosody_high"
    }
    low = {
        (row["scenario_id"], row["seed"]): row
        for row in rows
        if row["condition"] == "prosody_low"
    }
    paired = [
        (high[key], low[key])
        for key in high.keys() & low.keys()
        if high[key]["post_gap_observation"] == low[key]["post_gap_observation"]
    ]
    if paired:
        both = _mean(
            high_row["response_style_success"] is True
            and low_row["response_style_success"] is True
            for high_row, low_row in paired
        )
        print(
            f"Prosodic contrast: {both:.1%} of {len(paired)} identical-transcript "
            "pairs selected the expected approach in both deliveries."
        )


def failure_report(rows: list[dict]) -> None:
    """Print multilabel failure incidence among unsuccessful trajectories."""

    tags = Counter(
        tag
        for row in rows
        if not row["trajectory_success"]
        for tag in row.get("failure_tags", [])
    )
    if not tags:
        return
    print("\nFailure tags (multilabel counts; percentages need not sum to 100%)")
    failures = sum(not row["trajectory_success"] for row in rows)
    for tag, count in tags.most_common():
        print(f"  {tag:<30}{count:>5}  {count / failures:.1%} of failed trajectories")


def retention_curve(rows: list[dict], path: Path) -> None:
    """Plot full-audio accuracy and both dynamic random-choice floors."""

    full = [row for row in rows if row["condition"] == "full_audio"]
    if not full:
        return
    points = []
    for bucket in BUCKETS:
        group = [row for row in full if row["bucket"] == bucket]
        if group:
            points.append((bucket, summarize(group)))
    if not points:
        return

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.figure(figsize=(6.4, 4.2))
    plt.plot(
        [bucket for bucket, _ in points],
        [stats["pass1"] for _, stats in points],
        "o-",
        label="trajectory pass@1",
    )
    plt.plot(
        [bucket for bucket, _ in points],
        [stats["post"] for _, stats in points],
        "s--",
        label="post-gap action pass@1",
    )
    trajectory_chance = _mean(
        stats["trajectory_chance"] for _, stats in points
    )
    action_chance = _mean(stats["action_chance"] for _, stats in points)
    plt.axhline(
        action_chance,
        color="gray",
        linestyle=":",
        label=f"random action chance ({action_chance:.0%})",
    )
    plt.axhline(
        trajectory_chance,
        color="silver",
        linestyle="-.",
        label=f"random two-action chance ({trajectory_chance:.0%})",
    )
    plt.ylim(0, 1.05)
    plt.xlabel("clue-to-gap turn-distance bucket")
    plt.ylabel("accuracy")
    plt.title("Long-horizon conversational state tracking")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    print(f"\nRetention curve -> {path}")


def score_closed_loop(path: str | Path) -> None:
    """Run all closed-loop reports and write the retention plot."""

    rows = load(path)
    models = sorted({row["model"] for row in rows})
    print(f"Models: {', '.join(models)} | completed trajectories: {len(rows)}")
    condition_table(rows)
    paired_control_report(rows)
    failure_report(rows)
    output = Path(path).with_name(Path(path).stem + "_retention.png")
    retention_curve(rows, output)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "closed_loop":
        score_closed_loop(sys.argv[2])
    else:
        print(__doc__)
        print("Usage: python score.py closed_loop results/fake_closed_loop.jsonl")
