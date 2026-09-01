from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from benchmark_core import AgentManifest, AgentSpecification, RunRegistry, execute_run


class OneStepEnvironment:
    def reset(self, seed: int) -> int:
        return seed

    def step(self, action: int) -> tuple[int, float, bool, bool, dict[str, object]]:
        return action, 2.5, True, False, {}


class OneStepAgent:
    def reset(self, specification: AgentSpecification) -> None:
        pass

    def observe(self, observation: object) -> None:
        pass

    def act(self) -> int:
        return 7

    def learn(self, transition: object) -> None:
        pass

    def save(self) -> None:
        return None

    def load(self, state: object) -> None:
        pass


class RunTests(unittest.TestCase):
    def test_execute_run_persists_artifacts_and_registry_record(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            registry_path = root / "registry.jsonl"
            status = execute_run(
                OneStepAgent,
                OneStepEnvironment(),
                AgentSpecification("observation", "action", 11),
                AgentManifest("1", "baseline", "1"),
                run_id="run-1",
                benchmark_version="0.1",
                scenario="one-step",
                artifact_root=root / "artifacts",
                registry=RunRegistry(registry_path),
                config={"max_steps": 1},
                max_steps=1,
            )
            self.assertEqual(status, "PASS")
            episode = json.loads((root / "artifacts" / "run-1" / "raw" / "episode_result.json").read_text())
            self.assertEqual(episode["total_reward"], 2.5)
            self.assertEqual(episode["steps_detail"][0]["reward"], 2.5)
            run_metadata = json.loads(
                (root / "artifacts" / "run-1" / "manifest" / "run_metadata.json").read_text()
            )
            self.assertEqual(run_metadata["run_id"], "run-1")
            self.assertEqual(len(run_metadata["benchmark_code_hash"]), 64)
            metrics = json.loads(
                (root / "artifacts" / "run-1" / "metrics" / "episode_metrics.json").read_text()
            )
            self.assertEqual(metrics["total_reward"], 2.5)
            self.assertTrue((root / "artifacts" / "run-1" / "logs" / "execution.json").exists())
            self.assertEqual(len(registry_path.read_text(encoding="utf-8").splitlines()), 1)


if __name__ == "__main__":
    unittest.main()
