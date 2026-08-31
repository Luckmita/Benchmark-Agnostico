"""Structured, non-destructive storage for run artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ARTIFACT_GROUPS = ("raw", "derived", "logs", "metrics", "manifest")


class ArtifactStore:
    """Keep raw and derived artifacts in separate run-scoped directories."""

    def __init__(self, root: Path, run_id: str) -> None:
        if not run_id or "/" in run_id or "\\" in run_id or run_id in {".", ".."}:
            raise ValueError("run_id must be a non-empty path-safe identifier")
        self.root = root / run_id
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
        if path.exists() and not overwrite:
            raise FileExistsError(path)
        path.write_text(
            json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n",
            encoding="utf-8",
        )
        return path
