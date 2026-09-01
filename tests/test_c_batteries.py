"""Tests for C2-C11 capacity batteries."""

import pytest

from benchmark_core.tasks import (
    C2SampleEfficiencyConfig,
    C3RobustnessConfig,
    C5DynamicChangeConfig,
    C5DynamicEnvironment,
    C6AdversarialConfig,
    C10ExpandedActionConfig,
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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
