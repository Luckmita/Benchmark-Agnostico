from __future__ import annotations

import unittest

from benchmark_core import measure_callable


class ResourceMeasurementTests(unittest.TestCase):
    def test_measure_callable_reports_local_scope_and_result(self) -> None:
        measurement = measure_callable(lambda left, right: left + right, 2, 3)
        self.assertEqual(measurement.result, 5)
        self.assertGreaterEqual(measurement.wall_seconds, 0.0)
        self.assertGreaterEqual(measurement.cpu_seconds, 0.0)
        self.assertGreaterEqual(measurement.python_peak_bytes, 0)
        self.assertEqual(measurement.scope, "current-process-python-allocations")


if __name__ == "__main__":
    unittest.main()
