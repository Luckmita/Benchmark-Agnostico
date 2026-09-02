"""Historical generic validator disabled by the corrective gate review."""

from __future__ import annotations

import sys


def main() -> int:
    print(
        "disabled: a generic return comparison cannot validate distinct C1-C11 constructs; "
        "run the focused contract tests and an approved preregistered protocol",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
