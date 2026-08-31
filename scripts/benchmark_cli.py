"""Small dependency-free CLI for reproducibility utilities."""

from __future__ import annotations

import argparse
import json
import sys

from benchmark_core import hash_json


def main() -> int:
    parser = argparse.ArgumentParser(prog="benchmark-cli")
    subparsers = parser.add_subparsers(dest="command", required=True)
    hash_parser = subparsers.add_parser("hash-json", help="hash canonical JSON")
    hash_parser.add_argument("value", nargs="?", help="JSON value; defaults to stdin")
    args = parser.parse_args()

    if args.command == "hash-json":
        value_text = args.value if args.value is not None else sys.stdin.read()
        try:
            value = json.loads(value_text)
        except json.JSONDecodeError as error:
            print(f"invalid JSON: {error}", file=sys.stderr)
            return 2
        print(hash_json(value))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
