"""Dependency-free descriptive metrics for benchmark reports."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
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
