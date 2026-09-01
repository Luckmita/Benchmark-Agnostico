from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


class CliTests(unittest.TestCase):
    def test_public_c1_run_is_traceable(self) -> None:
        with TemporaryDirectory() as directory:
            output_root = Path(directory) / "public-run"
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "benchmark_core.cli",
                    "run-public-c1",
                    "--output-root",
                    str(output_root),
                    "--run-id",
                    "cli-c1-seed-7",
                    "--seed",
                    "7",
                    "--max-steps",
                    "3",
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(completed.stdout.strip())
            self.assertEqual(result["run_id"], "cli-c1-seed-7")
            run_root = output_root / "artifacts" / "cli-c1-seed-7"
            for group in ("raw", "derived", "logs", "metrics", "manifest"):
                self.assertTrue((run_root / group).is_dir())
            registry_record = json.loads((output_root / "registry.jsonl").read_text(encoding="utf-8"))
            self.assertEqual(registry_record["run_id"], "cli-c1-seed-7")
            self.assertEqual(len(registry_record["benchmark_code_hash"]), 64)


if __name__ == "__main__":
    unittest.main()
