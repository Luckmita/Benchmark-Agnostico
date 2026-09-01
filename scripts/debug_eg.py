#!/usr/bin/env python3
"""Debug EpsilonGreedy specifically."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.benchmark_core.tasks import C1BanditConfig, C1BanditEnvironment, EpsilonGreedyAgent
from src.benchmark_core.episode import run_episode
from src.benchmark_core.protocol import AgentSpecification, AgentCapabilities
from src.benchmark_core.manifest import AgentManifest


def test_eg() -> None:
    """Test EpsilonGreedy episode."""
    
    config = C1BanditConfig(reward_probabilities=(0.2, 0.8), max_steps=100)
    env = C1BanditEnvironment(config)
    
    spec = AgentSpecification(
        observation_space="discrete",
        action_space="discrete",
        seed=42,
        capabilities=AgentCapabilities(online_learning=True),  # EG has online learning
    )
    
    manifest = AgentManifest(
        manifest_version="1.0",
        agent_id="C1_EG_Debug",
        implementation_version="1.0",
        declared_timeout_seconds=5.0,
    )
    
    print("Creating EpsilonGreedy agent...")
    agent = EpsilonGreedyAgent(epsilon=0.1)
    print(f"  Agent type: {type(agent)}")
    print(f"  Agent methods: {[m for m in dir(agent) if not m.startswith('_')]}")
    
    print("\nRunning episode with factory...")
    
    def eg_factory() -> EpsilonGreedyAgent:
        return EpsilonGreedyAgent(epsilon=0.1, alpha=0.1)
    
    result = run_episode(
        factory=eg_factory,
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


if __name__ == "__main__":
    test_eg()
