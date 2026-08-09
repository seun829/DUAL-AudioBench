"""Contract tests applied to every registered domain.

These are deliberately generic rather than per-domain: a newly added template is
covered automatically, so a domain cannot ship with an unreachable observation
or an answer that is missing from its own menu.

For each domain and every combination of pre-gap action, hidden user action, and
external event, the suite asserts that the environment is deterministic, that the
reached hidden state is declared in the belief schema, that a resumed observation
exists, and that the state-derived correct action is actually presented.
"""

from __future__ import annotations

import itertools
import unittest

from dual_audio.core.environment import (
    correct_action,
    execute_action,
    post_gap_observation,
    transition,
)
from scenarios.generate import build
from scenarios.templates import TEMPLATES


def _one_task_per_domain() -> dict[str, dict]:
    """Build one representative scenario for each registered domain."""

    tasks = {}
    for name, template in TEMPLATES.items():
        tasks[template["domain"]] = build(name, "5-8", 0)
    return tasks


TASKS = _one_task_per_domain()


class DomainContractTests(unittest.TestCase):
    def test_every_domain_is_registered_once(self):
        domains = [template["domain"] for template in TEMPLATES.values()]
        self.assertEqual(len(domains), len(set(domains)), "duplicate domain name")
        self.assertGreaterEqual(len(domains), 10)

    def test_reachable_states_are_scorable_and_deterministic(self):
        for domain, task in sorted(TASKS.items()):
            menu = {item["action"] for item in task["post_gap_actions"]}
            variable = next(iter(task["belief_schema"]))
            allowed = task["belief_schema"][variable]
            options = [item["action"] for item in task["pre_gap_actions"]]
            elapsed = task["transition"]["elapsed_minutes"]

            for action, with_user, with_event in itertools.product(
                options, (False, True), (False, True)
            ):
                with self.subTest(domain=domain, action=action,
                                  user=with_user, event=with_event):
                    event = task["transition"]["external_event"] if with_event else None
                    user = task["transition"]["user_action"] if with_user else None

                    def run():
                        return transition(
                            domain,
                            execute_action(domain, task["initial_state"], action),
                            action,
                            elapsed,
                            event,
                            user,
                        )

                    state = run()
                    self.assertEqual(state, run(), "transition is not deterministic")
                    self.assertIn(
                        state[variable], allowed, "state left the declared belief schema"
                    )
                    self.assertIn(
                        correct_action(domain, state),
                        menu,
                        "state-derived answer is missing from the presented menu",
                    )
                    observation = post_gap_observation(domain, state)
                    self.assertTrue(
                        observation and isinstance(observation, str),
                        "reached state has no resumed observation",
                    )

    def test_pre_gap_action_changes_the_resulting_world(self):
        """A wrong pre-gap choice must not converge to the correct outcome."""

        for domain, task in sorted(TASKS.items()):
            with self.subTest(domain=domain):
                event = task["transition"]["external_event"]
                elapsed = task["transition"]["elapsed_minutes"]
                right = task["pre_gap"]["correct_action"]
                baseline = transition(
                    domain,
                    execute_action(domain, task["initial_state"], right),
                    right,
                    elapsed,
                    event,
                    None,
                )
                for wrong in [
                    item["action"]
                    for item in task["pre_gap_actions"]
                    if item["action"] != right
                ]:
                    other = transition(
                        domain,
                        execute_action(domain, task["initial_state"], wrong),
                        wrong,
                        elapsed,
                        event,
                        None,
                    )
                    self.assertNotEqual(
                        baseline, other, f"{domain}: {wrong} produced the correct world"
                    )

    def test_hidden_user_action_is_a_real_transition_input(self):
        for domain, task in sorted(TASKS.items()):
            with self.subTest(domain=domain):
                right = task["pre_gap"]["correct_action"]
                elapsed = task["transition"]["elapsed_minutes"]
                event = task["transition"]["external_event"]
                start = execute_action(domain, task["initial_state"], right)
                without = transition(domain, start, right, elapsed, event, None)
                with_user = transition(
                    domain, start, right, elapsed, event, task["transition"]["user_action"]
                )
                self.assertNotEqual(
                    without, with_user, "hidden user action had no effect on the world"
                )
                self.assertTrue(post_gap_observation(domain, with_user))

    def test_generated_scenarios_hold_their_invariants(self):
        """Alternation, distance, and menu size for every domain and bucket."""

        for name in TEMPLATES:
            for bucket in ("1-2", "5-8", "12-20"):
                with self.subTest(template=name, bucket=bucket):
                    task = build(name, bucket, 0)
                    turns = task["turns"]
                    for index, turn in enumerate(turns):
                        self.assertEqual(
                            turn["speaker"], "user" if index % 2 == 0 else "agent"
                        )
                    clue = next(
                        i for i, t in enumerate(turns) if t["kind"] == "clue"
                    )
                    self.assertEqual(
                        task["clue_turn_distance"], len(turns) - clue - 1
                    )
                    self.assertEqual(len(task["pre_gap_actions"]), 5)
                    self.assertEqual(len(task["post_gap_actions"]), 5)
                    untagged = [
                        item
                        for item in task["post_gap_actions"]
                        if not item["failure_tags"]
                    ]
                    self.assertEqual(
                        len(untagged), 1, "exactly one post-gap option must be untagged"
                    )


if __name__ == "__main__":
    unittest.main()
