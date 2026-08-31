"""Public contracts for the benchmark core."""

from .manifest import AgentManifest, check_determinism, validate_specification
from .episode import EpisodeResult, run_episode
from .artifacts import ArtifactStore
from .protocol import AgentCapabilities, AgentProtocolError, AgentSpecification, Transition, validate_agent
from .registry import RunRecord, RunRegistry, hash_file, hash_json
from .runner import RunResult, record_result, run_action

__all__ = [
    "AgentCapabilities",
    "AgentManifest",
    "AgentProtocolError",
    "AgentSpecification",
    "ArtifactStore",
    "EpisodeResult",
    "RunRecord",
    "RunRegistry",
    "Transition",
    "check_determinism",
    "hash_file",
    "hash_json",
    "record_result",
    "run_action",
    "run_episode",
    "RunResult",
    "validate_specification",
    "validate_agent",
]
