"""Compatibility wrapper for the installed benchmark CLI."""

from benchmark_core.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
