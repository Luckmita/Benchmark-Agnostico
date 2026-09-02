from __future__ import annotations

import json
from pathlib import Path
import unittest

from benchmark_core.tasks import PUBLIC_CAPACITY_NAMES


class CapacityTaxonomyTests(unittest.TestCase):
    def test_public_config_matches_runtime_taxonomy(self) -> None:
        path = Path(__file__).resolve().parents[1] / "configs" / "public" / "capacity_taxonomy.json"
        config = json.loads(path.read_text(encoding="utf-8"))
        configured = {item["id"]: item["name"] for item in config["capacities"]}
        self.assertEqual(configured, PUBLIC_CAPACITY_NAMES)
        self.assertEqual(config["status"], "B1_APPROVED_PUBLIC_TAXONOMY")


if __name__ == "__main__":
    unittest.main()
