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


@dataclass(frozen=True)
class C4GeneralizationConfig:
    """C4: Train/test split for generalization."""

    base_config: C1BanditConfig = C1BanditConfig()
    train_fraction: float = 0.8


@dataclass(frozen=True)
class C7InterpretabilityConfig:
    """C7: Track decision complexity."""

    base_config: C1BanditConfig = C1BanditConfig()


class C7InterpretabilityTracker:
    def __init__(self, config: C7InterpretabilityConfig | None = None) -> None:
        self.config = config or C7InterpretabilityConfig()
        self._env = C1BanditEnvironment(self.config.base_config)
        self._decisions: list[int] = []

    def reset(self, seed: int) -> int:
        self._decisions = []
        return self._env.reset(seed)

    def step(self, action: Any) -> tuple[int, float, bool, bool, dict[str, Any]]:
        self._decisions.append(action)
        return self._env.step(action)

    def decision_complexity(self) -> float:
        """Return 0 for deterministic (always 0 or 1), 1 for mixed."""
        if not self._decisions:
            return 0.0
        unique = len(set(self._decisions))
        return float(unique - 1)


@dataclass(frozen=True)
class C8CompositionConfig:
    """C8: Two-phase task composition."""

    phase1_probabilities: tuple[float, float] = (0.2, 0.8)
    phase2_probabilities: tuple[float, float] = (0.4, 0.6)
    steps_per_phase: int = 50


class C8CompositionEnvironment:
    def __init__(self, config: C8CompositionConfig | None = None) -> None:
        self.config = config or C8CompositionConfig()
        self._phase = 1
        self._step_in_phase = 0
        self._env = C1BanditEnvironment(C1BanditConfig(reward_probabilities=self.config.phase1_probabilities, max_steps=self.config.steps_per_phase * 2))

    def reset(self, seed: int) -> int:
        self._phase = 1
        self._step_in_phase = 0
        return self._env.reset(seed)

    def step(self, action: Any) -> tuple[int, float, bool, bool, dict[str, Any]]:
        if self._step_in_phase >= self.config.steps_per_phase:
            self._phase = 2
            self._step_in_phase = 0
            self._env = C1BanditEnvironment(C1BanditConfig(reward_probabilities=self.config.phase2_probabilities, max_steps=self.config.steps_per_phase))

        obs, reward, terminated, truncated, info = self._env.step(action)
        self._step_in_phase += 1
        info["phase"] = self._phase
        return obs, reward, terminated, truncated, info


@dataclass(frozen=True)
class C9MultiagentConfig:
    """C9: Two-agent competitive environment."""

    num_agents: int = 2
    num_actions: int = 2
    max_steps: int = 100


class C9MultiagentEnvironment:
    def __init__(self, config: C9MultiagentConfig | None = None) -> None:
        self.config = config or C9MultiagentConfig()
        self._random = __import__("random").Random()
        self._steps = 0
        self._agent_actions: list[int] = [0] * self.config.num_agents

    def reset(self, seed: int) -> int:
        self._random.seed(seed)
        self._steps = 0
        self._agent_actions = [0] * self.config.num_agents
        return 0

    def step(self, actions: list[int]) -> tuple[int, list[float], bool, bool, dict[str, Any]]:
        """Step with multiple agent actions, return rewards for each."""
        if len(actions) != self.config.num_agents:
            raise ValueError(f"Expected {self.config.num_agents} actions")
        self._agent_actions = actions
        self._steps += 1
        
        rewards = []
        for action in actions:
            if isinstance(action, bool) or not isinstance(action, int) or action < 0 or action >= self.config.num_actions:
                raise ValueError(f"action must be integer in [0, {self.config.num_actions - 1}]")
            # Reward is shared: better when agents coordinate on same best action
            prob = 0.8 if action == 1 else 0.2
            reward = 1.0 if self._random.random() < prob else 0.0
            rewards.append(reward)

        terminated = self._steps >= self.config.max_steps
        return 0, rewards, terminated, False, {}


@dataclass(frozen=True)
class C11AuditConfig:
    """C11: Auditability and replay validation."""

    base_config: C1BanditConfig = C1BanditConfig()


class C11AuditEnvironment:
    def __init__(self, config: C11AuditConfig | None = None) -> None:
        self.config = config or C11AuditConfig()
        self._env = C1BanditEnvironment(self.config.base_config)
        self._trajectory: list[dict[str, Any]] = []

    def reset(self, seed: int) -> int:
        self._trajectory = []
        obs = self._env.reset(seed)
        self._trajectory.append({"step": 0, "action": None, "reward": None, "obs": obs})
        return obs

    def step(self, action: Any) -> tuple[int, float, bool, bool, dict[str, Any]]:
        obs, reward, terminated, truncated, info = self._env.step(action)
        self._trajectory.append({
            "action": action,
            "reward": reward,
            "obs": obs,
            "terminated": terminated,
        })
        return obs, reward, terminated, truncated, info

    def get_trajectory(self) -> list[dict[str, Any]]:
        """Return full audit trail."""
        return self._trajectory.copy()
