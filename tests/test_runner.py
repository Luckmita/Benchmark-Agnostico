from __future__ import annotations

import time
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from benchmark_core import (
    AgentManifest,
    AgentSpecification,
    RunRegistry,
    RunRecord,
    hash_json,
    hash_paths,
    run_action,
)


class FastAgent:
    def reset(self, specification: AgentSpecification) -> None:
        pass

    def observe(self, observation: object) -> None:
        pass

    def act(self) -> int:
        return 3

    def learn(self, transition: object) -> None:
        pass

    def save(self) -> None:
        return None

    def load(self, state: object) -> None:
        pass


class SlowAgent(FastAgent):
    def act(self) -> int:
        time.sleep(0.25)
        return 4


class RunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.specification = AgentSpecification("observation", "action", 1)

    def test_fast_action_passes(self) -> None:
        result = run_action(FastAgent, self.specification, AgentManifest("1", "fast", "1", declared_timeout_seconds=1), {})
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.action, 3)

    def test_slow_action_is_terminated(self) -> None:
        result = run_action(SlowAgent, self.specification, AgentManifest("1", "slow", "1", declared_timeout_seconds=0.02), {})
        self.assertEqual(result.status, "TIMEOUT")

    def test_registry_is_append_only_and_hash_is_stable(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "registry.jsonl"
            registry = RunRegistry(path)
            self.assertEqual(hash_json({"b": 2, "a": 1}), hash_json({"a": 1, "b": 2}))
            registry.append(RunRecord.create(
                run_id="run-1",
                benchmark_version="0.1",
                environment="test",
                scenario="scenario",
                seed=1,
                submission="fast",
                model_hash="model",
                adapter_hash="adapter",
                config_hash="config",
                hardware="cpu",
                software="python",
                status="PASS",
            ))
            registry.append(RunRecord.create(
                run_id="run-2",
                benchmark_version="0.1",
                environment="test",
                scenario="scenario",
                seed=2,
                submission="fast",
                model_hash="model",
                adapter_hash="adapter",
                config_hash="config",
                hardware="cpu",
                software="python",
                status="TIMEOUT",
            ))
            self.assertEqual(len(path.read_text(encoding="utf-8").splitlines()), 2)
            self.assertTrue(path.parent.exists())

    def test_hash_paths_includes_relative_names_and_contents(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            left = root / "left.txt"
            right = root / "right.txt"
            left.write_text("same", encoding="utf-8")
            right.write_text("same", encoding="utf-8")
            self.assertNotEqual(hash_paths([left], base=root), hash_paths([right], base=root))


if __name__ == "__main__":
    unittest.main()
