"""Deterministic local CLI baseline for the research-assistant direction."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from checklist import run_research_case, validate_manifest


def run_cases(cases: list[dict[str, Any]]) -> dict[str, Any]:
    outcomes = []
    for case in cases:
        observed = run_research_case(case)
        expected = case.get("expected")
        passed = isinstance(expected, dict) and all(
            observed.get(key) == value for key, value in expected.items()
        )
        if observed["status"] == "cited_answer" and not observed["citations"]:
            passed = False
        outcomes.append({"id": case.get("id", "missing-id"), **observed, "passed": passed})
    return {
        "total": len(outcomes),
        "passed": sum(bool(outcome["passed"]) for outcome in outcomes),
        "outcomes": outcomes,
        "external_side_effects": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(__file__).parents[1] / "fixtures" / "manifest.json",
    )
    args = parser.parse_args()
    manifest_path = args.manifest.resolve()
    root = manifest_path.parent.parent
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    issues = validate_manifest(manifest, root)
    if issues:
        raise SystemExit("invalid manifest: " + ", ".join(issues))
    dataset = (root / manifest["eval_dataset"]).resolve()
    cases = json.loads(dataset.read_text(encoding="utf-8"))
    print(json.dumps(run_cases(cases), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
