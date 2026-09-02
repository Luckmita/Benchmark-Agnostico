"""Public development prototypes aligned with the normative C2-C9 taxonomy.

These helpers exercise contracts and controls. They are not sealed tasks and do
not constitute construct validation or a gate freeze.
"""

from __future__ import annotations

from dataclasses import dataclass
import random
import re
from typing import Any, Protocol

from .c1_learning import C1BanditConfig


PUBLIC_CAPACITY_NAMES: dict[str, str] = {
    "C1": "learning",
    "C2": "sample_efficiency",
    "C3": "generalization",
    "C4": "adaptation",
    "C5": "temporal_dependency",
    "C6": "planning",
    "C7": "continual_learning",
    "C8": "robustness",
    "C9": "multidomain_transfer",
    "C10": "uncertainty",
    "C11": "computational_efficiency",
}


@dataclass(frozen=True)
class C2SampleEfficiencyConfig:
    """Checkpoint protocol layered on an approved C1 family."""

    base_config: C1BanditConfig = C1BanditConfig()
    checkpoints: tuple[int, ...] = (10, 25, 50, 100)

    def validate(self) -> None:
        self.base_config.validate()
        if not self.checkpoints or any(step <= 0 for step in self.checkpoints):
            raise ValueError("checkpoints must be positive")
        if tuple(sorted(set(self.checkpoints))) != self.checkpoints:
            raise ValueError("checkpoints must be unique and increasing")
        if self.checkpoints[-1] > self.base_config.max_steps:
            raise ValueError("checkpoints cannot exceed the C1 budget")


@dataclass(frozen=True)
class C3GeneralizationConfig:
    """Explicit TRAIN/ID/OOD/structural development partitions."""

    train_probabilities: tuple[float, float] = (0.2, 0.8)
    id_heldout_probabilities: tuple[float, float] = (0.25, 0.75)
    ood_probabilities: tuple[float, float] = (0.4, 0.6)
    structural_transfer_encoding: tuple[str, str] = ("left", "right")

    def partitions(self) -> dict[str, dict[str, Any]]:
        values = {
            "TRAIN": {"reward_probabilities": self.train_probabilities, "encoding": (0, 1)},
            "ID_HELDOUT": {"reward_probabilities": self.id_heldout_probabilities, "encoding": (0, 1)},
            "OOD": {"reward_probabilities": self.ood_probabilities, "encoding": (0, 1)},
            "STRUCTURAL_TRANSFER": {
                "reward_probabilities": self.train_probabilities,
                "encoding": self.structural_transfer_encoding,
            },
        }
        for partition in values.values():
            C1BanditConfig(reward_probabilities=partition["reward_probabilities"]).validate()
        if len(set(self.structural_transfer_encoding)) != 2:
            raise ValueError("structural transfer encoding must contain two distinct actions")
        return values


@dataclass(frozen=True)
class C4AdaptationConfig:
    """Unannounced within-episode probability drift."""

    initial_probabilities: tuple[float, float] = (0.2, 0.8)
    change_at_step: int = 50
    final_probabilities: tuple[float, float] = (0.7, 0.3)
    max_steps: int = 100

    def validate(self) -> None:
        C1BanditConfig(self.initial_probabilities, self.max_steps).validate()
        C1BanditConfig(self.final_probabilities, self.max_steps).validate()
        if not 1 <= self.change_at_step < self.max_steps:
            raise ValueError("change_at_step must be inside the episode")
        if self.initial_probabilities == self.final_probabilities:
            raise ValueError("adaptation requires a real distribution change")


class C4AdaptationEnvironment:
    """Bandit drift prototype without an observation-side change flag."""

    def __init__(self, config: C4AdaptationConfig | None = None) -> None:
        self.config = config or C4AdaptationConfig()
        self.config.validate()
        self._random = random.Random()
        self._steps = 0

    def reset(self, seed: int) -> int:
        if not isinstance(seed, int) or isinstance(seed, bool) or seed < 0:
            raise ValueError("seed must be a non-negative integer")
        self._random.seed(seed)
        self._steps = 0
        return 0

    def step(self, action: Any) -> tuple[int, float, bool, bool, dict[str, Any]]:
        if isinstance(action, bool) or not isinstance(action, int) or action not in (0, 1):
            raise ValueError("action must be integer 0 or 1")
        probabilities = (
            self.config.initial_probabilities
            if self._steps < self.config.change_at_step
            else self.config.final_probabilities
        )
        reward = 1.0 if self._random.random() < probabilities[action] else 0.0
        self._steps += 1
        terminated = self._steps >= self.config.max_steps
        return 0, reward, terminated, False, {"phase": "pre" if self._steps <= self.config.change_at_step else "post"}


@dataclass(frozen=True)
class C5TemporalDependencyConfig:
    """Delayed-cue task where the decision observation omits the cue."""

    delay: int = 5
    distractor_observation: int = -1

    def validate(self) -> None:
        if self.delay < 1:
            raise ValueError("delay must be at least one step")
        if self.distractor_observation in (0, 1):
            raise ValueError("distractor observation cannot reveal the binary cue")


class C5TemporalDependencyEnvironment:
    def __init__(self, config: C5TemporalDependencyConfig | None = None) -> None:
        self.config = config or C5TemporalDependencyConfig()
        self.config.validate()
        self._random = random.Random()
        self._cue = 0
        self._steps = 0

    def reset(self, seed: int) -> int:
        if not isinstance(seed, int) or isinstance(seed, bool) or seed < 0:
            raise ValueError("seed must be a non-negative integer")
        self._random.seed(seed)
        self._cue = self._random.randrange(2)
        self._steps = 0
        return self._cue

    def step(self, action: Any) -> tuple[int, float, bool, bool, dict[str, Any]]:
        if isinstance(action, bool) or not isinstance(action, int) or action not in (0, 1):
            raise ValueError("action must be integer 0 or 1")
        self._steps += 1
        decision = self._steps > self.config.delay
        reward = 1.0 if decision and action == self._cue else 0.0
        return self.config.distractor_observation, reward, decision, False, {"decision": decision}


@dataclass(frozen=True)
class C6PlanningConfig:
    """Immediate-versus-delayed return conflict."""

    horizon: int = 5
    myopic_immediate: float = 1.0
    myopic_delayed: float = -2.0
    farsighted_immediate: float = -0.5
    farsighted_delayed: float = 3.0

    def validate(self) -> None:
        if self.horizon < 2:
            raise ValueError("planning horizon must be at least two")
        if self.myopic_immediate <= self.farsighted_immediate:
            raise ValueError("action 0 must be locally attractive")
        if self.myopic_immediate + self.myopic_delayed >= self.farsighted_immediate + self.farsighted_delayed:
            raise ValueError("action 1 must have the better delayed return")


class C6PlanningEnvironment:
    def __init__(self, config: C6PlanningConfig | None = None) -> None:
        self.config = config or C6PlanningConfig()
        self.config.validate()
        self._steps = 0
        self._first_action: int | None = None

    def reset(self, seed: int) -> str:
        if not isinstance(seed, int) or isinstance(seed, bool) or seed < 0:
            raise ValueError("seed must be a non-negative integer")
        self._steps = 0
        self._first_action = None
        return "choose"

    def step(self, action: Any) -> tuple[str, float, bool, bool, dict[str, Any]]:
        if isinstance(action, bool) or not isinstance(action, int) or action not in (0, 1):
            raise ValueError("action must be integer 0 or 1")
        self._steps += 1
        if self._first_action is None:
            self._first_action = action
            reward = self.config.myopic_immediate if action == 0 else self.config.farsighted_immediate
        elif self._steps == self.config.horizon:
            reward = self.config.myopic_delayed if self._first_action == 0 else self.config.farsighted_delayed
        else:
            reward = 0.0
        terminated = self._steps >= self.config.horizon
        return "wait", reward, terminated, False, {}


@dataclass(frozen=True)
class C7ContinualLearningConfig:
    """Ordered public task labels for performance-matrix evaluation."""

    tasks: tuple[str, ...] = ("A", "B", "C", "D")
    interactions_per_task: int = 100

    def validate(self) -> None:
        if len(self.tasks) < 2 or len(set(self.tasks)) != len(self.tasks):
            raise ValueError("continual learning requires unique ordered tasks")
        if self.interactions_per_task <= 0:
            raise ValueError("interactions_per_task must be positive")


def forgetting_from_performance_matrix(matrix: list[list[float]]) -> tuple[float, ...]:
    """Return per-task best-prior minus final performance.

    Rows represent training phases and columns represent retested tasks. Values
    that were not yet measured must be omitted by using shorter rows.
    """

    if not matrix or any(not row for row in matrix):
        raise ValueError("performance matrix cannot be empty")
    width = len(matrix[-1])
    if any(len(row) > width for row in matrix):
        raise ValueError("matrix rows cannot exceed final width")
    forgetting: list[float] = []
    for task_index in range(width):
        observed = [row[task_index] for row in matrix if task_index < len(row)]
        forgetting.append(max(observed) - observed[-1])
    return tuple(forgetting)


class PublicEnvironment(Protocol):
    def reset(self, seed: int) -> Any: ...

    def step(self, action: Any) -> tuple[Any, float, bool, bool, dict[str, Any]]: ...


@dataclass(frozen=True)
class C8RobustnessConfig:
    """Missing-observation perturbation independent from task reward."""

    missing_probability: float = 0.1
    missing_sentinel: str = "MISSING"

    def validate(self) -> None:
        if not 0.0 <= self.missing_probability <= 1.0:
            raise ValueError("missing_probability must be between zero and one")


class C8MissingObservationWrapper:
    def __init__(self, environment: PublicEnvironment, config: C8RobustnessConfig | None = None) -> None:
        self.environment = environment
        self.config = config or C8RobustnessConfig()
        self.config.validate()
        self._random = random.Random()

    def _perturb(self, observation: Any) -> Any:
        if self._random.random() < self.config.missing_probability:
            return self.config.missing_sentinel
        return observation

    def reset(self, seed: int) -> Any:
        self._random.seed(seed ^ 0xC8)
        return self._perturb(self.environment.reset(seed))

    def step(self, action: Any) -> tuple[Any, float, bool, bool, dict[str, Any]]:
        observation, reward, terminated, truncated, info = self.environment.step(action)
        return self._perturb(observation), reward, terminated, truncated, info


@dataclass(frozen=True)
class C9DomainSpec:
    name: str
    family: str
    observation_protocol: str
    action_protocol: str

    def validate(self) -> None:
        if not all(value.strip() for value in (self.name, self.family, self.observation_protocol, self.action_protocol)):
            raise ValueError("domain fields must be non-empty")


@dataclass(frozen=True)
class C9MultidomainTransferConfig:
    """Declares distinct public domains evaluated with one frozen core hash."""

    domains: tuple[C9DomainSpec, ...]
    core_hash: str

    def validate(self) -> None:
        if len(self.domains) < 2:
            raise ValueError("multidomain transfer requires at least two domains")
        for domain in self.domains:
            domain.validate()
        if len({domain.family for domain in self.domains}) < 2:
            raise ValueError("domains must come from distinct structural families")
        if re.fullmatch(r"sha256:[0-9a-f]{64}", self.core_hash) is None:
            raise ValueError("core_hash must be a sha256 digest")
