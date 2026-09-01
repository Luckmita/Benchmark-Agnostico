"""Environment-neutral episode execution contract."""

from __future__ import annotations

from dataclasses import dataclass
import multiprocessing as mp
import pickle
import time
from typing import Any, Callable, Protocol

from .manifest import AgentManifest
from .protocol import AgentProtocol, AgentSpecification, Transition, validate_agent
from .runner import RunResult


class EpisodeEnvironment(Protocol):
    def reset(self, seed: int) -> Any:
        ...

    def step(self, action: Any) -> tuple[Any, float, bool, bool, dict[str, Any]]:
        ...


@dataclass(frozen=True)
class EpisodeResult:
    status: str
    total_reward: float
    steps: int
    action_results: tuple[RunResult, ...]
    error: str = ""


def run_episode(
    factory: Callable[[], AgentProtocol],
    environment: EpisodeEnvironment,
    specification: AgentSpecification,
    manifest: AgentManifest,
    *,
    max_steps: int,
    action_validator: Callable[[Any], None] | None = None,
) -> EpisodeResult:
    """Run one stateful episode in a fresh process with a hard timeout."""

    if max_steps <= 0:
        return EpisodeResult("ERROR", 0.0, 0, (), "max_steps must be positive")
    manifest.validate()
    try:
        pickle.dumps((factory, environment, specification, action_validator))
    except (pickle.PicklingError, TypeError) as error:
        return EpisodeResult("ERROR", 0.0, 0, (), f"inputs are not spawnable: {error}")
    context = mp.get_context("spawn")
    result_queue: mp.Queue[Any] = context.Queue()
    process = context.Process(
        target=_episode_worker,
        args=(factory, environment, specification, max_steps, action_validator, result_queue),
    )
    process.start()
    process.join(manifest.declared_timeout_seconds)
    if process.is_alive():
        process.terminate()
        process.join()
        return EpisodeResult("TIMEOUT", 0.0, 0, (), "declared timeout exceeded")
    if result_queue.empty():
        return EpisodeResult("ERROR", 0.0, 0, (), "worker exited without a result")
    return result_queue.get()


def _episode_worker(
    factory: Callable[[], AgentProtocol],
    environment: EpisodeEnvironment,
    specification: AgentSpecification,
    max_steps: int,
    action_validator: Callable[[Any], None] | None,
    result_queue: mp.Queue[Any],
) -> None:
    try:
        agent = factory()
        validate_agent(agent, specification)
        observation = environment.reset(specification.seed)
        total_reward = 0.0
        action_results: list[RunResult] = []
        for step in range(max_steps):
            agent.observe(observation)
            action_start = time.monotonic()
            action = agent.act()
            action_elapsed = time.monotonic() - action_start
            if action_validator is not None:
                action_validator(action)
            next_observation, reward, terminated, truncated, _info = environment.step(action)
            reward = float(reward)
            total_reward += reward
            action_results.append(RunResult("PASS", action=action, reward=reward, elapsed_seconds=action_elapsed))
            if specification.capabilities.online_learning:
                agent.learn(Transition(observation, action, reward, next_observation, terminated, truncated))
            observation = next_observation
            if terminated or truncated:
                result_queue.put(EpisodeResult("PASS", total_reward, step + 1, tuple(action_results)))
                return
        result_queue.put(EpisodeResult("MAX_STEPS", total_reward, max_steps, tuple(action_results)))
    except ValueError as error:
        result_queue.put(EpisodeResult("INVALID_ACTION", 0.0, 0, (), str(error)))
    except Exception as error:  # worker boundary must serialize failures
        result_queue.put(EpisodeResult("ERROR", 0.0, 0, (), f"{type(error).__name__}: {error}"))
