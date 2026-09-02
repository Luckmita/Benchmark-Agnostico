"""Dependency-free descriptive metrics for benchmark reports."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from statistics import mean, median, stdev
from typing import Sequence


@dataclass(frozen=True)
class SummaryStatistics:
    count: int
    mean: float
    median: float
    std: float
    ci95_low: float
    ci95_high: float


def summarize(values: Sequence[float]) -> SummaryStatistics:
    if not values:
        raise ValueError("at least one value is required")
    numeric = [float(value) for value in values]
    average = mean(numeric)
    deviation = stdev(numeric) if len(numeric) > 1 else 0.0
    margin = 1.96 * deviation / sqrt(len(numeric))
    return SummaryStatistics(
        count=len(numeric),
        mean=average,
        median=median(numeric),
        std=deviation,
        ci95_low=average - margin,
        ci95_high=average + margin,
    )


def paired_effect_size(values_a: Sequence[float], values_b: Sequence[float]) -> float:
    """Cohen's d for paired differences, returning zero for no variation."""

    if len(values_a) != len(values_b) or not values_a:
        raise ValueError("paired samples must have equal non-zero length")
    differences = [float(a) - float(b) for a, b in zip(values_a, values_b)]
    deviation = stdev(differences) if len(differences) > 1 else 0.0
    return mean(differences) / deviation if deviation else 0.0


def win_rate(values_a: Sequence[float], values_b: Sequence[float]) -> float:
    if len(values_a) != len(values_b) or not values_a:
        raise ValueError("paired samples must have equal non-zero length")
    return sum(a > b for a, b in zip(values_a, values_b)) / len(values_a)


def trapezoidal_auc(values: Sequence[float]) -> float:
    if not values:
        raise ValueError("at least one value is required")
    return sum((left + right) / 2.0 for left, right in zip(values, values[1:]))


def steps_to_threshold(values: Sequence[float], threshold: float) -> int | None:
    for index, value in enumerate(values, start=1):
        if value >= threshold:
            return index
    return None


def brier_score(outcomes: Sequence[int], probabilities: Sequence[float]) -> float:
    """Binary Brier score for explicit probabilistic predictions."""

    _validate_probabilistic_predictions(outcomes, probabilities)
    return mean((float(probability) - outcome) ** 2 for outcome, probability in zip(outcomes, probabilities))


def expected_calibration_error(
    outcomes: Sequence[int],
    probabilities: Sequence[float],
    *,
    bins: int = 10,
) -> float:
    """Binary ECE using fixed equal-width confidence bins."""

    _validate_probabilistic_predictions(outcomes, probabilities)
    if bins <= 0:
        raise ValueError("bins must be positive")
    total = len(outcomes)
    error = 0.0
    for bin_index in range(bins):
        lower = bin_index / bins
        upper = (bin_index + 1) / bins
        members = [
            (outcome, float(probability))
            for outcome, probability in zip(outcomes, probabilities)
            if lower <= float(probability) < upper or (bin_index == bins - 1 and float(probability) == 1.0)
        ]
        if not members:
            continue
        accuracy = mean(outcome for outcome, _probability in members)
        confidence = mean(probability for _outcome, probability in members)
        error += len(members) / total * abs(accuracy - confidence)
    return error


def selective_accuracy(
    outcomes: Sequence[int],
    probabilities: Sequence[float],
    *,
    minimum_confidence: float,
) -> tuple[float | None, float]:
    """Return accuracy and coverage after abstaining below confidence."""

    _validate_probabilistic_predictions(outcomes, probabilities)
    if not 0.5 <= minimum_confidence <= 1.0:
        raise ValueError("minimum_confidence must be between 0.5 and 1")
    selected: list[bool] = []
    for outcome, probability in zip(outcomes, probabilities):
        confidence = max(float(probability), 1.0 - float(probability))
        if confidence >= minimum_confidence:
            selected.append((float(probability) >= 0.5) == bool(outcome))
    coverage = len(selected) / len(outcomes)
    return (mean(selected) if selected else None, coverage)


def evaluate_uncertainty(
    outcomes: Sequence[int],
    probabilities: Sequence[float] | None,
    *,
    bins: int = 10,
    minimum_confidence: float = 0.8,
) -> dict[str, float | str | None]:
    """Evaluate C10 or return NOT_SUPPORTED without converting it to failure."""

    if probabilities is None:
        return {"status": "NOT_SUPPORTED", "brier": None, "ece": None, "selective_accuracy": None, "coverage": None}
    accuracy, coverage = selective_accuracy(outcomes, probabilities, minimum_confidence=minimum_confidence)
    return {
        "status": "SUPPORTED",
        "brier": brier_score(outcomes, probabilities),
        "ece": expected_calibration_error(outcomes, probabilities, bins=bins),
        "selective_accuracy": accuracy,
        "coverage": coverage,
    }


def _validate_probabilistic_predictions(outcomes: Sequence[int], probabilities: Sequence[float]) -> None:
    if not outcomes or len(outcomes) != len(probabilities):
        raise ValueError("outcomes and probabilities must have equal non-zero length")
    if any(outcome not in (0, 1) or isinstance(outcome, bool) for outcome in outcomes):
        raise ValueError("outcomes must be binary integers")
    if any(not isfinite(float(probability)) or not 0.0 <= float(probability) <= 1.0 for probability in probabilities):
        raise ValueError("probabilities must be between zero and one")
