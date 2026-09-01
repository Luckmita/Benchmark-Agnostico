"""Public contracts for the benchmark core."""

from .manifest import AgentManifest, check_determinism, validate_specification
from .episode import EpisodeResult, run_episode
from .evaluation import evaluate_agent
from .metrics import SummaryStatistics, paired_effect_size, steps_to_threshold, summarize, trapezoidal_auc, win_rate
from .artifacts import ArtifactStore
from .protocol import AgentCapabilities, AgentProtocolError, AgentSpecification, Transition, validate_agent
from .registry import RunRecord, RunRegistry, hash_file, hash_json
from .runner import RunResult, record_result, run_action
from .run import execute_run

__all__ = [
    "AgentCapabilities",
    "AgentManifest",
    "AgentProtocolError",
    "AgentSpecification",
    "ArtifactStore",
    "EpisodeResult",
    "evaluate_agent",
    "RunRecord",
    "RunRegistry",
    "Transition",
    "check_determinism",
    "execute_run",
    "hash_file",
    "hash_json",
    "record_result",
    "run_action",
    "run_episode",
    "RunResult",
    "SummaryStatistics",
    "paired_effect_size",
    "steps_to_threshold",
    "summarize",
    "trapezoidal_auc",
    "validate_specification",
    "win_rate",
    "validate_agent",
]
