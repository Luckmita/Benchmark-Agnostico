"""Structured, non-destructive storage for run artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .registry import validate_run_id

ARTIFACT_GROUPS = ("raw", "derived", "logs", "metrics", "manifest")


class ArtifactStore:
    """Keep raw and derived artifacts in separate run-scoped directories."""

    def __init__(self, root: Path, run_id: str) -> None:
        validate_run_id(run_id)
        if root.is_symlink():
            raise ValueError("artifact root cannot be a symlink")
        self.root = root / run_id
        if self.root.is_symlink():
            raise ValueError("run directory cannot be a symlink")
        for group in ARTIFACT_GROUPS:
            directory = self.root / group
            if directory.is_symlink():
                raise ValueError("artifact directories cannot be symlinks")
            directory.mkdir(parents=True, exist_ok=True)
            if directory.is_symlink() or not directory.is_dir():
                raise ValueError("artifact directory is not a regular directory")

    def write_json(self, group: str, name: str, value: Any, *, overwrite: bool = False) -> Path:
        if group not in ARTIFACT_GROUPS:
            raise ValueError(f"unknown artifact group: {group}")
        if not name or Path(name).name != name or name in {".", ".."}:
            raise ValueError("artifact name must be a path-safe filename")
        path = (self.root / group / name).with_suffix(".json")
        if path.parent.resolve() != (self.root / group).resolve() or path.is_symlink():
            raise ValueError("artifact path must remain inside its group")
        if overwrite and group == "raw":
            raise ValueError("raw artifacts are immutable")
        payload = json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False) + "\n"
        mode = "w" if overwrite else "x"
        with path.open(mode, encoding="utf-8", newline="\n") as stream:
            stream.write(payload)
            stream.flush()
        return path
