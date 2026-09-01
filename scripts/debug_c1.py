#!/usr/bin/env python3
"""Debug C1 evaluation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.benchmark_core.tasks import C1BanditConfig, C1BanditEnvironment, RandomAgent
from src.benchmark_core.episode import run_episode
from src.benchmark_core.protocol import AgentSpecification, AgentCapabilities
from src.benchmark_core.manifest import AgentManifest


def test_single_episode() -> None:
    """Test a single episode to debug return accumulation."""
    
    config = C1BanditConfig(reward_probabilities=(0.2, 0.8), max_steps=100)
    env = C1BanditEnvironment(config)
    
    spec = AgentSpecification(
        observation_space="discrete",
        action_space="discrete",
        seed=42,
        capabilities=AgentCapabilities(),
    )
    
    manifest = AgentManifest(
        manifest_version="1.0",
        agent_id="C1_Random_Debug",
        implementation_version="1.0",
        declared_timeout_seconds=5.0,
    )
    
    print("Running single episode with RandomAgent...")
    result = run_episode(
        factory=RandomAgent,
        environment=env,
        specification=spec,
        manifest=manifest,
        max_steps=100,
    )
    
    print(f"Episode result:")
    print(f"  Status: {result.status}")
    print(f"  Total reward: {result.total_reward}")
    print(f"  Steps: {result.steps}")
    print(f"  Error: {result.error}")
    print(f"  Action results count: {len(result.action_results)}")


if __name__ == "__main__":
    test_single_episode()
