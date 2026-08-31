from __future__ import annotations

from math import nan
import unittest

from benchmark_core import (
    AgentCapabilities,
    AgentManifest,
    AgentProtocolError,
    AgentSpecification,
    check_determinism,
    validate_agent,
)


class MinimalAgent:
    def __init__(self) -> None:
        self.loaded = False

    def reset(self, specification: AgentSpecification) -> None:
        self.specification = specification

    def observe(self, observation: object) -> None:
        self.observation = observation

    def act(self) -> int:
        return 0

    def learn(self, transition: object) -> None:
        pass

    def save(self) -> dict[str, bool]:
        return {"loaded": self.loaded}

    def load(self, state: dict[str, bool]) -> None:
        self.loaded = state["loaded"]


class IncompleteAgent:
    def reset(self, specification: AgentSpecification) -> None:
        pass


class ProtocolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.specification = AgentSpecification(
            observation_space="opaque-observation-space",
            action_space="opaque-action-space",
            seed=7,
        )

    def test_minimal_agent_passes_without_optional_persistence(self) -> None:
        validate_agent(MinimalAgent(), self.specification)

    def test_persistence_capability_executes_save_and_load(self) -> None:
        specification = AgentSpecification(
            observation_space="observation",
            action_space="action",
            seed=7,
            capabilities=AgentCapabilities(persistence=True),
        )
        validate_agent(MinimalAgent(), specification)

    def test_incomplete_agent_is_rejected(self) -> None:
        with self.assertRaisesRegex(AgentProtocolError, "missing protocol methods"):
            validate_agent(IncompleteAgent(), self.specification)  # type: ignore[arg-type]

    def test_invalid_seed_is_rejected(self) -> None:
        specification = AgentSpecification("observation", "action", -1)
        with self.assertRaisesRegex(AgentProtocolError, "non-negative"):
            validate_agent(MinimalAgent(), specification)

    def test_manifest_serializes_auditable_metadata(self) -> None:
        manifest = AgentManifest("1", "baseline", "0.1", entrypoint="tests.test_protocol.MinimalAgent")
        self.assertEqual(manifest.to_dict()["agent_id"], "baseline")

    def test_manifest_rejects_non_finite_timeout(self) -> None:
        manifest = AgentManifest("1", "baseline", "0.1", declared_timeout_seconds=nan)
        with self.assertRaisesRegex(AgentProtocolError, "timeout"):
            manifest.validate()

    def test_determinism_check_accepts_same_seed_and_observation(self) -> None:
        check_determinism(MinimalAgent, self.specification, {"value": 1})


if __name__ == "__main__":
    unittest.main()
