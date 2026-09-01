"""Command-line entry points for public reproducibility workflows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import platform
import sys
from typing import Callable

from .manifest import AgentManifest
from .protocol import AgentCapabilities, AgentProtocol, AgentSpecification
from .registry import RunRegistry, hash_json
from .run import execute_run
from .tasks import C1BanditConfig, C1BanditEnvironment, EpsilonGreedyAgent, RandomAgent


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="benchmark-cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    hash_parser = subparsers.add_parser("hash-json", help="hash canonical JSON")
    hash_parser.add_argument("value", nargs="?", help="JSON value; defaults to stdin")

    run_parser = subparsers.add_parser("run-public-c1", help="execute one traceable public C1 development run")
    run_parser.add_argument("--output-root", type=Path, required=True)
    run_parser.add_argument("--run-id", required=True)
    run_parser.add_argument("--seed", type=int, required=True)
    run_parser.add_argument("--max-steps", type=int, default=100)
    run_parser.add_argument("--agent", choices=("random", "epsilon-greedy"), default="epsilon-greedy")
    return parser


def _run_public_c1(args: argparse.Namespace) -> int:
    if args.seed < 0:
        print("seed must be non-negative", file=sys.stderr)
        return 2
    if args.max_steps <= 0:
        print("max-steps must be positive", file=sys.stderr)
        return 2

    online_learning = args.agent == "epsilon-greedy"
    capabilities = AgentCapabilities(online_learning=online_learning)
    factory: Callable[[], AgentProtocol] = EpsilonGreedyAgent if online_learning else RandomAgent
    agent_id = "public-epsilon-greedy-baseline" if online_learning else "public-random-control"
    task_config = C1BanditConfig(max_steps=args.max_steps)
    config = {
        "status": "PUBLIC_DEVELOPMENT_ONLY",
        "capacity": "C1",
        "agent": {"name": args.agent, "epsilon": 0.1 if online_learning else None},
        "environment": {
            "name": "C1BanditEnvironment",
            "reward_probabilities": list(task_config.reward_probabilities),
            "max_steps": task_config.max_steps,
        },
        "seed": args.seed,
    }
    manifest = AgentManifest(
        manifest_version="1.0",
        agent_id=agent_id,
        implementation_version="0.1.0",
        capabilities=capabilities,
        entrypoint=f"benchmark_core.tasks.{factory.__name__}",
        training_provenance="public-control-no-pretraining",
        hardware_requirements="cpu",
        declared_timeout_seconds=max(5.0, args.max_steps * 0.1),
    )
    output_root = args.output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    status = execute_run(
        factory,
        C1BanditEnvironment(task_config),
        AgentSpecification("constant-zero", "integer-{0,1}", args.seed, capabilities),
        manifest,
        run_id=args.run_id,
        benchmark_version="0.1.0-development",
        scenario="C1-public-bandit-development",
        artifact_root=output_root / "artifacts",
        registry=RunRegistry(output_root / "registry.jsonl"),
        config=config,
        hardware=f"{platform.system()}-{platform.machine()}",
        software=f"Python-{platform.python_version()}",
        max_steps=args.max_steps,
    )
    print(json.dumps({"run_id": args.run_id, "status": status, "output_root": str(output_root)}, sort_keys=True))
    return 0 if status in {"PASS", "MAX_STEPS"} else 1


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.command == "hash-json":
        value_text = args.value if args.value is not None else sys.stdin.read()
        try:
            value = json.loads(value_text)
        except json.JSONDecodeError as error:
            print(f"invalid JSON: {error}", file=sys.stderr)
            return 2
        print(hash_json(value))
        return 0
    if args.command == "run-public-c1":
        return _run_public_c1(args)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
