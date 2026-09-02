"""Architecture-neutral agent protocol and contract validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite
import pickle
from typing import Any, Protocol, runtime_checkable


class AgentProtocolError(TypeError):
    """Raised when an agent violates the public lifecycle contract."""


@dataclass(frozen=True)
class AgentCapabilities:
    """Optional behaviors declared by an agent implementation."""

    online_learning: bool = False
    persistence: bool = False
    uncertainty: bool = False

    def validate(self) -> None:
        for name, value in (
            ("online_learning", self.online_learning),
            ("persistence", self.persistence),
            ("uncertainty", self.uncertainty),
        ):
            if not isinstance(value, bool):
                raise AgentProtocolError(f"capability {name} must be boolean")


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


@dataclass(frozen=True)
class AgentDecision:
    """Optional action envelope for agents declaring uncertainty support."""

    action: Any
    confidence: float | None = None

    def validate(self, *, uncertainty_declared: bool) -> None:
        if uncertainty_declared:
            if self.confidence is None or not isfinite(float(self.confidence)):
                raise AgentProtocolError("uncertainty capability requires finite confidence")
            if not 0.0 <= float(self.confidence) <= 1.0:
                raise AgentProtocolError("confidence must be between zero and one")
        elif self.confidence is not None:
            raise AgentProtocolError("confidence requires uncertainty capability declaration")


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

    validate_specification(specification)
    required = ("reset", "observe", "act", "learn", "save", "load")
    missing = [name for name in required if not callable(getattr(agent, name, None))]
    if missing:
        raise AgentProtocolError(f"missing protocol methods: {', '.join(missing)}")
    agent.reset(specification)
    if specification.capabilities.persistence:
        state = agent.save()
        try:
            pickle.dumps(state)
        except (pickle.PicklingError, TypeError, AttributeError) as error:
            raise AgentProtocolError(f"saved state must be serializable: {error}") from error
        agent.load(state)


def validate_specification(specification: AgentSpecification) -> None:
    """Validate protocol metadata while leaving spaces opaque."""

    if not isinstance(specification.seed, int) or isinstance(specification.seed, bool):
        raise AgentProtocolError("seed must be an integer")
    if specification.seed < 0:
        raise AgentProtocolError("seed must be non-negative")
    if not isinstance(specification.capabilities, AgentCapabilities):
        raise AgentProtocolError("capabilities must be AgentCapabilities")
    specification.capabilities.validate()
    if specification.observation_space is None or specification.action_space is None:
        raise AgentProtocolError("observation_space and action_space are required")


def normalize_decision(output: Any, *, uncertainty_declared: bool) -> AgentDecision:
    """Normalize a raw action or validate an uncertainty-aware action envelope."""

    if isinstance(output, AgentDecision):
        output.validate(uncertainty_declared=uncertainty_declared)
        return output
    if uncertainty_declared:
        raise AgentProtocolError("uncertainty capability requires AgentDecision output")
    return AgentDecision(action=output)
