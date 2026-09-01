"""Tests for C2-C11 capacity batteries."""

import pytest

from benchmark_core.tasks import (
    C2SampleEfficiencyConfig,
    C3RobustnessConfig,
    C4GeneralizationConfig,
    C5DynamicChangeConfig,
    C5DynamicEnvironment,
    C6AdversarialConfig,
    C7InterpretabilityConfig,
    C7InterpretabilityTracker,
    C8CompositionConfig,
    C8CompositionEnvironment,
    C9MultiagentConfig,
    C9MultiagentEnvironment,
    C10ExpandedActionConfig,
    C11AuditConfig,
    C11AuditEnvironment,
    CExpandedBanditEnvironment,
)


def test_c2_config_instantiates() -> None:
    """C2: Sample efficiency config can be created."""
    config = C2SampleEfficiencyConfig()
    assert config.threshold_percentile == 0.75


def test_c3_config_robustness() -> None:
    """C3: Robustness config uses variant probabilities."""
    config = C3RobustnessConfig()
    assert config.base_config.reward_probabilities == (0.3, 0.7)


def test_c4_generalization_config() -> None:
    """C4: Generalization config defines train/test split."""
    config = C4GeneralizationConfig()
    assert config.train_fraction == 0.8


def test_c5_dynamic_environment_switches() -> None:
    """C5: Dynamic environment switches probabilities mid-episode."""
    config = C5DynamicChangeConfig(
        initial_probabilities=(0.2, 0.8),
        switch_at_step=50,
        final_probabilities=(0.7, 0.3),
        max_steps=100,
    )
    env = C5DynamicEnvironment(config)
    obs = env.reset(42)
    assert obs == 0

    # Run until switch
    for _ in range(49):
        obs, reward, terminated, truncated, info = env.step(1)
        assert 0 <= reward <= 1.0
        assert not terminated

    # At step 50, switch happens
    obs, reward, terminated, truncated, info = env.step(1)
    assert not terminated

    # Continue to end
    while not terminated:
        obs, reward, terminated, truncated, info = env.step(1)


def test_c6_config_adversarial() -> None:
    """C6: Adversarial config inverts probabilities."""
    config = C6AdversarialConfig()
    assert config.base_config.reward_probabilities == (0.8, 0.2)


def test_c7_interpretability_tracker() -> None:
    """C7: Interpretability tracker measures decision complexity."""
    config = C7InterpretabilityConfig()
    tracker = C7InterpretabilityTracker(config)
    tracker.reset(42)
    
    # Make deterministic decisions on action 1
    for _ in range(10):
        obs, reward, terminated, truncated, info = tracker.step(1)
        if terminated:
            break
    
    complexity = tracker.decision_complexity()
    assert complexity == 0.0  # Only 1 unique action


def test_c7_interpretability_mixed_decisions() -> None:
    """C7: Interpretability tracks mixed decision complexity."""
    tracker = C7InterpretabilityTracker()
    tracker.reset(42)
    
    # Alternate between actions
    for i in range(10):
        obs, reward, terminated, truncated, info = tracker.step(i % 2)
        if terminated:
            break
    
    complexity = tracker.decision_complexity()
    assert complexity == 1.0  # 2 unique actions


def test_c8_composition_phase_change() -> None:
    """C8: Composition environment switches phases mid-episode."""
    config = C8CompositionConfig(
        phase1_probabilities=(0.2, 0.8),
        phase2_probabilities=(0.4, 0.6),  # Different probabilities
        steps_per_phase=10,
    )
    env = C8CompositionEnvironment(config)
    env.reset(42)
    
    phases_seen = set()
    for i in range(25):
        obs, reward, terminated, truncated, info = env.step(1)
        phases_seen.add(info["phase"])
        if terminated:
            break
    
    assert len(phases_seen) <= 2


def test_c9_multiagent_environment() -> None:
    """C9: Multiagent environment accepts actions for multiple agents."""
    config = C9MultiagentConfig(num_agents=2, num_actions=2)
    env = C9MultiagentEnvironment(config)
    env.reset(42)
    
    obs, rewards, terminated, truncated, info = env.step([0, 1])
    assert len(rewards) == 2
    assert all(0 <= r <= 1.0 for r in rewards)


def test_c9_multiagent_action_validation() -> None:
    """C9: Multiagent environment validates action count."""
    env = C9MultiagentEnvironment()
    env.reset(42)
    
    with pytest.raises(ValueError):
        env.step([0, 1, 2])  # Too many actions


def test_c10_expanded_bandit_instantiates() -> None:
    """C10: Expanded bandit environment with 4 actions."""
    config = C10ExpandedActionConfig(num_actions=4)
    env = CExpandedBanditEnvironment(config)
    obs = env.reset(42)
    assert obs == 0


def test_c10_expanded_bandit_validates_action() -> None:
    """C10: Expanded bandit validates action range."""
    config = C10ExpandedActionConfig(num_actions=4)
    env = CExpandedBanditEnvironment(config)
    env.reset(42)

    # Valid action
    obs, reward, terminated, truncated, info = env.step(0)
    assert 0 <= reward <= 1.0

    # Invalid action
    with pytest.raises(ValueError):
        env.step(4)  # Out of range

    with pytest.raises(ValueError):
        env.step(-1)  # Negative


def test_c10_expanded_bandit_runs_episode() -> None:
    """C10: Expanded bandit runs full episode."""
    config = C10ExpandedActionConfig(num_actions=4, max_steps=10)
    env = CExpandedBanditEnvironment(config)
    env.reset(42)

    for i in range(10):
        obs, reward, terminated, truncated, info = env.step(i % 4)
        if i == 9:
            assert terminated
        else:
            assert not terminated


def test_c11_audit_environment_tracks_trajectory() -> None:
    """C11: Audit environment tracks full trajectory."""
    config = C11AuditConfig()
    env = C11AuditEnvironment(config)
    env.reset(42)
    
    for _ in range(10):
        obs, reward, terminated, truncated, info = env.step(1)
        if terminated:
            break
    
    trajectory = env.get_trajectory()
    assert len(trajectory) > 0
    assert "action" in trajectory[1]  # Second entry has action
    assert trajectory[0]["action"] is None  # First is reset


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

