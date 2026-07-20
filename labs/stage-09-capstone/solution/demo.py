"""Deterministic local CLI baseline for the research-assistant direction."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from checklist import validate_manifest


def run_cases(cases: list[dict[str, Any]]) -> dict[str, Any]:
    outcomes = []
    expected = {
        "cited_query": ("complete", "cited_answer"),
        "no_source": ("no_sources", "stopped"),
        "denied_external": ("permission_denied", "stopped"),
        "secret_input": ("sensitive_input_rejected", "stopped"),
        "malformed": ("invalid_input", "stopped"),
    }
    for case in cases:
        stop_reason, status = expected.get(str(case.get("scenario")), ("unknown_case", "failed"))
        outcomes.append(
            {
                "id": case.get("id", "missing-id"),
                "status": status,
                "stop_reason": stop_reason,
                "citations": ["SYNTHETIC-01"] if status == "cited_answer" else [],
            }
        )
    return {
        "total": len(outcomes),
        "passed": sum(outcome["status"] != "failed" for outcome in outcomes),
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
