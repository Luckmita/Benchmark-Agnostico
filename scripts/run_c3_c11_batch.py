"""Historical batch disabled by CHG-2026-09-01-GATE-REALIGNMENT."""

from __future__ import annotations

import sys


def main() -> int:
    print(
        "disabled: the historical batch used non-normative C3-C11 IDs and treated "
        "absence of exceptions as scientific PASS; use focused public prototype tests instead",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
