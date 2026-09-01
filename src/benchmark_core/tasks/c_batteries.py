"""Public development tasks for C2-C11 capacities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .c1_learning import C1BanditConfig, C1BanditEnvironment


@dataclass(frozen=True)
class C2SampleEfficiencyConfig:
    """C2: Threshold-focused analysis of C1."""

    base_config: C1BanditConfig = C1BanditConfig()
    threshold_percentile: float = 0.75


@dataclass(frozen=True)
class C3RobustnessConfig:
    """C3: Variant probabilities for robustness check."""

    base_config: C1BanditConfig = C1BanditConfig(reward_probabilities=(0.3, 0.7))


@dataclass(frozen=True)
class C5DynamicChangeConfig:
    """C5: Probability switch at mid-point."""

    initial_probabilities: tuple[float, float] = (0.2, 0.8)
    switch_at_step: int = 50
    final_probabilities: tuple[float, float] = (0.7, 0.3)
    max_steps: int = 100


class C5DynamicEnvironment:
    def __init__(self, config: C5DynamicChangeConfig | None = None) -> None:
        self.config = config or C5DynamicChangeConfig()
        self._step = 0
        self._base_env = C1BanditEnvironment(
            C1BanditConfig(reward_probabilities=self.config.initial_probabilities, max_steps=self.config.max_steps)
        )

    def reset(self, seed: int) -> int:
        self._step = 0
        return self._base_env.reset(seed)

    def step(self, action: Any) -> tuple[int, float, bool, bool, dict[str, Any]]:
        if self._step == self.config.switch_at_step:
            self._base_env = C1BanditEnvironment(
                C1BanditConfig(reward_probabilities=self.config.final_probabilities, max_steps=self.config.max_steps)
            )
            self._base_env.reset(0)
        self._step += 1
        return self._base_env.step(action)


@dataclass(frozen=True)
class C6AdversarialConfig:
    """C6: Inverted reward probabilities."""

    base_config: C1BanditConfig = C1BanditConfig(reward_probabilities=(0.8, 0.2))


@dataclass(frozen=True)
class C10ExpandedActionConfig:
    """C10: Bandit with N actions instead of 2."""

    num_actions: int = 4
    reward_probabilities: tuple[float, ...] = (0.2, 0.4, 0.6, 0.8)
    max_steps: int = 100


class CExpandedBanditEnvironment:
    def __init__(self, config: C10ExpandedActionConfig | None = None) -> None:
        self.config = config or C10ExpandedActionConfig()
        self._random = __import__("random").Random()
        self._steps = 0

    def reset(self, seed: int) -> int:
        if not isinstance(seed, int) or isinstance(seed, bool) or seed < 0:
            raise ValueError("seed must be a non-negative integer")
        self._random.seed(seed)
        self._steps = 0
        return 0

    def step(self, action: Any) -> tuple[int, float, bool, bool, dict[str, Any]]:
        if isinstance(action, bool) or not isinstance(action, int) or action < 0 or action >= self.config.num_actions:
            raise ValueError(f"action must be integer in [0, {self.config.num_actions - 1}]")
        self._steps += 1
        probability = self.config.reward_probabilities[action]
        reward = 1.0 if self._random.random() < probability else 0.0
        terminated = self._steps >= self.config.max_steps
        return 0, reward, terminated, False, {}
