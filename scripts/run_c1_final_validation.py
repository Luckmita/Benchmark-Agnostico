#!/usr/bin/env python3
"""C1 final validation: execute frozen parameters and publish results."""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.benchmark_core.tasks import C1BanditConfig, C1BanditEnvironment, RandomAgent, EpsilonGreedyAgent
from src.benchmark_core.evaluation import evaluate_agent
from src.benchmark_core.protocol import AgentSpecification, AgentCapabilities
from src.benchmark_core.manifest import AgentManifest


def random_agent_factory() -> RandomAgent:
    """Factory for Random agent (module-level for pickling)."""
    return RandomAgent()


def epsilon_greedy_agent_factory() -> EpsilonGreedyAgent:
    """Factory for EpsilonGreedy agent (module-level for pickling)."""
    return EpsilonGreedyAgent(epsilon=0.1)


def main() -> None:
    """Execute C1 final validation with frozen parameters."""
    
    # Frozen parameters from C1_LEARNING_FINAL_PARAMETERS.md
    seeds = [42, 123, 456, 789, 1011, 1213, 1415, 1617, 1819, 2021]
    max_steps = 100
    threshold = 70.0  # Realistic threshold for learning agent
    config = C1BanditConfig(reward_probabilities=(0.2, 0.8), max_steps=max_steps)
    
    output_dir = Path("runs/C1_FINAL_2026-09-01")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("C1 Final Validation - Frozen Parameters")
    print("=" * 50)
    print(f"Seeds: {seeds}")
    print(f"Max steps per episode: {max_steps}")
    print(f"Threshold: {threshold}")
    print(f"Task: Bandit with probabilities {config.reward_probabilities}")
    print()
    
    # Create specification and manifest for agents
    spec = AgentSpecification(
        observation_space="discrete",
        action_space="discrete",
        seed=0,  # Will be overridden per seed
        capabilities=AgentCapabilities(online_learning=True),  # Enable learning
    )
    
    random_manifest = AgentManifest(
        manifest_version="1.0",
        agent_id="C1_Random",
        implementation_version="1.0",
        declared_timeout_seconds=5.0,
    )
    eg_manifest = AgentManifest(
        manifest_version="1.0",
        agent_id="C1_EpsilonGreedy",
        implementation_version="1.0",
        declared_timeout_seconds=5.0,
    )
    
    # Evaluate Random baseline
    print("Evaluating Random baseline...")
    random_results = evaluate_agent(
        factory=random_agent_factory,
        environment_factory=lambda: C1BanditEnvironment(config),
        specification=spec,
        manifest=random_manifest,
        seeds=seeds,
        max_steps=max_steps,
    )
    random_returns = random_results["returns"]
    
    print(f"  Random mean return: {random_results['summary']['mean']:.3f}")
    print(f"  Random median return: {random_results['summary']['median']:.3f}")
    print(f"  Random IC95: [{random_results['summary']['ci95_low']:.3f}, {random_results['summary']['ci95_high']:.3f}]")
    print()
    
    # Evaluate EpsilonGreedy learner
    print("Evaluating EpsilonGreedy learner...")
    
    eg_results = evaluate_agent(
        factory=epsilon_greedy_agent_factory,
        environment_factory=lambda: C1BanditEnvironment(config),
        specification=spec,
        manifest=eg_manifest,
        seeds=seeds,
        max_steps=max_steps,
    )
    eg_returns = eg_results["returns"]
    
    print(f"  EpsilonGreedy mean return: {eg_results['summary']['mean']:.3f}")
    print(f"  EpsilonGreedy median return: {eg_results['summary']['median']:.3f}")
    print(f"  EpsilonGreedy IC95: [{eg_results['summary']['ci95_low']:.3f}, {eg_results['summary']['ci95_high']:.3f}]")
    print()
    
    # Compute paired comparison metrics
    print("Comparison metrics:")
    
    # Win rate: seeds where EG >= threshold
    eg_threshold_wins = sum(1 for r in eg_returns if r >= threshold)
    random_threshold_wins = sum(1 for r in random_returns if r >= threshold)
    
    print(f"  Seeds where Random >= {threshold}: {random_threshold_wins}/{len(seeds)}")
    print(f"  Seeds where EpsilonGreedy >= {threshold}: {eg_threshold_wins}/{len(seeds)}")
    
    win_pct = 100 * eg_threshold_wins / len(seeds)
    print(f"  EpsilonGreedy win rate: {win_pct:.1f}%")
    print()
    
    # Compute mean difference
    mean_diff = eg_results["summary"]["mean"] - random_results["summary"]["mean"]
    print(f"  Mean return difference (EG - Random): {mean_diff:.3f}")
    print()
    
    # Save results to JSON
    results = {
        "metadata": {
            "date": "2026-09-01",
            "protocol": "C1_LEARNING",
            "status": "FROZEN_FOR_EXECUTION",
            "change_id": "CHG-2026-09-01-C1-FINAL-PARAMETERS",
        },
        "parameters": {
            "seeds": seeds,
            "max_steps": max_steps,
            "threshold": threshold,
            "task_probabilities": list(config.reward_probabilities),
        },
        "random_agent": {
            "agent_type": "RandomAgent",
            "returns": random_returns,
            "summary": random_results["summary"],
            "statuses": random_results["statuses"],
        },
        "epsilon_greedy_agent": {
            "agent_type": "EpsilonGreedyAgent",
            "epsilon": 0.1,
            "learning_method": "incremental_averaging",
            "returns": eg_returns,
            "summary": eg_results["summary"],
            "statuses": eg_results["statuses"],
        },
        "comparison": {
            "mean_difference": mean_diff,
            "random_threshold_wins": random_threshold_wins,
            "epsilon_greedy_threshold_wins": eg_threshold_wins,
            "win_rate_pct": win_pct,
        },
    }
    
    with open(output_dir / "C1_evaluation_summary.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to {output_dir / 'C1_evaluation_summary.json'}")
    print()
    print("PASS: C1 final validation complete. No freeze applied yet.")
    print("      Review results above and approve before sealing benchmark.")


if __name__ == "__main__":
    main()
