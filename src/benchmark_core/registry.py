"""Append-only registry records for reproducible benchmark runs."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class RunRecord:
    run_id: str
    timestamp: str
    benchmark_version: str
    environment: str
    scenario: str
    seed: int
    submission: str
    model_hash: str
    adapter_hash: str
    config_hash: str
    hardware: str
    software: str
    start_time: str
    end_time: str
    status: str
    benchmark_code_hash: str = "unknown"

    @classmethod
    def create(cls, **values: Any) -> "RunRecord":
        now = datetime.now(timezone.utc).isoformat()
        values.setdefault("timestamp", now)
        values.setdefault("start_time", now)
        values.setdefault("end_time", now)
        return cls(**values)

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))


class RunRegistry:
    """Append-only JSONL registry; existing records are never rewritten."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, record: RunRecord) -> None:
        with self.path.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(record.to_json() + "\n")


def hash_json(value: Any) -> str:
    """Hash canonical JSON for configs and manifests."""

    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def hash_paths(paths: Iterable[Path], *, base: Path) -> str:
    """Hash file names and contents in a stable order relative to base."""

    resolved_base = base.resolve()
    normalized: list[tuple[str, Path]] = []
    for path in paths:
        resolved = path.resolve()
        try:
            relative = resolved.relative_to(resolved_base).as_posix()
        except ValueError as error:
            raise ValueError("all hashed paths must remain inside base") from error
        if not resolved.is_file() or resolved.is_symlink():
            raise ValueError("hashed paths must be regular non-symlink files")
        normalized.append((relative, resolved))
    digest = hashlib.sha256()
    for relative, path in sorted(normalized):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        digest.update(b"\0")
    return digest.hexdigest()


def hash_source_tree() -> str:
    """Hash the installed benchmark_core Python source tree."""

    root = Path(__file__).resolve().parent
    return hash_paths(root.rglob("*.py"), base=root)
