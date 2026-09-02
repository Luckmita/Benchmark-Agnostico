from __future__ import annotations

import unittest

from benchmark_core import AgentCapabilities, AgentManifest, AgentSpecification, run_episode
from benchmark_core.tasks import C1BanditConfig, C1BanditEnvironment, EpsilonGreedyAgent, RandomAgent


class C1LearningTests(unittest.TestCase):
    def setUp(self) -> None:
        self.capabilities = AgentCapabilities(online_learning=True)
        self.manifest = AgentManifest(
            "1", "c1-development", "0.1", capabilities=self.capabilities, declared_timeout_seconds=2
        )
        self.specification = AgentSpecification(
            observation_space="constant",
            action_space="{0,1}",
            seed=17,
            capabilities=self.capabilities,
        )

    def test_environment_is_reproducible_after_reset(self) -> None:
        environment = C1BanditEnvironment(C1BanditConfig(max_steps=5))
        environment.reset(17)
        first = [environment.step(1)[1] for _ in range(5)]
        environment.reset(17)
        second = [environment.step(1)[1] for _ in range(5)]
        self.assertEqual(first, second)

    def test_environment_rejects_invalid_action(self) -> None:
        environment = C1BanditEnvironment()
        environment.reset(1)
        with self.assertRaises(ValueError):
            environment.step(2)

    def test_epsilon_greedy_beats_random_on_development_task(self) -> None:
        config = C1BanditConfig(max_steps=100)
        learning = run_episode(
            EpsilonGreedyAgent,
            C1BanditEnvironment(config),
            self.specification,
            self.manifest,
            max_steps=config.max_steps,
        )
        random_result = run_episode(
            RandomAgent,
            C1BanditEnvironment(config),
            self.specification,
            AgentManifest("1", "random", "0.1", capabilities=self.capabilities, declared_timeout_seconds=2),
            max_steps=config.max_steps,
        )
        self.assertEqual(learning.status, "PASS")
        self.assertEqual(random_result.status, "PASS")
        self.assertGreater(learning.total_reward, random_result.total_reward)


if __name__ == "__main__":
    unittest.main()
