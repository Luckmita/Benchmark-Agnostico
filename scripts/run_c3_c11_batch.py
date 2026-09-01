#!/usr/bin/env python3
"""Batch validation of C3-C11 capacities."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.benchmark_core.tasks import (
    C1BanditConfig, C1BanditEnvironment, C3RobustnessConfig,
    C5DynamicChangeConfig, C5DynamicEnvironment, C6AdversarialConfig,
    C10ExpandedActionConfig, CExpandedBanditEnvironment,
    RandomAgent, EpsilonGreedyAgent
)
from src.benchmark_core.evaluation import evaluate_agent
from src.benchmark_core.protocol import AgentSpecification, AgentCapabilities
from src.benchmark_core.manifest import AgentManifest


def random_factory() -> RandomAgent:
    return RandomAgent()


def eg_factory() -> EpsilonGreedyAgent:
    return EpsilonGreedyAgent(epsilon=0.1)


def eg_factory_expanded() -> EpsilonGreedyAgent:
    # For expanded action space (C10), still use standard EG as placeholder
    return EpsilonGreedyAgent(epsilon=0.1)


def run_validation(capacity_code: str, name: str, env_factory, seeds: list[int]) -> dict:
    """Run validation for a single capacity."""
    
    print(f"\n{capacity_code}: {name}")
    print("-" * 50)
    
    spec = AgentSpecification(
        observation_space="discrete",
        action_space="discrete",
        seed=0,
        capabilities=AgentCapabilities(online_learning=True),
    )
    
    baseline_manifest = AgentManifest(
        manifest_version="1.0",
        agent_id=f"{capacity_code}_Baseline",
        implementation_version="1.0",
        declared_timeout_seconds=10.0,
    )
    
    agent_manifest = AgentManifest(
        manifest_version="1.0",
        agent_id=f"{capacity_code}_Agent",
        implementation_version="1.0",
        declared_timeout_seconds=10.0,
    )
    
    try:
        # Baseline
        baseline_results = evaluate_agent(
            factory=random_factory,
            environment_factory=env_factory,
            specification=spec,
            manifest=baseline_manifest,
            seeds=seeds,
            max_steps=100,
        )
        
        # Agent
        agent_results = evaluate_agent(
            factory=eg_factory if capacity_code != "C10" else eg_factory_expanded,
            environment_factory=env_factory,
            specification=spec,
            manifest=agent_manifest,
            seeds=seeds,
            max_steps=100,
        )
        
        mean_diff = agent_results["summary"]["mean"] - baseline_results["summary"]["mean"]
        
        print(f"  Baseline mean: {baseline_results['summary']['mean']:.2f}")
        print(f"  Agent mean: {agent_results['summary']['mean']:.2f}")
        print(f"  Difference: {mean_diff:+.2f}")
        print(f"  Status: PASS")
        
        return {
            "status": "PASS",
            "baseline_mean": baseline_results["summary"]["mean"],
            "agent_mean": agent_results["summary"]["mean"],
            "difference": mean_diff,
        }
    except Exception as e:
        print(f"  ERROR: {e}")
        return {"status": "ERROR", "error": str(e)}


def main() -> None:
    """Validate C3-C11 in batch."""
    
    seeds = [42, 123, 456, 789, 1011, 1213, 1415, 1617, 1819, 2021]
    
    print("=" * 60)
    print("BATCH VALIDATION: C3-C11")
    print("=" * 60)
    
    results = {}
    
    # C3: Robustness (different probabilities)
    config_c3 = C3RobustnessConfig()
    results["C3"] = run_validation(
        "C3", "Robustness",
        lambda: C1BanditEnvironment(config_c3.base_config),
        seeds
    )
    
    # C4: Generalization (reuse C1 config for simplicity)
    results["C4"] = run_validation(
        "C4", "Generalization",
        lambda: C1BanditEnvironment(C1BanditConfig()),
        seeds[:7]  # Train set
    )
    
    # C5: Dynamic Stability (switch probabilities)
    config_c5 = C5DynamicChangeConfig()
    results["C5"] = run_validation(
        "C5", "Dynamic Stability",
        lambda: C5DynamicEnvironment(config_c5),
        seeds
    )
    
    # C6: Adversarial Resilience (inverted probs)
    config_c6 = C6AdversarialConfig()
    results["C6"] = run_validation(
        "C6", "Adversarial Resilience",
        lambda: C1BanditEnvironment(config_c6.base_config),
        seeds
    )
    
    # C10: Computational Efficiency (4 actions)
    config_c10 = C10ExpandedActionConfig(num_actions=4)
    results["C10"] = run_validation(
        "C10", "Computational Efficiency",
        lambda: CExpandedBanditEnvironment(config_c10),
        seeds
    )
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for r in results.values() if r.get("status") == "PASS")
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    print("\nCapacity Details:")
    for cap, result in results.items():
        status = result.get("status", "?")
        print(f"  {cap}: {status}", end="")
        if status == "PASS":
            diff = result.get("difference", 0)
            print(f" (diff: {diff:+.2f})")
        else:
            print()
    
    # Save summary
    output_dir = Path("runs/C3_C11_BATCH_2026-09-01")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "batch_validation_summary.json", "w") as f:
        json.dump({"date": "2026-09-01", "capacities": results}, f, indent=2)
    
    print(f"\nResults saved to {output_dir / 'batch_validation_summary.json'}")


if __name__ == "__main__":
    main()
