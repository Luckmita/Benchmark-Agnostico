from __future__ import annotations

import json
from math import nan
import unittest

from benchmark_core import (
    AgentCapabilities,
    AgentManifest,
    AgentProtocolError,
    AgentSpecification,
    check_determinism,
    validate_agent,
    validate_contract,
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


class NonSerializablePersistenceAgent(MinimalAgent):
    def save(self) -> object:
        return lambda: None


class FixedActionAgent(MinimalAgent):
    def __init__(self, action: int) -> None:
        super().__init__()
        self.action = action

    def act(self) -> int:
        return self.action


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

    def test_persistence_state_must_be_serializable(self) -> None:
        specification = AgentSpecification(
            "observation",
            "action",
            7,
            AgentCapabilities(persistence=True),
        )
        with self.assertRaisesRegex(AgentProtocolError, "serializable"):
            validate_agent(NonSerializablePersistenceAgent(), specification)

    def test_incomplete_agent_is_rejected(self) -> None:
        with self.assertRaisesRegex(AgentProtocolError, "missing protocol methods"):
            validate_agent(IncompleteAgent(), self.specification)  # type: ignore[arg-type]

    def test_invalid_seed_is_rejected(self) -> None:
        specification = AgentSpecification("observation", "action", -1)
        with self.assertRaisesRegex(AgentProtocolError, "non-negative"):
            validate_agent(MinimalAgent(), specification)

    def test_capability_values_must_be_boolean(self) -> None:
        specification = AgentSpecification(
            "observation",
            "action",
            1,
            AgentCapabilities(online_learning="yes"),  # type: ignore[arg-type]
        )
        with self.assertRaisesRegex(AgentProtocolError, "must be boolean"):
            validate_agent(MinimalAgent(), specification)

    def test_manifest_serializes_auditable_metadata(self) -> None:
        manifest = AgentManifest("1", "baseline", "0.1", entrypoint="tests.test_protocol.MinimalAgent")
        self.assertEqual(manifest.to_dict()["agent_id"], "baseline")

    def test_manifest_rejects_non_finite_timeout(self) -> None:
        manifest = AgentManifest("1", "baseline", "0.1", declared_timeout_seconds=nan)
        with self.assertRaisesRegex(AgentProtocolError, "timeout"):
            manifest.validate()

    def test_manifest_rejects_untraceable_hash_format(self) -> None:
        manifest = AgentManifest("1", "baseline", "0.1", model_hash="abc123")
        with self.assertRaisesRegex(AgentProtocolError, "model_hash"):
            manifest.validate()

    def test_manifest_json_round_trip_is_strict(self) -> None:
        manifest = AgentManifest(
            "1",
            "baseline",
            "0.1",
            dependencies=("package==1.0",),
            training_provenance="public baseline",
        )
        loaded = AgentManifest.from_dict(json.loads(json.dumps(manifest.to_dict())))
        self.assertEqual(loaded, manifest)
        unknown = manifest.to_dict()
        unknown["extra"] = True
        with self.assertRaisesRegex(AgentProtocolError, "unknown manifest fields"):
            AgentManifest.from_dict(unknown)

    def test_manifest_and_specification_capabilities_must_match(self) -> None:
        manifest = AgentManifest("1", "baseline", "1")
        specification = AgentSpecification(
            "observation", "action", 1, AgentCapabilities(online_learning=True)
        )
        with self.assertRaisesRegex(AgentProtocolError, "must match"):
            validate_contract(manifest, specification)

    def test_determinism_check_accepts_same_seed_and_observation(self) -> None:
        check_determinism(MinimalAgent, self.specification, {"value": 1})

    def test_determinism_check_rejects_different_fresh_actions(self) -> None:
        actions = iter((0, 1))

        def factory() -> FixedActionAgent:
            return FixedActionAgent(next(actions))

        with self.assertRaisesRegex(AgentProtocolError, "not deterministic"):
            check_determinism(factory, self.specification, {"value": 1})


if __name__ == "__main__":
    unittest.main()
