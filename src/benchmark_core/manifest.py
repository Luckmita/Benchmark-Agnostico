"""Versioned metadata contract for agents and reproducible runs."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any, Callable

from .protocol import AgentCapabilities, AgentProtocol, AgentProtocolError, AgentSpecification, validate_agent


@dataclass(frozen=True)
class AgentManifest:
    """Public metadata; it must not contain hidden task data or ground truth."""

    manifest_version: str
    agent_id: str
    implementation_version: str
    capabilities: AgentCapabilities = field(default_factory=AgentCapabilities)
    entrypoint: str = ""
    dependencies: tuple[str, ...] = ()
    declared_timeout_seconds: float = 1.0

    def validate(self) -> None:
        if not self.manifest_version.strip():
            raise AgentProtocolError("manifest_version is required")
        if not self.agent_id.strip():
            raise AgentProtocolError("agent_id is required")
        if not self.implementation_version.strip():
            raise AgentProtocolError("implementation_version is required")
        if not isfinite(self.declared_timeout_seconds) or self.declared_timeout_seconds <= 0:
            raise AgentProtocolError("declared_timeout_seconds must be positive")
        if not isinstance(self.capabilities, AgentCapabilities):
            raise AgentProtocolError("capabilities must be AgentCapabilities")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)


def validate_specification(specification: AgentSpecification) -> None:
    """Validate only protocol metadata, never the opaque spaces themselves."""

    if not isinstance(specification.seed, int) or isinstance(specification.seed, bool):
        raise AgentProtocolError("seed must be an integer")
    if specification.seed < 0:
        raise AgentProtocolError("seed must be non-negative")
    if not isinstance(specification.capabilities, AgentCapabilities):
        raise AgentProtocolError("capabilities must be AgentCapabilities")
    if specification.observation_space is None or specification.action_space is None:
        raise AgentProtocolError("observation_space and action_space are required")


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
