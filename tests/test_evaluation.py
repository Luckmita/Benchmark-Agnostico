from __future__ import annotations

import unittest

from benchmark_core import AgentCapabilities, AgentManifest, AgentSpecification, evaluate_agent
from benchmark_core.tasks import C1BanditConfig, C1BanditEnvironment, EpsilonGreedyAgent


class EvaluationTests(unittest.TestCase):
    def test_evaluation_preserves_seed_level_results(self) -> None:
        config = C1BanditConfig(max_steps=20)
        report = evaluate_agent(
            EpsilonGreedyAgent,
            lambda: C1BanditEnvironment(config),
            AgentSpecification("constant", "{0,1}", 0, AgentCapabilities(online_learning=True)),
            AgentManifest("1", "epsilon", "1", declared_timeout_seconds=2),
            seeds=[1, 2, 3],
            max_steps=config.max_steps,
        )
        self.assertEqual(report["seeds"], [1, 2, 3])
        self.assertEqual(len(report["returns"]), 3)
        self.assertEqual(report["summary"]["count"], 3)
        self.assertTrue(all(status == "PASS" for status in report["statuses"]))

    def test_empty_seed_list_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            evaluate_agent(
                EpsilonGreedyAgent,
                C1BanditEnvironment,
                AgentSpecification("constant", "{0,1}", 0),
                AgentManifest("1", "epsilon", "1"),
                seeds=[],
                max_steps=2,
            )


if __name__ == "__main__":
    unittest.main()
