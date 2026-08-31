"""Export active repository skills as plain text for other AI agents."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / ".github" / "skills"
CATALOG = ROOT / "docs" / "SKILLS_CATALOG.md"


def active_names() -> set[str]:
    names: set[str] = set()
    for line in CATALOG.read_text(encoding="utf-8").splitlines():
        match = re.match(r"\| `([^`]+)` \| active \|", line)
        if match:
            names.add(match.group(1))
    return names


def main() -> int:
    for name in sorted(active_names()):
        path = SKILLS_ROOT / name / "SKILL.md"
        if path.is_file():
            print(f"\n<!-- skill: {name} -->\n")
            print(path.read_text(encoding="utf-8").rstrip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
