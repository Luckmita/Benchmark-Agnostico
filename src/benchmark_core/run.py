"""Orchestration of one reproducible benchmark run."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from .artifacts import ArtifactStore
from .episode import EpisodeEnvironment, run_episode
from .manifest import AgentManifest
from .protocol import AgentProtocol, AgentSpecification
from .registry import RunRecord, RunRegistry, hash_json


def execute_run(
    factory: Callable[[], AgentProtocol],
    environment: EpisodeEnvironment,
    specification: AgentSpecification,
    manifest: AgentManifest,
    *,
    run_id: str,
    benchmark_version: str,
    scenario: str,
    artifact_root: Path,
    registry: RunRegistry,
    config: dict[str, Any],
    hardware: str = "unknown",
    software: str = "unknown",
    max_steps: int,
    action_validator: Callable[[Any], None] | None = None,
) -> str:
    """Execute, persist, and register one run; return its final status."""

    manifest.validate()
    manifest_data = manifest.to_dict()
    artifact_store = ArtifactStore(artifact_root, run_id)
    artifact_store.write_json("manifest", "agent_manifest", manifest_data)
    artifact_store.write_json("manifest", "config", config)
    result = run_episode(
        factory,
        environment,
        specification,
        manifest,
        max_steps=max_steps,
        action_validator=action_validator,
    )
    artifact_store.write_json(
        "raw",
        "episode_result",
        {
            "status": result.status,
            "total_reward": result.total_reward,
            "steps": result.steps,
            "error": result.error,
            "actions": [item.action for item in result.action_results],
        },
    )
    registry.append(
        RunRecord.create(
            run_id=run_id,
            benchmark_version=benchmark_version,
            environment=type(environment).__name__,
            scenario=scenario,
            seed=specification.seed,
            submission=manifest.agent_id,
            model_hash=hash_json(manifest_data),
            adapter_hash="not-applicable",
            config_hash=hash_json(config),
            hardware=hardware,
            software=software,
            status=result.status,
        )
    )
    return result.status
