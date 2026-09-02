"""Development-only local resource accounting for normative C11."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter, process_time
import tracemalloc
from typing import Any, Callable


@dataclass(frozen=True)
class ResourceMeasurement:
    wall_seconds: float
    cpu_seconds: float
    python_peak_bytes: int
    result: Any
    scope: str = "current-process-python-allocations"


def measure_callable(function: Callable[..., Any], *args: Any, **kwargs: Any) -> ResourceMeasurement:
    """Measure one callable without claiming GPU, child-process or energy coverage."""

    tracemalloc.start()
    wall_start = perf_counter()
    cpu_start = process_time()
    try:
        result = function(*args, **kwargs)
        cpu_seconds = process_time() - cpu_start
        wall_seconds = perf_counter() - wall_start
        _current, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return ResourceMeasurement(wall_seconds, cpu_seconds, peak, result)
