from __future__ import annotations

import json
from pathlib import Path
import unittest

from benchmark_core import AgentManifest


class ManifestSchemaTests(unittest.TestCase):
    def test_python_manifest_serialization_covers_json_schema_required_fields(self) -> None:
        schema_path = Path(__file__).resolve().parents[1] / "schemas" / "agent_manifest.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        serialized = AgentManifest("1", "baseline", "1").to_dict()
        self.assertEqual(set(schema["required"]) - set(serialized), set())
        self.assertEqual(set(serialized) - set(schema["properties"]), set())


if __name__ == "__main__":
    unittest.main()
