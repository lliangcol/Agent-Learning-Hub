import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("lab_s05_compare", ROOT / "solution" / "compare.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_fixed_dataset_has_twenty_cases_and_failure_categories() -> None:
    cases = MODULE.load_cases(ROOT / "fixtures" / "eval-cases.json")
    assert len(cases) == 20
    assert {case["scenario"] for case in cases} >= {
        "success",
        "empty_result",
        "tool_error",
        "repeated_call",
        "denied",
    }
    bare = MODULE.evaluate(cases, harness=False)
    harness = MODULE.evaluate(cases, harness=True)
    assert harness["success_rate"] > bare["success_rate"]
    assert harness["passed"] == 20
    assert harness["runner"] == "typed-agent-runner"
    assert harness["total_steps"] > 0
    assert harness["total_tool_calls"] > 0
    assert harness["latency_ms"] >= 0
    assert {
        "completed",
        "repeated_call",
        "provider_error",
        "deadline",
        "tool_budget",
    } <= set(harness["stop_reasons"])
    assert all(outcome["cost"] is None for outcome in harness["outcomes"])
    assert harness["cost"] is None


def test_unknown_dataset_shape_and_scenario_are_rejected(tmp_path) -> None:
    invalid = tmp_path / "invalid.json"
    invalid.write_text('{"not":"a list"}', encoding="utf-8")
    with pytest.raises(ValueError, match="must be a list"):
        MODULE.load_cases(invalid)
    with pytest.raises(ValueError, match="unsupported scenario"):
        MODULE.evaluate([{"id": "bad", "scenario": "surprise"}], harness=True)
