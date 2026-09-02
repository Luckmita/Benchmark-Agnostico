"""Append-only registry records for reproducible benchmark runs."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from dataclasses import asdict, dataclass
from datetime import timezone
from pathlib import Path
import re
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

    def validate(self) -> None:
        validate_run_id(self.run_id)
        for field_name in (
            "timestamp",
            "benchmark_version",
            "environment",
            "scenario",
            "submission",
            "model_hash",
            "adapter_hash",
            "config_hash",
            "hardware",
            "software",
            "start_time",
            "end_time",
            "status",
            "benchmark_code_hash",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if not isinstance(self.seed, int) or isinstance(self.seed, bool) or self.seed < 0:
            raise ValueError("seed must be a non-negative integer")
        if self.status not in {"PASS", "ERROR", "TIMEOUT", "INVALID_ACTION", "MAX_STEPS"}:
            raise ValueError("unknown run status")
        timestamp = _parse_timestamp(self.timestamp, "timestamp")
        start_time = _parse_timestamp(self.start_time, "start_time")
        end_time = _parse_timestamp(self.end_time, "end_time")
        if end_time < start_time:
            raise ValueError("end_time cannot precede start_time")
        if timestamp < start_time:
            raise ValueError("registry timestamp cannot precede start_time")
        for field_name in ("model_hash", "adapter_hash", "config_hash", "benchmark_code_hash"):
            _validate_hash(getattr(self, field_name), field_name)

    @classmethod
    def create(cls, **values: Any) -> "RunRecord":
        now = datetime.now(timezone.utc).isoformat()
        values.setdefault("timestamp", now)
        values.setdefault("start_time", now)
        values.setdefault("end_time", now)
        return cls(**values)

    def to_json(self) -> str:
        self.validate()
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))


class RunRegistry:
    """Append-only JSONL registry; existing records are never rewritten."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._claims = self.path.parent / f".{self.path.name}.run_ids"
        self._claims.mkdir(parents=True, exist_ok=True)

    def append(self, record: RunRecord) -> None:
        payload = record.to_json()
        if self.contains(record.run_id):
            raise ValueError(f"duplicate run_id: {record.run_id}")
        claim = self._claims / f"{record.run_id}.claim"
        try:
            with claim.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(record.run_id + "\n")
        except FileExistsError as error:
            raise ValueError(f"duplicate run_id: {record.run_id}") from error
        try:
            with self.path.open("a", encoding="utf-8", newline="\n") as stream:
                stream.write(payload + "\n")
                stream.flush()
        except Exception:
            claim.unlink(missing_ok=True)
            raise

    def contains(self, run_id: str) -> bool:
        validate_run_id(run_id)
        claim = self._claims / f"{run_id}.claim"
        if claim.exists():
            return True
        if not self.path.exists():
            return False
        with self.path.open("r", encoding="utf-8") as stream:
            for line in stream:
                if not line.strip():
                    continue
                try:
                    if json.loads(line).get("run_id") == run_id:
                        return True
                except json.JSONDecodeError as error:
                    raise ValueError("registry contains invalid JSONL") from error
        return False


def hash_json(value: Any) -> str:
    """Hash canonical JSON for configs and manifests."""

    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
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


def validate_run_id(run_id: str) -> None:
    if not isinstance(run_id, str) or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", run_id) is None:
        raise ValueError("run_id must be 1-128 portable characters: letters, digits, dot, underscore or hyphen")


def _parse_timestamp(value: str, field_name: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"{field_name} must be an ISO-8601 timestamp") from error
    if parsed.tzinfo is None:
        raise ValueError(f"{field_name} must include a timezone")
    return parsed


def _validate_hash(value: str, field_name: str) -> None:
    if value in {"unknown", "not-applicable", "not-provided"}:
        return
    if re.fullmatch(r"(?:sha256:)?[0-9a-f]{64}", value) is None:
        raise ValueError(f"{field_name} must be a SHA-256 digest or explicit sentinel")
