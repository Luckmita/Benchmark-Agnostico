"""Architecture-neutral agent protocol and contract validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


class AgentProtocolError(TypeError):
    """Raised when an agent violates the public lifecycle contract."""


@dataclass(frozen=True)
class AgentCapabilities:
    """Optional behaviors declared by an agent implementation."""

    online_learning: bool = False
    persistence: bool = False
    uncertainty: bool = False


@dataclass(frozen=True)
class AgentSpecification:
    """Task-provided initialization data; it contains no hidden ground truth."""

    observation_space: Any
    action_space: Any
    seed: int
    capabilities: AgentCapabilities = field(default_factory=AgentCapabilities)


@dataclass(frozen=True)
class Transition:
    """A public interaction record delivered only when online learning is enabled."""

    observation: Any
    action: Any
    reward: float
    next_observation: Any
    terminated: bool
    truncated: bool = False


@runtime_checkable
class AgentProtocol(Protocol):
    def reset(self, specification: AgentSpecification) -> None:
        ...

    def observe(self, observation: Any) -> None:
        ...

    def act(self) -> Any:
        ...

    def learn(self, transition: Transition) -> None:
        ...

    def save(self) -> Any:
        ...

    def load(self, state: Any) -> None:
        ...


def validate_agent(agent: AgentProtocol, specification: AgentSpecification) -> None:
    """Check protocol shape and required optional capabilities before a run."""

    if not isinstance(specification.seed, int) or isinstance(specification.seed, bool):
        raise AgentProtocolError("seed must be an integer")
    if specification.seed < 0:
        raise AgentProtocolError("seed must be non-negative")
    if not isinstance(specification.capabilities, AgentCapabilities):
        raise AgentProtocolError("capabilities must be AgentCapabilities")
    if specification.observation_space is None or specification.action_space is None:
        raise AgentProtocolError("observation_space and action_space are required")
    required = ("reset", "observe", "act", "learn", "save", "load")
    missing = [name for name in required if not callable(getattr(agent, name, None))]
    if missing:
        raise AgentProtocolError(f"missing protocol methods: {', '.join(missing)}")
    agent.reset(specification)
    if specification.capabilities.persistence:
        state = agent.save()
        agent.load(state)
