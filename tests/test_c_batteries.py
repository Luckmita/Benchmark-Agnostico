"""Contract tests for public, non-sealed C2-C9 development prototypes."""

from __future__ import annotations

import pytest

from benchmark_core.tasks import (
    PUBLIC_CAPACITY_NAMES,
    C1BanditConfig,
    C1BanditEnvironment,
    C2SampleEfficiencyConfig,
    C3GeneralizationConfig,
    C4AdaptationConfig,
    C4AdaptationEnvironment,
    C5TemporalDependencyConfig,
    C5TemporalDependencyEnvironment,
    C6PlanningConfig,
    C6PlanningEnvironment,
    C7ContinualLearningConfig,
    C8MissingObservationWrapper,
    C8RobustnessConfig,
    C9DomainSpec,
    C9MultidomainTransferConfig,
    forgetting_from_performance_matrix,
)


def test_capacity_ids_match_normative_taxonomy() -> None:
    assert PUBLIC_CAPACITY_NAMES == {
        "C1": "learning",
        "C2": "sample_efficiency",
        "C3": "generalization",
        "C4": "adaptation",
        "C5": "temporal_dependency",
        "C6": "planning",
        "C7": "continual_learning",
        "C8": "robustness",
        "C9": "multidomain_transfer",
        "C10": "uncertainty",
        "C11": "computational_efficiency",
    }


def test_c2_checkpoints_are_ordered_inside_c1_budget() -> None:
    C2SampleEfficiencyConfig().validate()
    with pytest.raises(ValueError, match="budget"):
        C2SampleEfficiencyConfig(C1BanditConfig(max_steps=20), (10, 25)).validate()


def test_c3_exposes_four_distinct_generalization_levels() -> None:
    partitions = C3GeneralizationConfig().partitions()
    assert tuple(partitions) == ("TRAIN", "ID_HELDOUT", "OOD", "STRUCTURAL_TRANSFER")
    assert partitions["TRAIN"]["encoding"] != partitions["STRUCTURAL_TRANSFER"]["encoding"]


def test_c4_changes_distribution_without_observation_flag() -> None:
    environment = C4AdaptationEnvironment(C4AdaptationConfig(change_at_step=2, max_steps=4))
    assert environment.reset(7) == 0
    phases = [environment.step(1)[4]["phase"] for _ in range(4)]
    assert phases == ["pre", "pre", "post", "post"]


def test_c5_delays_decision_until_cue_is_no_longer_observable() -> None:
    environment = C5TemporalDependencyEnvironment(C5TemporalDependencyConfig(delay=2))
    cue = environment.reset(3)
    first_observation, first_reward, first_done, _, _ = environment.step(1 - cue)
    assert first_observation == -1
    assert first_reward == 0.0
    assert not first_done
    environment.step(1 - cue)
    _observation, final_reward, final_done, _, info = environment.step(cue)
    assert final_done and info["decision"]
    assert final_reward == 1.0


def _planning_return(first_action: int) -> float:
    environment = C6PlanningEnvironment(C6PlanningConfig(horizon=3))
    environment.reset(1)
    total = 0.0
    done = False
    action = first_action
    while not done:
        _observation, reward, done, _, _info = environment.step(action)
        total += reward
        action = 0
    return total


def test_c6_separates_myopic_reward_from_better_delayed_return() -> None:
    assert _planning_return(0) < _planning_return(1)


def test_c7_reports_forgetting_per_retested_task() -> None:
    C7ContinualLearningConfig().validate()
    forgetting = forgetting_from_performance_matrix([[0.8], [0.7, 0.9], [0.6, 0.8, 0.85]])
    assert forgetting == pytest.approx((0.2, 0.1, 0.0))


def test_c8_missing_wrapper_changes_observation_not_reward() -> None:
    base = C1BanditEnvironment(C1BanditConfig(reward_probabilities=(1.0, 0.0), max_steps=1))
    wrapper = C8MissingObservationWrapper(base, C8RobustnessConfig(missing_probability=1.0))
    assert wrapper.reset(1) == "MISSING"
    observation, reward, done, _, _ = wrapper.step(0)
    assert observation == "MISSING"
    assert reward == 1.0
    assert done


def test_c9_requires_distinct_domains_and_one_frozen_core_hash() -> None:
    config = C9MultidomainTransferConfig(
        domains=(
            C9DomainSpec("grid", "discrete", "grid-v1", "enum-v1"),
            C9DomainSpec("control", "continuous", "vector-v1", "float-v1"),
        ),
        core_hash="sha256:" + "a" * 64,
    )
    config.validate()
    invalid = C9MultidomainTransferConfig((config.domains[0], config.domains[0]), core_hash="hash")
    with pytest.raises(ValueError, match="distinct"):
        invalid.validate()
