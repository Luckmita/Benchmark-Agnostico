"""Evaluation helpers that preserve per-seed results and uncertainty."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Callable, Sequence

from .episode import EpisodeEnvironment, run_episode
from .manifest import AgentManifest
from .metrics import SummaryStatistics, summarize
from .protocol import AgentProtocol, AgentSpecification


def evaluate_agent(
    factory: Callable[[], AgentProtocol],
    environment_factory: Callable[[], EpisodeEnvironment],
    specification: AgentSpecification,
    manifest: AgentManifest,
    *,
    seeds: Sequence[int],
    max_steps: int,
    action_validator: Callable[[Any], None] | None = None,
) -> dict[str, Any]:
    """Evaluate an agent over explicit seeds without hiding per-seed outcomes."""

    if not seeds:
        raise ValueError("at least one seed is required")
    returns: list[float] = []
    statuses: list[str] = []
    for seed in seeds:
        seeded_specification = AgentSpecification(
            specification.observation_space,
            specification.action_space,
            seed,
            specification.capabilities,
        )
        result = run_episode(
            factory,
            environment_factory(),
            seeded_specification,
            manifest,
            max_steps=max_steps,
            action_validator=action_validator,
        )
        returns.append(result.total_reward)
        statuses.append(result.status)
    summary: SummaryStatistics = summarize(returns)
    return {
        "seeds": list(seeds),
        "returns": returns,
        "statuses": statuses,
        "summary": asdict(summary),
    }
