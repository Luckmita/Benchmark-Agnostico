"""Validate repository skills without third-party dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / ".github" / "skills"
REQUIRED_SECTIONS = (
    "When to use",
    "Inputs",
    "Procedure",
    "Output",
    "Validation",
    "Limits",
)
FORBIDDEN_PATTERNS = (
    re.compile(r"(?:seed|senha|token|api[_ -]?key)\s*[:=]\s*[^<\[\]`\s]+", re.IGNORECASE),
    re.compile(r"(?:ground[_ -]?truth|hidden[_ -]?task|sealed[_ -]?task)\s*[:=]\s*[^<\[\]`\s]+", re.IGNORECASE),
)


def parse_frontmatter(path: Path, text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return {}, [f"{path}: frontmatter must start with ---"]

    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, [f"{path}: frontmatter closing --- is missing"]

    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line or line.startswith((" ", "\t")):
            errors.append(f"{path}: invalid frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        value = value.strip().strip('"').strip("'")
        metadata[key.strip()] = value
    return metadata, errors


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    metadata, errors = parse_frontmatter(path, text)
    expected_name = path.parent.name
    if metadata.get("name") != expected_name:
        errors.append(f"{path}: name must be {expected_name!r}")
    if not metadata.get("description"):
        errors.append(f"{path}: description is required")
    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^##\s+{re.escape(section)}\s*$", text, re.MULTILINE):
            errors.append(f"{path}: missing section {section!r}")
    for pattern in FORBIDDEN_PATTERNS:
        if pattern.search(text):
            errors.append(f"{path}: contains restricted phrase matching {pattern.pattern!r}")
    for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
        if not re.match(r"^(?:https?://|#)", target):
            target_path = (path.parent / target).resolve()
            if not target_path.exists():
                errors.append(f"{path}: broken local link {target!r}")
    return errors


def main() -> int:
    if not SKILLS_ROOT.exists():
        print(f"skills directory not found: {SKILLS_ROOT}", file=sys.stderr)
        return 1
    paths = sorted(
        path
        for path in SKILLS_ROOT.glob("*/SKILL.md")
        if path.parent.name != "_template"
    )
    if not paths:
        print("no skills found", file=sys.stderr)
        return 1

    errors: list[str] = []
    names: set[str] = set()
    for path in paths:
        if path.parent.name in names:
            errors.append(f"duplicate skill name: {path.parent.name}")
        names.add(path.parent.name)
        errors.extend(validate_skill(path))

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"validated {len(paths)} skill(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
