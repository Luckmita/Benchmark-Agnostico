"""Historical command disabled by CHG-2026-09-01-GATE-REALIGNMENT."""

from __future__ import annotations

import sys


def main() -> int:
    print(
        "disabled: C2 cannot reuse aggregate C1 returns as steps-to-threshold evidence; "
        "a preregistered checkpoint protocol is required",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
