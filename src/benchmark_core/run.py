"""Orchestration of one reproducible benchmark run."""

from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Callable

from .artifacts import ArtifactStore
from .episode import EpisodeEnvironment, run_episode
from .manifest import AgentManifest
from .protocol import AgentProtocol, AgentSpecification
from .registry import RunRecord, RunRegistry, hash_json, hash_source_tree


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
    benchmark_code_hash: str | None = None,
) -> str:
    """Execute, persist, and register one run; return its final status."""

    manifest.validate()
    manifest_data = manifest.to_dict()
    manifest_hash = hash_json(manifest_data)
    config_hash = hash_json(config)
    code_hash = benchmark_code_hash or hash_source_tree()
    artifact_store = ArtifactStore(artifact_root, run_id)
    artifact_store.write_json("manifest", "agent_manifest", manifest_data)
    artifact_store.write_json("manifest", "config", config)
    start_time = datetime.now(timezone.utc).isoformat()
    result = run_episode(
        factory,
        environment,
        specification,
        manifest,
        max_steps=max_steps,
        action_validator=action_validator,
    )
    end_time = datetime.now(timezone.utc).isoformat()
    artifact_store.write_json(
        "raw",
        "episode_result",
        {
            "status": result.status,
            "total_reward": result.total_reward,
            "steps": result.steps,
            "error": result.error,
            "steps_detail": [
                {
                    "step": index,
                    "action": item.action,
                    "reward": item.reward,
                    "confidence": item.confidence,
                    "action_elapsed_seconds": item.elapsed_seconds,
                }
                for index, item in enumerate(result.action_results, start=1)
            ],
        },
    )
    artifact_store.write_json(
        "metrics",
        "episode_metrics",
        {
            "run_id": run_id,
            "status": result.status,
            "total_reward": result.total_reward,
            "steps": result.steps,
            "mean_action_seconds": (
                sum(item.elapsed_seconds for item in result.action_results) / len(result.action_results)
                if result.action_results
                else None
            ),
        },
    )
    artifact_store.write_json(
        "manifest",
        "run_metadata",
        {
            "run_id": run_id,
            "benchmark_version": benchmark_version,
            "benchmark_code_hash": code_hash,
            "manifest_hash": manifest_hash,
            "config_hash": config_hash,
            "model_hash": manifest.model_hash,
            "adapter_hash": manifest.adapter_hash,
            "hardware": hardware,
            "software": software,
            "start_time": start_time,
            "end_time": end_time,
        },
    )
    artifact_store.write_json(
        "logs",
        "execution",
        {"run_id": run_id, "status": result.status, "error": result.error},
    )
    registry.append(
        RunRecord.create(
            run_id=run_id,
            benchmark_version=benchmark_version,
            environment=type(environment).__name__,
            scenario=scenario,
            seed=specification.seed,
            submission=manifest.agent_id,
            model_hash=manifest.model_hash,
            adapter_hash=manifest.adapter_hash,
            config_hash=config_hash,
            hardware=hardware,
            software=software,
            status=result.status,
            start_time=start_time,
            end_time=end_time,
            benchmark_code_hash=code_hash,
        )
    )
    return result.status
