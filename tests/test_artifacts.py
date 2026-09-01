from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from benchmark_core import ArtifactStore


class ArtifactTests(unittest.TestCase):
    def test_store_creates_all_groups_and_keeps_existing_json(self) -> None:
        with TemporaryDirectory() as directory:
            store = ArtifactStore(Path(directory), "run-1")
            path = store.write_json("raw", "observations", {"value": 1})
            self.assertEqual(path.read_text(encoding="utf-8"), '{\n  "value": 1\n}\n')
            with self.assertRaises(FileExistsError):
                store.write_json("raw", "observations", {"value": 2})
            for group in ("raw", "derived", "logs", "metrics", "manifest"):
                self.assertTrue((Path(directory) / "run-1" / group).is_dir())

    def test_path_unsafe_run_id_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                ArtifactStore(Path(directory), "../escape")

    def test_path_unsafe_artifact_name_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            store = ArtifactStore(Path(directory), "run-1")
            with self.assertRaises(ValueError):
                store.write_json("raw", "../escape", {})

    def test_symlinked_group_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            run_root = root / "run-1"
            run_root.mkdir()
            try:
                (run_root / "raw").symlink_to(root / "outside", target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable in this environment")
            with self.assertRaises(ValueError):
                ArtifactStore(root, "run-1")

    def test_symlinked_run_directory_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "outside").mkdir()
            try:
                (root / "run-1").symlink_to(root / "outside", target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable in this environment")
            with self.assertRaises(ValueError):
                ArtifactStore(root, "run-1")

    def test_symlinked_artifact_root_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            base = Path(directory)
            (base / "outside").mkdir()
            root = base / "artifacts"
            try:
                root.symlink_to(base / "outside", target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable in this environment")
            with self.assertRaises(ValueError):
                ArtifactStore(root, "run-1")


if __name__ == "__main__":
    unittest.main()
