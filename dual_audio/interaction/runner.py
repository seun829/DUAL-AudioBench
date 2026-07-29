from __future__ import annotations

import copy
import hashlib
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dual_audio.core.beliefs import (
    evaluate_state_belief,
    normalize_state_belief,
    probability_of,
    top_state_assignment,
)
from dual_audio.core.conditions import Condition, condition_turns, prosody_for
from dual_audio.core.environment import (
    correct_action,
    execute_action,
    execute_user_action,
    transition,
)
from dual_audio.core.types import AgentResponse, Observation
from dual_audio.users.scripted import ScriptedUserSimulator


def _stable_rng(*parts: object) -> random.Random:
    value = hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()
    return random.Random(value)


def _menu(
    task: dict,
    stage: str,
    seed: int,
) -> tuple[tuple[dict[str, str], ...], dict[str, str]]:
    """Build a paired, randomized public menu.

    The condition is intentionally absent from the seed, so clue-ablation and
    control runs receive exactly the same menu and option order.
    """

    actions = copy.deepcopy(task[f"{stage}_actions"])
    _stable_rng(task["scenario_id"], stage, seed).shuffle(actions)
    labels = [chr(ord("A") + i) for i in range(len(actions))]
    public = tuple(
        {"label": label, "description": action["description"]}
        for label, action in zip(labels, actions)
    )
    return public, {
        label: action["action"] for label, action in zip(labels, actions)
    }


def _style_menu(
    task: dict, seed: int
) -> tuple[tuple[dict[str, str], ...], dict[str, str]]:
    styles = copy.deepcopy(task["response_styles"])
    _stable_rng(task["scenario_id"], "style", seed).shuffle(styles)
    labels = [chr(ord("X") + i) for i in range(len(styles))]
    public = tuple(
        {"label": label, "description": style["description"]}
        for label, style in zip(labels, styles)
    )
    return public, {
        label: style["style"] for label, style in zip(labels, styles)
    }


def _failure_tags(task: dict, stage: str, action: str | None) -> list[str]:
    if action is None:
        return ["OFF_MENU_RESPONSE"]
    for item in task[f"{stage}_actions"]:
        if item["action"] == action:
            return list(item.get("failure_tags", []))
    return ["OFF_MENU_RESPONSE"]


def _belief_checkpoint(
    task: dict,
    state: dict[str, Any],
    response: AgentResponse,
    selected_action: str | None = None,
    expected_action: str | None = None,
) -> dict[str, Any]:
    """Evaluate one explicit belief report and its optional action coupling."""

    schema = {
        variable: tuple(values)
        for variable, values in task["belief_schema"].items()
    }
    belief = normalize_state_belief(response.state_belief, schema)
    evaluation = evaluate_state_belief(belief, schema, state)
    assignments = top_state_assignment(evaluation)
    implied_action = None
    if len(assignments) == len(schema):
        hypothetical = copy.deepcopy(state)
        hypothetical.update(assignments)
        implied_action = correct_action(task["domain"], hypothetical)

    confidence = evaluation["mean_confidence"]
    threshold = task["belief_confidence_threshold"]
    low_confidence = confidence is None or confidence < threshold
    revalidation_action = (
        selected_action in task["revalidation_actions"]
        if selected_action is not None
        else None
    )
    action_correct = (
        selected_action == expected_action if expected_action is not None else None
    )
    action_belief_consistent = (
        selected_action == implied_action
        if selected_action is not None and implied_action is not None
        else None
    )
    outcome = None
    if action_correct is not None:
        if evaluation["all_correct"] and action_correct:
            outcome = "FULL_SUCCESS"
        elif evaluation["all_correct"] and not action_correct:
            outcome = "ACTION_SELECTION_FAILURE"
        elif not evaluation["all_correct"] and action_correct:
            outcome = "LUCKY_ACTION"
        else:
            outcome = "STATE_SYNCHRONIZATION_FAILURE"

    if low_confidence and selected_action is not None:
        uncertainty_behavior = (
            "UNCERTAIN_RECHECKED"
            if revalidation_action
            else "UNCERTAIN_ACTED"
        )
    elif low_confidence:
        uncertainty_behavior = "UNCERTAIN_BELIEF_REPORTED"
    else:
        uncertainty_behavior = "CONFIDENT"

    return {
        "state_belief": belief,
        "needs_revalidation": response.needs_revalidation,
        "report_valid": (
            evaluation["valid"]
            and isinstance(response.needs_revalidation, bool)
        ),
        "evaluation": evaluation,
        "low_confidence": low_confidence,
        "confidence_threshold": threshold,
        "risk_calibration_consistent": (
            response.needs_revalidation == low_confidence
            if isinstance(response.needs_revalidation, bool)
            else False
        ),
        "selected_action": selected_action,
        "expected_action": expected_action,
        "implied_action_from_top_belief": implied_action,
        "action_belief_consistent": action_belief_consistent,
        "action_correct": action_correct,
        "revalidation_action": revalidation_action,
        "uncertainty_behavior": uncertainty_behavior,
        "belief_action_outcome": outcome,
    }


def _belief_revision(
    task: dict,
    state_before: dict[str, Any],
    state_after: dict[str, Any],
    before_checkpoint: dict[str, Any],
    after_checkpoint: dict[str, Any],
    final_checkpoint: dict[str, Any],
) -> dict[str, Any]:
    """Measure evidence-driven revision, stale mass, and reflection-only change."""

    variables = {}
    for variable in task["belief_schema"]:
        old_value = str(state_before[variable])
        new_value = str(state_after[variable])
        before_belief = before_checkpoint["state_belief"]
        after_belief = after_checkpoint["state_belief"]
        final_belief = final_checkpoint["state_belief"]
        changed = old_value != new_value
        variables[variable] = {
            "old_state": old_value,
            "new_state": new_value,
            "state_changed": changed,
            "probability_new_state_before_gap": probability_of(
                before_belief, variable, new_value
            ),
            "probability_new_state_after_observation": probability_of(
                after_belief, variable, new_value
            ),
            "probability_new_state_before_final_action": probability_of(
                final_belief, variable, new_value
            ),
            "belief_revision_gain": (
                probability_of(after_belief, variable, new_value)
                - probability_of(before_belief, variable, new_value)
            ),
            "final_revision_gain": (
                probability_of(final_belief, variable, new_value)
                - probability_of(before_belief, variable, new_value)
            ),
            "reflection_gain": (
                probability_of(final_belief, variable, new_value)
                - probability_of(after_belief, variable, new_value)
            ),
            "stale_belief_persistence": (
                probability_of(after_belief, variable, old_value)
                if changed
                else None
            ),
        }

    changed_rows = [row for row in variables.values() if row["state_changed"]]
    return {
        "variables": variables,
        "mean_revision_gain": (
            sum(row["belief_revision_gain"] for row in changed_rows)
            / len(changed_rows)
            if changed_rows
            else None
        ),
        "mean_final_revision_gain": (
            sum(row["final_revision_gain"] for row in changed_rows)
            / len(changed_rows)
            if changed_rows
            else None
        ),
        "mean_stale_belief_persistence": (
            sum(row["stale_belief_persistence"] for row in changed_rows)
            / len(changed_rows)
            if changed_rows
            else None
        ),
    }


class ClosedLoopRunner:
    """Execute and record one complete alternating-turn benchmark trajectory.

    The runner owns orchestration only. Task meaning comes from scenario JSON,
    state mechanics come from ``core.environment``, user language comes from
    the user simulator, and model behavior comes through ``Agent.respond``.
    """

    def __init__(self, user_simulator=None, audio_renderer=None):
        self.user = user_simulator or ScriptedUserSimulator()
        self.audio_renderer = audio_renderer

    def _audio(
        self,
        text: str,
        speaker: str,
        prosody: str,
        modality: str,
    ) -> Path | None:
        """Render a turn unless this is a transcript condition or dry run."""

        if modality == "transcript" or self.audio_renderer is None:
            return None
        return self.audio_renderer.render(text, speaker, prosody)

    def _append_agent_turn(
        self,
        history: list[dict],
        response: AgentResponse,
        fallback_text: str,
        modality: str,
    ) -> None:
        """Append evaluated-agent text and optional synthesized replay audio."""

        text = response.message.strip() if response.message else fallback_text
        audio = self._audio(text, "agent", "neutral", modality)
        history.append(
            {
                "role": "agent",
                "text": text,
                "audio_path": str(audio) if audio else None,
                "action_label": response.action,
                "response_style_label": response.response_style,
            }
        )

    def execute(
        self,
        agent,
        task: dict[str, Any],
        condition: Condition,
        seed: int,
    ) -> dict[str, Any]:
        """Run a task/condition/seed and return its auditable trajectory.

        Menu order is paired across conditions, the selected pre-gap action is
        executed before time advances, and the expected post-gap action is
        derived from the resulting state rather than copied from task metadata.
        """

        state_initial = copy.deepcopy(task["initial_state"])
        state = copy.deepcopy(state_initial)
        history: list[dict] = []
        calls: list[dict] = []
        belief_schema = {
            variable: tuple(values)
            for variable, values in task["belief_schema"].items()
        }
        belief_state_space_size = 1
        for values in belief_schema.values():
            belief_state_space_size *= len(values)
        pre_turns = self.user.pre_gap_turns(task, condition)
        mock_bucket = "1-2" if condition.name == "state_change_short" else task["bucket"]

        if not pre_turns or pre_turns[0]["speaker"] != "user":
            raise ValueError(f"{task['scenario_id']} must start with a user turn")
        if pre_turns[-1]["speaker"] != "user":
            raise ValueError(f"{task['scenario_id']} must reach the action after a user turn")

        pre_menu, pre_map = _menu(task, "pre_gap", seed)
        expected_pre = task["pre_gap"]["correct_action"]
        expected_pre_label = next(
            label for label, action in pre_map.items() if action == expected_pre
        )

        # Every scripted user turn is answered by the evaluated agent. Scripted
        # agent text is only a dialogue-intent constraint, never played as audio.
        i = 0
        while i < len(pre_turns):
            user_turn = pre_turns[i]
            is_checkpoint = i == len(pre_turns) - 1
            guidance = ""
            if not is_checkpoint:
                next_turn = pre_turns[i + 1]
                if next_turn["speaker"] != "agent":
                    raise ValueError(
                        f"{task['scenario_id']} is not alternating at turn {i + 1}"
                    )
                guidance = next_turn["text"]

            user_audio = self._audio(
                user_turn["text"], "user", "neutral", condition.modality
            )
            history.append(
                {
                    "role": "user",
                    "text": user_turn["text"],
                    "kind": user_turn.get("kind"),
                    "audio_path": str(user_audio) if user_audio else None,
                }
            )
            stage = "pre_gap" if is_checkpoint else "dialogue"
            observation = Observation(
                text=user_turn["text"],
                audio_path=user_audio,
                modality=condition.modality,
                stage=stage,
                instruction=guidance,
                action_menu=pre_menu if is_checkpoint else (),
                belief_schema=belief_schema if is_checkpoint else {},
                private={
                    "scenario_id": task["scenario_id"],
                    "condition": condition.name,
                    "seed": seed,
                    "bucket": mock_bucket,
                    "expected_action_label": expected_pre_label,
                    "belief_targets": {
                        variable: state[variable] for variable in belief_schema
                    },
                },
            )
            response = agent.respond(observation, history[:-1])
            calls.append(
                {
                    "stage": stage,
                    "raw": response.raw,
                    "action_label": response.action,
                    "state_belief": response.state_belief,
                    "needs_revalidation": response.needs_revalidation,
                }
            )
            public_description = next(
                (
                    item["description"]
                    for item in pre_menu
                    if item["label"] == response.action
                ),
                "review the available options",
            )
            fallback = (
                f"I will {public_description}"
                if is_checkpoint
                else guidance
            )
            self._append_agent_turn(
                history, response, fallback, condition.modality
            )
            if is_checkpoint:
                pre_response = response
                break
            i += 2

        selected_pre = pre_map.get(pre_response.action)
        pre_belief_checkpoint = _belief_checkpoint(
            task=task,
            state=state,
            response=pre_response,
            selected_action=selected_pre,
            expected_action=expected_pre,
        )
        # An invalid selection is a no-op tool call but remains visible in the log.
        if selected_pre is not None:
            state = execute_action(task["domain"], state, selected_pre)
        state_before_gap = copy.deepcopy(state)

        acknowledgement = self.user.acknowledgement(task, condition)
        acknowledgement_audio = self._audio(
            acknowledgement["text"], "user", "neutral", condition.modality
        )
        history.append(
            {
                "role": "user",
                "text": acknowledgement["text"],
                "kind": acknowledgement.get("kind"),
                "audio_path": (
                    str(acknowledgement_audio) if acknowledgement_audio else None
                ),
            }
        )

        external_event = (
            task["transition"]["external_event"]
            if condition.apply_external_event
            else None
        )
        gap_user_action = (
            task["transition"].get("user_action")
            if condition.apply_user_action
            else None
        )
        state_after_user_action = execute_user_action(
            task["domain"],
            state,
            gap_user_action,
        )
        state_after_gap = transition(
            domain=task["domain"],
            current_state=state,
            agent_action=selected_pre or "invalid_action",
            elapsed_minutes=task["transition"]["elapsed_minutes"],
            external_event=external_event,
            user_action=gap_user_action,
        )

        post_text = self.user.post_gap(task, state_after_gap)
        post_prosody, expected_style = prosody_for(task, condition)
        post_audio = self._audio(
            post_text, "user", post_prosody, condition.modality
        )
        post_menu, post_map = _menu(task, "post_gap", seed)
        expected_post = correct_action(task["domain"], state_after_gap)
        expected_post_label = next(
            label for label, action in post_map.items() if action == expected_post
        )

        style_menu: tuple[dict[str, str], ...] = ()
        style_map: dict[str, str] = {}
        expected_style_label = None
        if condition.score_style:
            style_menu, style_map = _style_menu(task, seed)
            expected_style_label = next(
                label for label, style in style_map.items() if style == expected_style
            )

        belief_observation = Observation(
            text=post_text,
            audio_path=post_audio,
            modality=condition.modality,
            stage="post_gap_belief",
            belief_schema=belief_schema,
            private={
                "scenario_id": task["scenario_id"],
                "condition": condition.name,
                "seed": seed,
                "bucket": mock_bucket,
                "belief_targets": {
                    variable: state_after_gap[variable]
                    for variable in belief_schema
                },
            },
        )
        resumed_belief_response = agent.respond(belief_observation, history)
        calls.append(
            {
                "stage": "post_gap_belief",
                "raw": resumed_belief_response.raw,
                "state_belief": resumed_belief_response.state_belief,
                "needs_revalidation": resumed_belief_response.needs_revalidation,
            }
        )
        history.append(
            {
                "role": "user",
                "text": post_text,
                "kind": "post_gap_observation",
                "audio_path": str(post_audio) if post_audio else None,
                "prosody": post_prosody,
            }
        )
        resumed_belief_checkpoint = _belief_checkpoint(
            task=task,
            state=state_after_gap,
            response=resumed_belief_response,
        )

        # The final decision is a separate introspection checkpoint. There is no
        # new user evidence: audio replay/history already contains the resumed
        # utterance exactly once.
        final_observation = Observation(
            text="",
            audio_path=None,
            modality=condition.modality,
            stage="post_gap",
            action_menu=post_menu,
            style_menu=style_menu,
            belief_schema=belief_schema,
            prior_state_belief=resumed_belief_response.state_belief,
            private={
                "scenario_id": task["scenario_id"],
                "condition": condition.name,
                "seed": seed,
                "bucket": mock_bucket,
                "expected_action_label": expected_post_label,
                "expected_style_label": expected_style_label,
                "belief_targets": {
                    variable: state_after_gap[variable]
                    for variable in belief_schema
                },
            },
        )
        post_response = agent.respond(final_observation, history)
        calls.append(
            {
                "stage": "post_gap",
                "raw": post_response.raw,
                "action_label": post_response.action,
                "response_style_label": post_response.response_style,
                "state_belief": post_response.state_belief,
                "needs_revalidation": post_response.needs_revalidation,
            }
        )
        selected_post = post_map.get(post_response.action)
        selected_style = style_map.get(post_response.response_style)
        final_belief_checkpoint = _belief_checkpoint(
            task=task,
            state=state_after_gap,
            response=post_response,
            selected_action=selected_post,
            expected_action=expected_post,
        )
        public_post_description = next(
            (
                item["description"]
                for item in post_menu
                if item["label"] == post_response.action
            ),
            "review the available options",
        )
        post_fallback = f"I will {public_post_description}"
        self._append_agent_turn(
            history, post_response, post_fallback, condition.modality
        )
        if selected_post is not None:
            state_final = execute_action(
                task["domain"], state_after_gap, selected_post
            )
        else:
            state_final = copy.deepcopy(state_after_gap)

        pre_ok = selected_pre == expected_pre
        post_ok = selected_post == expected_post
        style_ok = (
            selected_style == expected_style if condition.score_style else None
        )
        belief_reporting_ok = all(
            checkpoint["report_valid"]
            for checkpoint in (
                pre_belief_checkpoint,
                resumed_belief_checkpoint,
                final_belief_checkpoint,
            )
        )
        belief_state_ok = all(
            checkpoint["evaluation"]["all_correct"]
            for checkpoint in (
                pre_belief_checkpoint,
                resumed_belief_checkpoint,
                final_belief_checkpoint,
            )
        )
        action_trajectory_ok = pre_ok and post_ok and (style_ok is not False)
        trajectory_ok = (
            action_trajectory_ok and belief_reporting_ok and belief_state_ok
        )
        belief_revision = _belief_revision(
            task=task,
            state_before=state_initial,
            state_after=state_after_gap,
            before_checkpoint=pre_belief_checkpoint,
            after_checkpoint=resumed_belief_checkpoint,
            final_checkpoint=final_belief_checkpoint,
        )
        presented_turns = condition_turns(task, condition)
        clue_index = next(
            (
                i
                for i, turn in enumerate(presented_turns)
                if turn.get("kind") in {"clue", "clue_ablation"}
            ),
            None,
        )
        effective_distance = (
            len(presented_turns) - clue_index - 1
            if clue_index is not None
            else None
        )
        return {
            "schema_version": "0.3",
            "scenario_id": task["scenario_id"],
            "domain": task["domain"],
            "bucket": task["bucket"],
            "clue_turn_distance": task["clue_turn_distance"],
            "effective_clue_turn_distance": effective_distance,
            "condition": condition.name,
            "seed": seed,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "initial_state": state_initial,
            "pre_gap_action": selected_pre,
            "expected_pre_gap_action": expected_pre,
            "pre_gap_action_label": pre_response.action,
            "pre_gap_menu": list(pre_menu),
            "pre_gap_menu_size": len(pre_menu),
            "pre_gap_success": pre_ok,
            "state_before_gap": state_before_gap,
            "elapsed_minutes": task["transition"]["elapsed_minutes"],
            "external_event": external_event,
            "gap_user_action": gap_user_action,
            "state_after_user_action": state_after_user_action,
            "state_after_gap": state_after_gap,
            "post_gap_observation": post_text,
            "post_gap_prosody": post_prosody,
            "post_gap_action": selected_post,
            "expected_post_gap_action": expected_post,
            "post_gap_action_label": post_response.action,
            "post_gap_menu": list(post_menu),
            "post_gap_menu_size": len(post_menu),
            "post_gap_success": post_ok,
            "response_style": selected_style,
            "expected_response_style": expected_style,
            "response_style_success": style_ok,
            "response_style_menu_size": len(style_menu) or 1,
            "belief_state_space_size": belief_state_space_size,
            "belief_checkpoint_chance": 1 / belief_state_space_size,
            "belief_checkpoints": {
                "pre_gap": pre_belief_checkpoint,
                "post_observation": resumed_belief_checkpoint,
                "pre_final_action": final_belief_checkpoint,
            },
            "belief_revision": belief_revision,
            "belief_reporting_success": belief_reporting_ok,
            "state_belief_success": belief_state_ok,
            "action_trajectory_success": action_trajectory_ok,
            "failure_tags": (
                []
                if trajectory_ok
                else sorted(
                    set(
                        ([] if pre_ok else _failure_tags(task, "pre_gap", selected_pre))
                        + (
                            []
                            if post_ok
                            else _failure_tags(task, "post_gap", selected_post)
                        )
                        + (
                            []
                            if style_ok is not False
                            else ["PROSODY_GROUNDING_FAILURE"]
                        )
                        + (
                            []
                            if belief_reporting_ok
                            else ["BELIEF_REPORT_INVALID"]
                        )
                        + (
                            []
                            if belief_state_ok
                            else ["STATE_BELIEF_ERROR"]
                        )
                    )
                )
            ),
            "trajectory_success": trajectory_ok,
            "final_state": state_final,
            "turns": history,
            "model_calls": calls,
        }
