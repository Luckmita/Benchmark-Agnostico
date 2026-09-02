"""Fail-closed checks for active gate and capacity documentation."""

from __future__ import annotations

import json
from pathlib import Path
import sys


EXPECTED = {
    "C1": ("learning", "C1_LEARNING_PREREGISTRATION.md"),
    "C2": ("sample_efficiency", "C2_SAMPLE_EFFICIENCY_PREREGISTRATION.md"),
    "C3": ("generalization", "C3_GENERALIZATION_PREREGISTRATION.md"),
    "C4": ("adaptation", "C4_ADAPTATION_PREREGISTRATION.md"),
    "C5": ("temporal_dependency", "C5_TEMPORAL_DEPENDENCY_PREREGISTRATION.md"),
    "C6": ("planning", "C6_PLANNING_PREREGISTRATION.md"),
    "C7": ("continual_learning", "C7_CONTINUAL_LEARNING_PREREGISTRATION.md"),
    "C8": ("robustness", "C8_ROBUSTNESS_PREREGISTRATION.md"),
    "C9": ("multidomain_transfer", "C9_MULTIDOMAIN_TRANSFER_PREREGISTRATION.md"),
    "C10": ("uncertainty", "C10_UNCERTAINTY_PREREGISTRATION.md"),
    "C11": ("computational_efficiency", "C11_COMPUTATIONAL_EFFICIENCY_PREREGISTRATION.md"),
}

HISTORICAL = (
    "C3_ROBUSTNESS_PREREGISTRATION.md",
    "C4_GENERALIZATION_PREREGISTRATION.md",
    "C5_DYNAMIC_STABILITY_PREREGISTRATION.md",
    "C6_ADVERSARIAL_RESILIENCE_PREREGISTRATION.md",
    "C7_INTERPRETABILITY_PREREGISTRATION.md",
    "C8_COMPOSITIONALITY_PREREGISTRATION.md",
    "C9_MULTIAGENT_COORDINATION_PREREGISTRATION.md",
    "C10_COMPUTATIONAL_EFFICIENCY_PREREGISTRATION.md",
    "C11_AUDIT_TRANSPARENCY_PREREGISTRATION.md",
)


def check(root: Path) -> list[str]:
    errors: list[str] = []
    protocol_root = root / "docs" / "protocols"
    taxonomy = json.loads((root / "configs" / "public" / "capacity_taxonomy.json").read_text(encoding="utf-8"))
    configured = {item["id"]: item["name"] for item in taxonomy["capacities"]}
    expected_names = {capacity_id: values[0] for capacity_id, values in EXPECTED.items()}
    if configured != expected_names:
        errors.append("public capacity taxonomy differs from the normative mapping")
    for capacity_id, (_name, filename) in EXPECTED.items():
        path = protocol_root / filename
        if not path.is_file():
            errors.append(f"missing canonical protocol for {capacity_id}: {filename}")
    for filename in HISTORICAL:
        first_line = (protocol_root / filename).read_text(encoding="utf-8").splitlines()[0]
        if not first_line.startswith("# HISTORICO SUPERADO"):
            errors.append(f"historical protocol is not marked as superseded: {filename}")
    status = (root / "docs" / "STATUS.md").read_text(encoding="utf-8")
    if "Gate atual: `B4 - IN REVIEW`" not in status:
        errors.append("active status must identify B4 as the gate under review")
    if "Ultimo gate vigente aprovado: `B3`" not in status:
        errors.append("active status must record B3 as the latest approved gate")
    if "submissao somente em B16" not in status:
        errors.append("active status must reserve submissions for B16")
    if not (root / "docs" / "reviews" / "B1_CORRECTIVE_APPROVAL_2026-09-02.md").is_file():
        errors.append("missing corrective B1 approval record")
    if not (root / "docs" / "reviews" / "B2_GATE_REVIEW_2026-09-02.md").is_file():
        errors.append("missing B2 gate review")
    if not (root / "docs" / "reviews" / "B3_GATE_REVIEW_2026-09-02.md").is_file():
        errors.append("missing B3 gate review")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = check(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("governance checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
