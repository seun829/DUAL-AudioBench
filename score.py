"""Score closed-loop trajectory JSONL.

Primary metrics are repeated-trial pass@1, scenario-majority accuracy,
between-seed variance, domain-clustered confidence intervals, and the fraction
of scenarios that pass every trial. pass@k is labeled with the trials actually
available rather than silently calling a two-trial run pass@5.
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


def _fmt_percent(value: float) -> str:
    """Format a fraction or render unavailable values as a dash."""

    return "-" if math.isnan(value) else f"{value:.1%}"


def expected_calibration_error(
    predictions: list[tuple[float, bool]],
    bins: int = 10,
) -> float:
    """Compute top-state expected calibration error over fixed-width bins."""

    if not predictions:
        return math.nan
    total = len(predictions)
    error = 0.0
    for index in range(bins):
        lower = index / bins
        upper = (index + 1) / bins
        members = [
            (confidence, correct)
            for confidence, correct in predictions
            if lower <= confidence < upper
            or (index == bins - 1 and confidence == 1.0)
        ]
        if not members:
            continue
        mean_confidence = _mean(confidence for confidence, _ in members)
        accuracy = _mean(correct for _, correct in members)
        error += len(members) / total * abs(mean_confidence - accuracy)
    return error


def clustered_bootstrap_ci(
    rows: list[dict],
    field: str = "trajectory_success",
    samples: int = 20000,
    seed: int = 8128,
    cluster_field: str = "domain",
) -> tuple[float, float]:
    """Bootstrap a 95% CI while resampling independent task families.

    All distance/variant/seed siblings from one domain remain together.  Rows
    without a domain fall back to scenario clustering for backwards-compatible
    synthetic tests.
    """

    grouped = defaultdict(list)
    for row in rows:
        cluster = row.get(cluster_field) or row["scenario_id"]
        grouped[cluster].append(float(row[field]))
    cluster_rates = [_mean(values) for values in grouped.values()]
    rng = random.Random(seed)
    estimates = []
    for _ in range(samples):
        draw = [rng.choice(cluster_rates) for _ in cluster_rates]
        estimates.append(_mean(draw))
    estimates.sort()
    return estimates[int(samples * 0.025)], estimates[int(samples * 0.975)]


def paired_cluster_effect(
    rows: list[dict],
    left: str,
    right: str,
    field: str,
    samples: int = 20000,
    seed: int = 8128,
) -> dict:
    """Return a matched condition effect with domain-level uncertainty.

    Pairing occurs by scenario and seed. Differences are averaged inside each
    domain before bootstrap resampling. With at most 20 domains, an exact
    two-sided sign-flip test supplies the p-value.
    """

    indexed = {
        (row["scenario_id"], row["seed"], row["condition"]): row
        for row in rows
        if not row.get("error")
    }
    by_domain = defaultdict(list)
    for scenario_id, run_seed, condition in indexed:
        if condition != left:
            continue
        other = indexed.get((scenario_id, run_seed, right))
        if other is None:
            continue
        row = indexed[(scenario_id, run_seed, left)]
        domain = row.get("domain") or scenario_id
        by_domain[domain].append(float(row[field]) - float(other[field]))
    domain_effects = [_mean(values) for values in by_domain.values()]
    n_pairs = sum(len(values) for values in by_domain.values())
    if not domain_effects:
        return {
            "left": left,
            "right": right,
            "field": field,
            "paired_n": 0,
            "clusters": 0,
            "delta": math.nan,
            "ci": (math.nan, math.nan),
            "p_value": math.nan,
        }
    estimate = _mean(domain_effects)
    rng = random.Random(seed)
    boot = []
    for _ in range(samples):
        boot.append(
            _mean(rng.choice(domain_effects) for _ in domain_effects)
        )
    boot.sort()
    ci = (boot[int(samples * 0.025)], boot[int(samples * 0.975)])
    if len(domain_effects) <= 20:
        extreme = 0
        permutations = 1 << len(domain_effects)
        for mask in range(permutations):
            trial = _mean(
                effect if mask & (1 << index) else -effect
                for index, effect in enumerate(domain_effects)
            )
            extreme += abs(trial) >= abs(estimate) - 1e-12
        p_value = extreme / permutations
    else:
        trials = 20000
        extreme = sum(
            abs(_mean(effect * rng.choice((-1, 1)) for effect in domain_effects))
            >= abs(estimate) - 1e-12
            for _ in range(trials)
        )
        p_value = extreme / trials
    return {
        "left": left,
        "right": right,
        "field": field,
        "paired_n": n_pairs,
        "clusters": len(domain_effects),
        "delta": estimate,
        "ci": ci,
        "p_value": p_value,
        "domain_effects": dict(zip(by_domain, domain_effects)),
    }


def paired_checkpoint_effect(
    rows: list[dict],
    left: str,
    right: str,
    checkpoint: str,
) -> dict:
    """Compare checkpoint top-state accuracy between matched conditions."""

    augmented = []
    for row in rows:
        copied = dict(row)
        copied["_checkpoint_correct"] = bool(
            row["belief_checkpoints"][checkpoint]["evaluation"]["all_correct"]
        )
        augmented.append(copied)
    return paired_cluster_effect(
        augmented, left, right, "_checkpoint_correct"
    )


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
    pass_k = min(5, max(len(values) for values in by_scenario.values()))
    first_k = {
        key: [
            success
            for _, success in sorted(
                (
                    row["seed"],
                    bool(row["trajectory_success"]),
                )
                for row in rows
                if row["scenario_id"] == key
            )[:pass_k]
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
        "pass_k": pass_k,
        "pass_at_k": _mean(any(values) for values in first_k.values()),
        "pass_at_5": (
            _mean(any(values) for values in first_k.values())
            if pass_k == 5
            else None
        ),
        "two_action_chance": _mean(
            1 / (row["pre_gap_menu_size"] * row["post_gap_menu_size"])
            for row in rows
        ),
        "action_trajectory_chance": _mean(
            1
            / (
                row["pre_gap_menu_size"]
                * row["post_gap_menu_size"]
                * row.get("response_style_menu_size", 1)
            )
            for row in rows
        ),
        "trajectory_chance": _mean(
            (
                1
                / (
                    row["pre_gap_menu_size"]
                    * row["post_gap_menu_size"]
                    * row.get("response_style_menu_size", 1)
                )
            )
            * row.get("belief_checkpoint_chance", 1.0) ** 3
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
        f"{'majority':>10}{'seed var':>10}{'domain 95% CI':>19}{'all trials':>12}"
    )
    for condition, group in groups.items():
        stats = summarize(group)
        ci = f"{stats['ci'][0]:.1%}-{stats['ci'][1]:.1%}"
        print(
            f"{condition:<23}{stats['n']:>5}{stats['pass1']:>9.1%}"
            f"{stats['pre']:>8.1%}{stats['post']:>8.1%}"
            f"{stats['majority']:>10.1%}{stats['seed_variance']:>10.4f}"
            f"{ci:>19}{stats['all_trials']:>12.1%}"
        )
    print("\nSupplemental repeated-sampling metric")
    observed_k = min(summarize(group)["pass_k"] for group in groups.values())
    print(
        f"{'condition':<23}{f'pass@{observed_k}':>9}{'action chance':>15}"
        f"{'2-action chance':>18}{'full chance':>14}"
    )
    for condition, group in groups.items():
        stats = summarize(group)
        print(
            f"{condition:<23}{stats['pass_at_k']:>9.1%}"
            f"{stats['action_chance']:>15.1%}"
            f"{stats['two_action_chance']:>18.1%}"
            f"{stats['trajectory_chance']:>14.3%}"
        )


def summarize_beliefs(rows: list[dict]) -> dict:
    """Aggregate checkpoint accuracy, revision, calibration, and consistency."""

    checkpoint_names = ("pre_gap", "post_observation", "pre_final_action")
    checkpoint_accuracy = {}
    checkpoint_validity = {}
    calibration_predictions = []
    brier_scores = []
    action_consistency = {"pre_gap": [], "pre_final_action": []}
    risk_consistency = []
    uncertainty = Counter()
    outcome_matrix = Counter()

    for checkpoint_name in checkpoint_names:
        checkpoints = [
            row["belief_checkpoints"][checkpoint_name] for row in rows
        ]
        checkpoint_accuracy[checkpoint_name] = _mean(
            checkpoint["evaluation"]["all_correct"]
            for checkpoint in checkpoints
        )
        checkpoint_validity[checkpoint_name] = _mean(
            checkpoint["report_valid"] for checkpoint in checkpoints
        )
        for checkpoint in checkpoints:
            risk_consistency.append(
                checkpoint["risk_calibration_consistent"]
            )
            uncertainty[checkpoint["uncertainty_behavior"]] += 1
            outcome = checkpoint.get("belief_action_outcome")
            if outcome:
                outcome_matrix[outcome] += 1
            consistency = checkpoint.get("action_belief_consistent")
            if (
                checkpoint_name in action_consistency
                and consistency is not None
            ):
                action_consistency[checkpoint_name].append(consistency)
            for variable in checkpoint["evaluation"]["variables"].values():
                if not variable["valid"]:
                    continue
                calibration_predictions.append(
                    (variable["confidence"], variable["correct"])
                )
                brier_scores.append(variable["brier"])

    revision = [
        row["belief_revision"]["mean_revision_gain"]
        for row in rows
        if row["belief_revision"]["mean_revision_gain"] is not None
    ]
    final_revision = [
        row["belief_revision"]["mean_final_revision_gain"]
        for row in rows
        if row["belief_revision"]["mean_final_revision_gain"] is not None
    ]
    stale = [
        row["belief_revision"]["mean_stale_belief_persistence"]
        for row in rows
        if row["belief_revision"]["mean_stale_belief_persistence"] is not None
    ]
    return {
        "checkpoint_accuracy": checkpoint_accuracy,
        "checkpoint_validity": checkpoint_validity,
        "revision_gain": _mean(revision),
        "final_revision_gain": _mean(final_revision),
        "stale_belief_persistence": _mean(stale),
        "mean_brier": _mean(brier_scores),
        "ece": expected_calibration_error(calibration_predictions),
        "pre_action_belief_consistency": _mean(action_consistency["pre_gap"]),
        "final_action_belief_consistency": _mean(
            action_consistency["pre_final_action"]
        ),
        "risk_calibration_consistency": _mean(risk_consistency),
        "uncertainty_behavior": uncertainty,
        "outcome_matrix": outcome_matrix,
    }


def _belief_jsd(left: dict, right: dict) -> float:
    """Return normalized Jensen-Shannon divergence across shared variables."""

    divergences = []
    for variable in left.keys() & right.keys():
        labels = left[variable].keys() | right[variable].keys()
        p = [float(left[variable].get(label, 0.0)) for label in labels]
        q = [float(right[variable].get(label, 0.0)) for label in labels]
        midpoint = [(a + b) / 2 for a, b in zip(p, q)]

        def kl(values, target):
            return sum(
                value * math.log(value / reference)
                for value, reference in zip(values, target)
                if value > 0 and reference > 0
            )

        divergences.append((kl(p, midpoint) + kl(q, midpoint)) / (2 * math.log(2)))
    return _mean(divergences)


def _clustered_pair_summary(pairs: list[tuple[dict, dict]], value_fn) -> dict:
    """Summarize a paired quantity after averaging dependent rows by domain."""

    grouped = defaultdict(list)
    for left, right in pairs:
        value = float(value_fn(left, right))
        if math.isfinite(value):
            grouped[left.get("domain") or left["scenario_id"]].append(value)
    effects = [_mean(values) for values in grouped.values()]
    if not effects:
        return {"mean": math.nan, "ci": (math.nan, math.nan), "clusters": 0}
    rng = random.Random(8128)
    boot = sorted(
        _mean(rng.choice(effects) for _ in effects)
        for _ in range(20000)
    )
    return {
        "mean": _mean(effects),
        "ci": (boot[500], boot[19500]),
        "clusters": len(effects),
    }


def summarize_prosody(rows: list[dict]) -> dict:
    """Measure style sensitivity and factual invariance on high/low pairs."""

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
    pairs = [
        (high[key], low[key])
        for key in sorted(high.keys() & low.keys())
        if high[key]["post_gap_observation"] == low[key]["post_gap_observation"]
    ]
    if not pairs:
        return {"paired_n": 0, "unique_stimuli": 0}

    def belief(row, checkpoint):
        return row["belief_checkpoints"][checkpoint]["state_belief"]

    def top_assignment(value):
        return {
            variable: max(distribution, key=distribution.get)
            for variable, distribution in value.items()
            if distribution
        }

    style_contrast = _clustered_pair_summary(
        pairs,
        lambda high_row, low_row: (
            (high_row.get("response_style") == high_row.get("expected_response_style"))
            - (low_row.get("response_style") == high_row.get("expected_response_style"))
        ),
    )
    both_correct = _clustered_pair_summary(
        pairs,
        lambda high_row, low_row: (
            high_row.get("response_style_success") is True
            and low_row.get("response_style_success") is True
        ),
    )
    action_invariance = _clustered_pair_summary(
        pairs,
        lambda high_row, low_row: (
            high_row.get("post_gap_action") == low_row.get("post_gap_action")
        ),
    )
    belief_invariance = _clustered_pair_summary(
        pairs,
        lambda high_row, low_row: (
            top_assignment(belief(high_row, "post_observation"))
            == top_assignment(belief(low_row, "post_observation"))
        ),
    )
    post_jsd = _clustered_pair_summary(
        pairs,
        lambda high_row, low_row: _belief_jsd(
            belief(high_row, "post_observation"),
            belief(low_row, "post_observation"),
        ),
    )
    final_jsd = _clustered_pair_summary(
        pairs,
        lambda high_row, low_row: _belief_jsd(
            belief(high_row, "pre_final_action"),
            belief(low_row, "pre_final_action"),
        ),
    )
    categories = {}
    for category in sorted({left["post_gap_prosody"] for left, _ in pairs}):
        category_pairs = [pair for pair in pairs if pair[0]["post_gap_prosody"] == category]
        categories[category] = {
            "pairs": len(category_pairs),
            "both_correct": _clustered_pair_summary(
                category_pairs,
                lambda left, right: (
                    left.get("response_style_success") is True
                    and right.get("response_style_success") is True
                ),
            ),
        }
    return {
        "paired_n": len(pairs),
        "unique_stimuli": len(
            {
                left.get("prosody_stimulus_id") or left["scenario_id"]
                for left, _ in pairs
            }
        ),
        "both_style_random_chance": _mean(
            1
            / max(left.get("response_style_menu_size", 1), 1)
            / max(right.get("response_style_menu_size", 1), 1)
            for left, right in pairs
        ),
        "high_style_accuracy": _mean(
            left.get("response_style_success") is True for left, _ in pairs
        ),
        "low_style_accuracy": _mean(
            right.get("response_style_success") is True for _, right in pairs
        ),
        "high_style": _clustered_pair_summary(
            pairs,
            lambda left, right: left.get("response_style_success") is True,
        ),
        "low_style": _clustered_pair_summary(
            pairs,
            lambda left, right: right.get("response_style_success") is True,
        ),
        "both_style_correct": both_correct,
        "style_contrast": style_contrast,
        "technical_action_invariance": action_invariance,
        "post_observation_top_belief_invariance": belief_invariance,
        "post_observation_belief_jsd": post_jsd,
        "pre_final_belief_jsd": final_jsd,
        "categories": categories,
    }


def belief_report(rows: list[dict]) -> None:
    """Print explicit belief-state, revision, calibration, and coupling metrics."""

    groups = defaultdict(list)
    for row in rows:
        groups[row["condition"]].append(row)

    print("\nExplicit hidden-state belief tracking")
    print(
        f"{'condition':<23}{'valid':>8}{'pre':>8}{'post obs':>10}"
        f"{'pre-final':>11}{'revision':>10}{'stale':>9}"
        f"{'Brier':>9}{'ECE':>8}"
    )
    for condition, group in groups.items():
        stats = summarize_beliefs(group)
        accuracy = stats["checkpoint_accuracy"]
        validity = _mean(stats["checkpoint_validity"].values())
        print(
            f"{condition:<23}{_fmt_percent(validity):>8}"
            f"{_fmt_percent(accuracy['pre_gap']):>8}"
            f"{_fmt_percent(accuracy['post_observation']):>10}"
            f"{_fmt_percent(accuracy['pre_final_action']):>11}"
            f"{_fmt_percent(stats['revision_gain']):>10}"
            f"{_fmt_percent(stats['stale_belief_persistence']):>9}"
            f"{stats['mean_brier']:>9.3f}{_fmt_percent(stats['ece']):>8}"
        )

    print("\nBelief-action and risk consistency")
    print(
        f"{'condition':<23}{'pre A-B':>10}{'final A-B':>11}"
        f"{'risk flag':>11}{'uncertain act':>15}{'uncertain check':>17}"
    )
    all_outcomes = Counter()
    for condition, group in groups.items():
        stats = summarize_beliefs(group)
        uncertainty = stats["uncertainty_behavior"]
        total = sum(uncertainty.values())
        all_outcomes.update(stats["outcome_matrix"])
        print(
            f"{condition:<23}"
            f"{_fmt_percent(stats['pre_action_belief_consistency']):>10}"
            f"{_fmt_percent(stats['final_action_belief_consistency']):>11}"
            f"{_fmt_percent(stats['risk_calibration_consistency']):>11}"
            f"{_fmt_percent(uncertainty['UNCERTAIN_ACTED'] / total):>15}"
            f"{_fmt_percent(uncertainty['UNCERTAIN_RECHECKED'] / total):>17}"
        )

    print("\nBelief x action outcome matrix (pre-gap and final decisions)")
    total_outcomes = sum(all_outcomes.values())
    for outcome in (
        "FULL_SUCCESS",
        "ACTION_SELECTION_FAILURE",
        "LUCKY_ACTION",
        "STATE_SYNCHRONIZATION_FAILURE",
    ):
        count = all_outcomes[outcome]
        print(f"  {outcome:<34}{count:>5}  {count / total_outcomes:.1%}")


def paired_control_report(rows: list[dict]) -> None:
    """Report matched controls with domain-clustered uncertainty."""

    if {"full_audio", "transcript_only"} <= {
        row["condition"] for row in rows
    }:
        print("\nTranscript minus audio paired effects (domain clustered)")
        modality_effects = [
            (
                "pre-gap action",
                paired_cluster_effect(
                    rows, "transcript_only", "full_audio", "pre_gap_success"
                ),
            ),
            (
                "post-gap action",
                paired_cluster_effect(
                    rows, "transcript_only", "full_audio", "post_gap_success"
                ),
            ),
            (
                "post-observation belief",
                paired_checkpoint_effect(
                    rows, "transcript_only", "full_audio", "post_observation"
                ),
            ),
            (
                "strict trajectory",
                paired_cluster_effect(
                    rows, "transcript_only", "full_audio", "trajectory_success"
                ),
            ),
        ]
        for label, effect in modality_effects:
            print(
                f"  {label:<25}{effect['delta']:+.1%} "
                f"[{effect['ci'][0]:+.1%}, {effect['ci'][1]:+.1%}] "
                f"p={effect['p_value']:.4f}"
            )

    clue = paired_cluster_effect(
        rows, "full_audio", "clue_removed", "post_gap_success"
    )
    if clue["paired_n"]:
        print(
            f"\nClue-ablation check: full minus clue-removed post-gap accuracy "
            f"= {clue['delta']:+.1%} "
            f"[{clue['ci'][0]:+.1%}, {clue['ci'][1]:+.1%}], "
            f"p={clue['p_value']:.4f}; {clue['clusters']} domain clusters, "
            f"{clue['paired_n']} paired trials."
        )
        if clue["ci"][0] <= 0 <= clue["ci"][1]:
            print(
                "WARNING: the domain-clustered clue effect is inconclusive."
            )

    prosody = summarize_prosody(rows)
    if prosody["paired_n"]:
        both = prosody["both_style_correct"]
        print(
            f"Prosodic contrast: {both['mean']:.1%} both-correct "
            f"[{both['ci'][0]:.1%}, {both['ci'][1]:.1%}] across "
            f"{prosody['paired_n']} pairs/{prosody['unique_stimuli']} stimuli; "
            f"action invariance={prosody['technical_action_invariance']['mean']:.1%}, "
            f"belief invariance={prosody['post_observation_top_belief_invariance']['mean']:.1%}, "
            f"belief JSD={prosody['post_observation_belief_jsd']['mean']:.3f}."
        )

    user_action = paired_cluster_effect(
        rows, "hidden_user_action", "full_audio", "post_gap_success"
    )
    if user_action["paired_n"]:
        print(
            f"Hidden-user-action check: dual-control minus external-only "
            f"post-gap accuracy = {user_action['delta']:+.1%} "
            f"[{user_action['ci'][0]:+.1%}, {user_action['ci'][1]:+.1%}]."
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
    plt.errorbar(
        [bucket for bucket, _ in points],
        [stats["pass1"] for _, stats in points],
        yerr=[
            [stats["pass1"] - stats["ci"][0] for _, stats in points],
            [stats["ci"][1] - stats["pass1"] for _, stats in points],
        ],
        fmt="o-",
        capsize=3,
        label="trajectory pass@1",
    )
    post_cis = [
        clustered_bootstrap_ci(
            [row for row in full if row["bucket"] == bucket],
            "post_gap_success",
        )
        for bucket, _ in points
    ]
    plt.errorbar(
        [bucket for bucket, _ in points],
        [stats["post"] for _, stats in points],
        yerr=[
            [stats["post"] - ci[0] for (_, stats), ci in zip(points, post_cis)],
            [ci[1] - stats["post"] for (_, stats), ci in zip(points, post_cis)],
        ],
        fmt="s--",
        capsize=3,
        label="post-gap action pass@1",
    )
    trajectory_chance = _mean(
        stats["trajectory_chance"] for _, stats in points
    )
    action_trajectory_chance = _mean(
        stats["two_action_chance"] for _, stats in points
    )
    action_chance = _mean(stats["action_chance"] for _, stats in points)
    plt.axhline(
        action_chance,
        color="gray",
        linestyle=":",
        label=f"random action chance ({action_chance:.0%})",
    )
    plt.axhline(
        action_trajectory_chance,
        color="silver",
        linestyle="-.",
        label=(
            f"random two-action chance "
            f"({action_trajectory_chance:.0%})"
        ),
    )
    plt.axhline(
        trajectory_chance,
        color="lightgray",
        linestyle="--",
        label=f"random action+belief chance ({trajectory_chance:.2%})",
    )
    plt.ylim(0, 1.05)
    plt.xlabel("clue-to-gap turn-distance bucket")
    plt.ylabel("accuracy")
    plt.title("Long-horizon conversational state tracking")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    print(f"\nRetention curve -> {path}")


def modality_belief_curve(rows: list[dict], path: Path) -> None:
    """Plot immediate belief accuracy by distance for audio and transcript."""

    conditions = ("full_audio", "transcript_only")
    if not set(conditions) <= {row["condition"] for row in rows}:
        return
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.figure(figsize=(6.4, 4.2))
    for condition, label, marker in (
        ("full_audio", "audio replay", "o"),
        ("transcript_only", "transcript", "s"),
    ):
        means, lows, highs = [], [], []
        for bucket in BUCKETS:
            group = [
                row
                for row in rows
                if row["condition"] == condition and row["bucket"] == bucket
            ]
            values = [
                {
                    **row,
                    "_belief": bool(
                        row["belief_checkpoints"]["post_observation"]["evaluation"][
                            "all_correct"
                        ]
                    ),
                }
                for row in group
            ]
            mean = _mean(row["_belief"] for row in values)
            low, high = clustered_bootstrap_ci(values, "_belief")
            means.append(mean)
            lows.append(mean - low)
            highs.append(high - mean)
        plt.errorbar(
            BUCKETS,
            means,
            yerr=[lows, highs],
            fmt=f"{marker}-",
            capsize=3,
            label=label,
        )
    plt.ylim(0, 1.05)
    plt.xlabel("clue-to-gap turn-distance bucket")
    plt.ylabel("post-observation belief accuracy")
    plt.title("Immediate state resynchronization by modality")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    print(f"Modality belief curve -> {path}")


def prosody_summary_plot(rows: list[dict], path: Path) -> None:
    """Plot category-specific paired prosody adaptation with domain CIs."""

    stats = summarize_prosody(rows)
    if not stats.get("paired_n"):
        return
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    labels = list(stats["categories"])
    values = [stats["categories"][label]["both_correct"]["mean"] for label in labels]
    lows = [
        value - stats["categories"][label]["both_correct"]["ci"][0]
        for label, value in zip(labels, values)
    ]
    highs = [
        stats["categories"][label]["both_correct"]["ci"][1] - value
        for label, value in zip(labels, values)
    ]
    plt.figure(figsize=(6.4, 4.2))
    plt.bar(labels, values, yerr=[lows, highs], capsize=4)
    pair_chance = stats["both_style_random_chance"]
    plt.axhline(
        pair_chance,
        color="gray",
        linestyle=":",
        label=f"random pair chance ({pair_chance:.2%})",
    )
    plt.ylim(0, 1.05)
    plt.ylabel("both deliveries correct")
    plt.title("Selective prosody grounding by high-affect category")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    print(f"Prosody summary -> {path}")


def score_closed_loop(path: str | Path) -> None:
    """Run all closed-loop reports and write the retention plot."""

    rows = load(path)
    models = sorted({row["model"] for row in rows})
    print(f"Models: {', '.join(models)} | completed trajectories: {len(rows)}")
    condition_table(rows)
    belief_report(rows)
    paired_control_report(rows)
    failure_report(rows)
    output = Path(path).with_name(Path(path).stem + "_retention.png")
    retention_curve(rows, output)
    modality_belief_curve(
        rows,
        Path(path).with_name(Path(path).stem + "_modality_belief.png"),
    )
    prosody_summary_plot(
        rows,
        Path(path).with_name(Path(path).stem + "_prosody.png"),
    )


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "closed_loop":
        score_closed_loop(sys.argv[2])
    else:
        print(__doc__)
        print("Usage: python score.py closed_loop results/fake_closed_loop.jsonl")
