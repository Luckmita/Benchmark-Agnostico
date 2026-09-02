from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest


class LegacyScriptTests(unittest.TestCase):
    def test_superseded_freeze_scripts_fail_closed(self) -> None:
        root = Path(__file__).resolve().parents[1]
        for name in (
            "run_c1_final_validation.py",
            "run_c2_sample_efficiency.py",
            "run_c3_c11_batch.py",
            "validate_capacity.py",
        ):
            completed = subprocess.run(
                [sys.executable, str(root / "scripts" / name)],
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertIn("disabled", completed.stderr)


if __name__ == "__main__":
    unittest.main()
