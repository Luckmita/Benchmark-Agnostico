"""Versioned metadata contract for agents and reproducible runs."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
import re
from typing import Any, Callable, Mapping

from .protocol import (
    AgentCapabilities,
    AgentProtocol,
    AgentProtocolError,
    AgentSpecification,
    validate_agent,
    validate_specification,
)


@dataclass(frozen=True)
class AgentManifest:
    """Public metadata; it must not contain hidden task data or ground truth."""

    manifest_version: str
    agent_id: str
    implementation_version: str
    capabilities: AgentCapabilities = field(default_factory=AgentCapabilities)
    entrypoint: str = "not-applicable"
    dependencies: tuple[str, ...] = ()
    declared_timeout_seconds: float = 1.0
    runtime: str = "python"
    training_provenance: str = "not-declared"
    model_hash: str = "not-applicable"
    adapter_hash: str = "not-applicable"
    hardware_requirements: str = "unspecified"

    def validate(self) -> None:
        for field_name, value in (
            ("manifest_version", self.manifest_version),
            ("agent_id", self.agent_id),
            ("implementation_version", self.implementation_version),
            ("entrypoint", self.entrypoint),
            ("runtime", self.runtime),
            ("training_provenance", self.training_provenance),
            ("hardware_requirements", self.hardware_requirements),
        ):
            if not isinstance(value, str) or not value.strip():
                raise AgentProtocolError(f"{field_name} is required")
        if (
            isinstance(self.declared_timeout_seconds, bool)
            or not isinstance(self.declared_timeout_seconds, (int, float))
            or not isfinite(self.declared_timeout_seconds)
            or self.declared_timeout_seconds <= 0
        ):
            raise AgentProtocolError("declared_timeout_seconds must be positive")
        if not isinstance(self.capabilities, AgentCapabilities):
            raise AgentProtocolError("capabilities must be AgentCapabilities")
        self.capabilities.validate()
        if not isinstance(self.dependencies, tuple) or any(
            not isinstance(item, str) or not item.strip() for item in self.dependencies
        ):
            raise AgentProtocolError("dependencies must be a tuple of non-empty strings")
        if len(set(self.dependencies)) != len(self.dependencies):
            raise AgentProtocolError("dependencies must be unique")
        for field_name, value in (("model_hash", self.model_hash), ("adapter_hash", self.adapter_hash)):
            if not isinstance(value, str):
                raise AgentProtocolError(f"{field_name} must be a string")
            if value not in {"not-applicable", "not-provided"} and re.fullmatch(r"sha256:[0-9a-f]{64}", value) is None:
                raise AgentProtocolError(f"{field_name} must be a sha256 digest or an explicit sentinel")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "AgentManifest":
        """Load the public JSON shape while rejecting missing or unknown fields."""

        expected = {
            "manifest_version",
            "agent_id",
            "implementation_version",
            "capabilities",
            "entrypoint",
            "dependencies",
            "declared_timeout_seconds",
            "runtime",
            "training_provenance",
            "model_hash",
            "adapter_hash",
            "hardware_requirements",
        }
        missing = expected - set(value)
        unknown = set(value) - expected
        if missing:
            raise AgentProtocolError(f"missing manifest fields: {', '.join(sorted(missing))}")
        if unknown:
            raise AgentProtocolError(f"unknown manifest fields: {', '.join(sorted(unknown))}")
        capabilities = value["capabilities"]
        if not isinstance(capabilities, Mapping):
            raise AgentProtocolError("capabilities must be an object")
        capability_keys = {"online_learning", "persistence", "uncertainty"}
        if set(capabilities) != capability_keys:
            raise AgentProtocolError("capabilities must contain exactly online_learning, persistence and uncertainty")
        dependencies = value["dependencies"]
        if not isinstance(dependencies, list):
            raise AgentProtocolError("dependencies must be an array")
        manifest = cls(
            manifest_version=value["manifest_version"],
            agent_id=value["agent_id"],
            implementation_version=value["implementation_version"],
            capabilities=AgentCapabilities(**capabilities),
            entrypoint=value["entrypoint"],
            dependencies=tuple(dependencies),
            declared_timeout_seconds=value["declared_timeout_seconds"],
            runtime=value["runtime"],
            training_provenance=value["training_provenance"],
            model_hash=value["model_hash"],
            adapter_hash=value["adapter_hash"],
            hardware_requirements=value["hardware_requirements"],
        )
        manifest.validate()
        return manifest


def validate_contract(manifest: AgentManifest, specification: AgentSpecification) -> None:
    """Require manifest and runtime specification to agree on capabilities."""

    manifest.validate()
    validate_specification(specification)
    if manifest.capabilities != specification.capabilities:
        raise AgentProtocolError("manifest and specification capabilities must match")


def check_determinism(
    factory: Callable[[], AgentProtocol],
    specification: AgentSpecification,
    observation: Any,
) -> None:
    """Compare fresh-agent actions for the same seeded public input."""

    validate_specification(specification)
    actions: list[Any] = []
    for _ in range(2):
        agent = factory()
        validate_agent(agent, specification)
        agent.observe(observation)
        actions.append(agent.act())
    if actions[0] != actions[1]:
        raise AgentProtocolError("agent is not deterministic for the same seed and observation")
