from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest


class GovernanceTests(unittest.TestCase):
    def test_governance_check_passes(self) -> None:
        root = Path(__file__).resolve().parents[1]
        completed = subprocess.run(
            [sys.executable, str(root / "scripts" / "check_governance.py")],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("governance checks passed", completed.stdout)


if __name__ == "__main__":
    unittest.main()
