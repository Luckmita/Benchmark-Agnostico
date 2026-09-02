from __future__ import annotations

import time
import unittest

from benchmark_core import AgentCapabilities, AgentManifest, AgentSpecification, run_episode


class CounterEnvironment:
    def reset(self, seed: int) -> int:
        self.steps = 0
        return 0

    def step(self, action: int) -> tuple[int, float, bool, bool, dict[str, object]]:
        self.steps += 1
        return self.steps, float(action), self.steps >= 3, False, {}


class StatefulAgent:
    def __init__(self) -> None:
        self.value = 0

    def reset(self, specification: AgentSpecification) -> None:
        self.value = 0

    def observe(self, observation: int) -> None:
        self.observation = observation

    def act(self) -> int:
        return self.value

    def learn(self, transition: object) -> None:
        self.value += 1

    def save(self) -> int:
        return self.value

    def load(self, state: int) -> None:
        self.value = state


class SlowEnvironment(CounterEnvironment):
    def step(self, action: int) -> tuple[int, float, bool, bool, dict[str, object]]:
        time.sleep(0.2)
        return super().step(action)


class InvalidAfterOneEnvironment(CounterEnvironment):
    def step(self, action: int) -> tuple[int, float, bool, bool, dict[str, object]]:
        if getattr(self, "steps", 0) >= 1:
            raise ValueError("second action invalid")
        return super().step(action)


def reject_action(action: object) -> None:
    raise ValueError("invalid")


class EpisodeTests(unittest.TestCase):
    def test_online_learning_preserves_agent_state_in_episode(self) -> None:
        specification = AgentSpecification(
            "observation",
            "action",
            1,
            AgentCapabilities(online_learning=True),
        )
        capabilities = specification.capabilities
        result = run_episode(
            StatefulAgent,
            CounterEnvironment(),
            specification,
            AgentManifest("1", "stateful", "1", capabilities=capabilities, declared_timeout_seconds=1),
            max_steps=5,
        )
        self.assertEqual(result.status, "PASS")
        self.assertEqual([item.action for item in result.action_results], [0, 1, 2])
        self.assertEqual(result.total_reward, 3.0)

    def test_action_validator_rejects_invalid_action(self) -> None:
        result = run_episode(
            StatefulAgent,
            CounterEnvironment(),
            AgentSpecification("observation", "action", 1),
            AgentManifest("1", "stateful", "1"),
            max_steps=3,
            action_validator=reject_action,
        )
        self.assertEqual(result.status, "INVALID_ACTION")

    def test_episode_timeout_is_hard(self) -> None:
        result = run_episode(
            StatefulAgent,
            SlowEnvironment(),
            AgentSpecification("observation", "action", 1),
            AgentManifest("1", "slow", "1", declared_timeout_seconds=0.02),
            max_steps=3,
        )
        self.assertEqual(result.status, "TIMEOUT")

    def test_invalid_action_preserves_completed_raw_steps(self) -> None:
        result = run_episode(
            StatefulAgent,
            InvalidAfterOneEnvironment(),
            AgentSpecification("observation", "action", 1),
            AgentManifest("1", "partial", "1"),
            max_steps=3,
        )
        self.assertEqual(result.status, "INVALID_ACTION")
        self.assertEqual(result.steps, 1)
        self.assertEqual(result.total_reward, 0.0)
        self.assertEqual(len(result.action_results), 1)
        self.assertEqual(result.action_results[0].observation, 0)
        self.assertEqual(result.action_results[0].next_observation, 1)


if __name__ == "__main__":
    unittest.main()
