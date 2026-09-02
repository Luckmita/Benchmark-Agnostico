from __future__ import annotations

import unittest

from benchmark_core.metrics import (
    brier_score,
    evaluate_uncertainty,
    expected_calibration_error,
    paired_effect_size,
    selective_accuracy,
    steps_to_threshold,
    summarize,
    trapezoidal_auc,
    win_rate,
)


class MetricsTests(unittest.TestCase):
    def test_summary_contains_distribution_and_ci(self) -> None:
        result = summarize([1, 2, 3, 4])
        self.assertEqual(result.count, 4)
        self.assertEqual(result.mean, 2.5)
        self.assertLess(result.ci95_low, result.mean)
        self.assertGreater(result.ci95_high, result.mean)

    def test_paired_comparison_metrics(self) -> None:
        self.assertEqual(win_rate([2, 3, 4], [1, 3, 2]), 2 / 3)
        self.assertGreater(paired_effect_size([4, 5, 6], [1, 2, 1]), 0)

    def test_auc_and_threshold(self) -> None:
        self.assertEqual(trapezoidal_auc([0, 2, 4]), 4.0)
        self.assertEqual(steps_to_threshold([0.1, 0.4, 0.8], 0.5), 3)
        self.assertIsNone(steps_to_threshold([0.1, 0.4], 0.5))

    def test_uncertainty_metrics_reward_calibrated_predictions(self) -> None:
        outcomes = [0, 0, 1, 1]
        probabilities = [0.0, 0.1, 0.9, 1.0]
        self.assertLess(brier_score(outcomes, probabilities), 0.01)
        self.assertLess(expected_calibration_error(outcomes, probabilities, bins=2), 0.1)
        accuracy, coverage = selective_accuracy(outcomes, probabilities, minimum_confidence=0.8)
        self.assertEqual(accuracy, 1.0)
        self.assertEqual(coverage, 1.0)

    def test_uncertainty_can_be_not_supported_without_failure(self) -> None:
        result = evaluate_uncertainty([0, 1], None)
        self.assertEqual(result["status"], "NOT_SUPPORTED")
        self.assertIsNone(result["brier"])

    def test_empty_inputs_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            summarize([])
        with self.assertRaises(ValueError):
            trapezoidal_auc([])


if __name__ == "__main__":
    unittest.main()
