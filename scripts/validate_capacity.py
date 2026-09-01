#!/usr/bin/env python3
"""Generic capacity validation template for C2-C11."""

import json
import sys
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.benchmark_core.evaluation import evaluate_agent
from src.benchmark_core.protocol import AgentSpecification, AgentCapabilities
from src.benchmark_core.manifest import AgentManifest


def validate_capacity(
    capacity_name: str,
    capacity_id: int,
    agent_factory: Callable,
    baseline_factory: Callable,
    environment_factory: Callable,
    seeds: list[int],
    max_steps: int,
    config_dict: dict[str, Any],
) -> dict[str, Any]:
    """
    Generic capacity validation orchestrator.
    
    Parameters:
    - capacity_name: descriptive name (e.g., "Sample Efficiency")
    - capacity_id: 1-11 (C1-C11)
    - agent_factory: callable returning test agent
    - baseline_factory: callable returning baseline agent
    - environment_factory: callable returning environment
    - seeds: list of seeds for reproducibility
    - max_steps: steps per episode
    - config_dict: task-specific configuration
    
    Returns: evaluation results dict with summary statistics
    """
    
    capacity_code = f"C{capacity_id}"
    spec = AgentSpecification(
        observation_space="discrete",
        action_space="discrete",
        seed=0,
        capabilities=AgentCapabilities(online_learning=True),
    )
    
    agent_manifest = AgentManifest(
        manifest_version="1.0",
        agent_id=f"{capacity_code}_Agent",
        implementation_version="1.0",
        declared_timeout_seconds=10.0,
    )
    
    baseline_manifest = AgentManifest(
        manifest_version="1.0",
        agent_id=f"{capacity_code}_Baseline",
        implementation_version="1.0",
        declared_timeout_seconds=10.0,
    )
    
    print(f"{capacity_code} - {capacity_name}")
    print("=" * 60)
    print(f"Seeds: {len(seeds)} ({seeds[0]}...{seeds[-1]})")
    print(f"Max steps: {max_steps}")
    print()
    
    # Evaluate baseline
    print(f"Evaluating {capacity_code} baseline...")
    baseline_results = evaluate_agent(
        factory=baseline_factory,
        environment_factory=environment_factory,
        specification=spec,
        manifest=baseline_manifest,
        seeds=seeds,
        max_steps=max_steps,
    )
    
    print(f"  Baseline mean: {baseline_results['summary']['mean']:.3f}")
    print(f"  Baseline median: {baseline_results['summary']['median']:.3f}")
    print(f"  Baseline IC95: [{baseline_results['summary']['ci95_low']:.3f}, {baseline_results['summary']['ci95_high']:.3f}]")
    print()
    
    # Evaluate agent
    print(f"Evaluating {capacity_code} test agent...")
    agent_results = evaluate_agent(
        factory=agent_factory,
        environment_factory=environment_factory,
        specification=spec,
        manifest=agent_manifest,
        seeds=seeds,
        max_steps=max_steps,
    )
    
    print(f"  Agent mean: {agent_results['summary']['mean']:.3f}")
    print(f"  Agent median: {agent_results['summary']['median']:.3f}")
    print(f"  Agent IC95: [{agent_results['summary']['ci95_low']:.3f}, {agent_results['summary']['ci95_high']:.3f}]")
    print()
    
    # Comparison
    mean_diff = agent_results["summary"]["mean"] - baseline_results["summary"]["mean"]
    print(f"Comparison:")
    print(f"  Mean difference: {mean_diff:+.3f}")
    print()
    
    # Aggregate results
    results = {
        "metadata": {
            "date": "2026-09-01",
            "capacity": capacity_code,
            "name": capacity_name,
            "status": "PROPOSED - PENDING APPROVAL",
            "change_id": f"CHG-2026-09-01-{capacity_code}-FINAL-PARAMETERS",
        },
        "parameters": {
            "seeds": seeds,
            "max_steps": max_steps,
            **config_dict,
        },
        "baseline": {
            "returns": baseline_results["returns"],
            "summary": baseline_results["summary"],
            "statuses": baseline_results["statuses"],
        },
        "agent": {
            "returns": agent_results["returns"],
            "summary": agent_results["summary"],
            "statuses": agent_results["statuses"],
        },
        "comparison": {
            "mean_difference": mean_diff,
        },
    }
    
    return results


if __name__ == "__main__":
    print("Capacity validation template - import and use validate_capacity()")
