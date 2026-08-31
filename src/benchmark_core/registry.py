"""Append-only registry records for reproducible benchmark runs."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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
