"""C1 public development task: stationary two-action bandit."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from ..protocol import AgentSpecification, Transition


@dataclass(frozen=True)
class C1BanditConfig:
    """Development-only parameters; final values require preregistration."""

    reward_probabilities: tuple[float, float] = (0.2, 0.8)
    max_steps: int = 100

    def validate(self) -> None:
        if len(self.reward_probabilities) != 2:
            raise ValueError("C1 requires exactly two action probabilities")
        if any(probability < 0.0 or probability > 1.0 for probability in self.reward_probabilities):
            raise ValueError("reward probabilities must be between zero and one")
        if self.reward_probabilities[0] == self.reward_probabilities[1]:
            raise ValueError("C1 actions must have different reward probabilities")
        if self.max_steps <= 0:
            raise ValueError("max_steps must be positive")


class C1BanditEnvironment:
    """Constant observation; only reward feedback reveals action quality."""

    def __init__(self, config: C1BanditConfig | None = None) -> None:
        self.config = config or C1BanditConfig()
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
        self._steps += 1
        probability = self.config.reward_probabilities[action]
        reward = 1.0 if self._random.random() < probability else 0.0
        terminated = self._steps >= self.config.max_steps
        return 0, reward, terminated, False, {}


class RandomAgent:
    def reset(self, specification: AgentSpecification) -> None:
        self._random = random.Random(specification.seed)

    def observe(self, observation: Any) -> None:
        pass

    def act(self) -> int:
        return self._random.randrange(2)

    def learn(self, transition: Transition) -> None:
        pass

    def save(self) -> None:
        return None

    def load(self, state: Any) -> None:
        pass


class EpsilonGreedyAgent:
    def __init__(self, epsilon: float = 0.1) -> None:
        if not 0.0 <= epsilon <= 1.0:
            raise ValueError("epsilon must be between zero and one")
        self.epsilon = epsilon
        self._random = random.Random()
        self._counts = [0, 0]
        self._values = [0.0, 0.0]

    def reset(self, specification: AgentSpecification) -> None:
        self._random.seed(specification.seed)
        self._counts = [0, 0]
        self._values = [0.0, 0.0]

    def observe(self, observation: Any) -> None:
        pass

    def act(self) -> int:
        if self._random.random() < self.epsilon or self._counts[0] == self._counts[1]:
            return self._random.randrange(2)
        return 0 if self._values[0] > self._values[1] else 1

    def learn(self, transition: Transition) -> None:
        action = transition.action
        if isinstance(action, bool) or not isinstance(action, int) or action not in (0, 1):
            raise ValueError("transition action must be integer 0 or 1")
        self._counts[action] += 1
        count = self._counts[action]
        self._values[action] += (float(transition.reward) - self._values[action]) / count

    def save(self) -> dict[str, Any]:
        return {"counts": list(self._counts), "values": list(self._values)}

    def load(self, state: dict[str, Any]) -> None:
        self._counts = list(state["counts"])
        self._values = list(state["values"])
