"""Process-isolated execution primitives for benchmark runs."""

from __future__ import annotations

import multiprocessing as mp
import time
from dataclasses import dataclass
from typing import Any, Callable

from .manifest import AgentManifest, validate_contract
from .protocol import AgentProtocol, AgentSpecification, normalize_decision, validate_agent
from .registry import RunRecord, RunRegistry


@dataclass(frozen=True)
class RunResult:
    status: str
    action: Any = None
    reward: float | None = None
    confidence: float | None = None
    observation: Any = None
    next_observation: Any = None
    terminated: bool = False
    truncated: bool = False
    elapsed_seconds: float = 0.0
    error: str = ""


def _act_worker(
    factory: Callable[[], AgentProtocol],
    specification: AgentSpecification,
    observation: Any,
    result_queue: mp.Queue[Any],
) -> None:
    try:
        agent = factory()
        validate_agent(agent, specification)
        agent.observe(observation)
        decision = normalize_decision(
            agent.act(), uncertainty_declared=specification.capabilities.uncertainty
        )
        result_queue.put(("PASS", decision.action, decision.confidence, ""))
    except Exception as error:  # worker boundary must serialize failures
        result_queue.put(("ERROR", None, None, f"{type(error).__name__}: {error}"))


def run_action(
    factory: Callable[[], AgentProtocol],
    specification: AgentSpecification,
    manifest: AgentManifest,
    observation: Any,
) -> RunResult:
    """Run one black-box action in a fresh process with a hard timeout."""

    validate_contract(manifest, specification)
    start = time.monotonic()
    context = mp.get_context("spawn")
    result_queue: mp.Queue[Any] = context.Queue()
    process = context.Process(target=_act_worker, args=(factory, specification, observation, result_queue))
    process.start()
    process.join(manifest.declared_timeout_seconds)
    elapsed = time.monotonic() - start
    if process.is_alive():
        process.terminate()
        process.join()
        return RunResult("TIMEOUT", elapsed_seconds=elapsed, error="declared timeout exceeded")
    if result_queue.empty():
        return RunResult("ERROR", elapsed_seconds=elapsed, error="worker exited without a result")
    status, action, confidence, error = result_queue.get()
    return RunResult(status, action=action, confidence=confidence, elapsed_seconds=elapsed, error=error)


def record_result(
    registry: RunRegistry,
    result: RunResult,
    *,
    run_id: str,
    benchmark_version: str,
    environment: str,
    scenario: str,
    seed: int,
    manifest: AgentManifest,
    model_hash: str,
    adapter_hash: str,
    config_hash: str,
    hardware: str,
    software: str,
) -> None:
    """Persist a run result without replacing raw execution history."""

    registry.append(
        RunRecord.create(
            run_id=run_id,
            benchmark_version=benchmark_version,
            environment=environment,
            scenario=scenario,
            seed=seed,
            submission=manifest.agent_id,
            model_hash=model_hash,
            adapter_hash=adapter_hash,
            config_hash=config_hash,
            hardware=hardware,
            software=software,
            status=result.status,
        )
    )
