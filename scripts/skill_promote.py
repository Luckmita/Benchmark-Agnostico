"""Promote a validated skill and update the catalog."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "docs" / "SKILLS_CATALOG.md"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python scripts/skill_promote.py <skill-name>", file=sys.stderr)
        return 2
    name = sys.argv[1]
    skill = ROOT / ".github" / "skills" / name / "SKILL.md"
    if not skill.is_file():
        print(f"skill not found: {name}", file=sys.stderr)
        return 1
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "skill_validator.py")],
        cwd=ROOT,
        check=False,
    )
    if result.returncode:
        print("promotion blocked: skill validation failed", file=sys.stderr)
        return result.returncode

    catalog = CATALOG.read_text(encoding="utf-8")
    row = re.compile(rf"^\| `{re.escape(name)}` \| [^|]+ \|", re.MULTILINE)
    if not row.search(catalog):
        print(f"promotion blocked: add {name!r} to docs/SKILLS_CATALOG.md first", file=sys.stderr)
        return 1
    updated = row.sub(f"| `{name}` | active |", catalog, count=1)
    CATALOG.write_text(updated, encoding="utf-8")
    print(f"promoted skill: {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
