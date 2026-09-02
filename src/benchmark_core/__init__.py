"""Public contracts for the benchmark core."""

from .manifest import AgentManifest, check_determinism, validate_contract, validate_specification
from .episode import EpisodeResult, run_episode
from .evaluation import evaluate_agent
from .metrics import (
    SummaryStatistics,
    brier_score,
    evaluate_uncertainty,
    expected_calibration_error,
    paired_effect_size,
    selective_accuracy,
    steps_to_threshold,
    summarize,
    trapezoidal_auc,
    win_rate,
)
from .artifacts import ArtifactStore
from .protocol import AgentCapabilities, AgentDecision, AgentProtocolError, AgentSpecification, Transition, validate_agent
from .registry import RunRecord, RunRegistry, hash_file, hash_json, hash_paths, hash_source_tree, validate_run_id
from .runner import RunResult, record_result, run_action
from .run import execute_run
from .resources import ResourceMeasurement, measure_callable

__all__ = [
    "AgentCapabilities",
    "AgentDecision",
    "AgentManifest",
    "AgentProtocolError",
    "AgentSpecification",
    "ArtifactStore",
    "brier_score",
    "EpisodeResult",
    "evaluate_agent",
    "evaluate_uncertainty",
    "expected_calibration_error",
    "RunRecord",
    "RunRegistry",
    "Transition",
    "check_determinism",
    "execute_run",
    "hash_file",
    "hash_json",
    "hash_paths",
    "hash_source_tree",
    "record_result",
    "ResourceMeasurement",
    "run_action",
    "run_episode",
    "RunResult",
    "SummaryStatistics",
    "selective_accuracy",
    "paired_effect_size",
    "steps_to_threshold",
    "summarize",
    "trapezoidal_auc",
    "validate_specification",
    "validate_run_id",
    "win_rate",
    "validate_agent",
    "validate_contract",
    "measure_callable",
]
