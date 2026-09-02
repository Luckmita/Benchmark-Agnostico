"""Historical command disabled by CHG-2026-09-01-GATE-REALIGNMENT."""

from __future__ import annotations

import sys


def main() -> int:
    print(
        "disabled: the 2026-09-01 C1 freeze was superseded; use "
        "'python -m benchmark_core.cli run-public-c1' for infrastructure-only development runs",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
