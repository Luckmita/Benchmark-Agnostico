---
name: gate-review
description: "Use when closing a benchmark gate, reviewing gate evidence, extracting reusable agent skills, or preparing a handoff."
---

# Gate review

## When to use

Use at the end of every gate and before a large release milestone. This workflow reviews the gate without inspecting candidate architectures before B14/B15.

## Inputs

- `docs/STATUS.md`
- `docs/EXECUTION_PLAN.md`
- `docs/DECISIONS.md`
- The gate's tests, reports, raw evidence, and change records
- `AGENTS.md` and the applicable technical contract

## Procedure

1. Identify the current gate and copy its exit criteria into the review notes.
2. Check each criterion against a reproducible artifact, command, or review record.
3. Record failures as blockers; do not reinterpret a failed benchmark as an agent failure.
4. Review the completed work for a repeatable workflow that another agent would benefit from.
5. Propose a skill only if the workflow has a clear trigger, inputs, procedure, output, validation, and limits.
6. Run `python scripts/skill_validator.py` before promoting any skill.
7. Promote only validated skills with evidence and a catalog entry. Scientific changes still require a `CHANGE-ID` and the relevant gate approval.
8. Update `docs/STATUS.md` with result, evidence, risks, and the next executable step.

## Output

- Gate result: `PASS`, `BLOCKED`, or `TEST_INVALID`
- Evidence paths and validation commands
- Open decisions and risks
- Skill proposal or promotion record, when justified
- A resumable next step in `docs/STATUS.md`

## Validation

- The gate exit criteria are all mapped to evidence.
- No candidate data, sealed seed, hidden task, or private hint was exposed.
- `python scripts/skill_validator.py` exits successfully.
- Any scientific change has a `CHANGE-ID`.

## Limits

This skill does not approve scientific changes, release a sealed set, inspect candidate internals, or replace human governance. It extracts process knowledge; it cannot change benchmark validity by itself.
