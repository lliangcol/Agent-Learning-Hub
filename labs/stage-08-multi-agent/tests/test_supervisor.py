import importlib.util
import sys
from pathlib import Path

PATH = Path(__file__).parents[1] / "solution" / "supervisor.py"
SPEC = importlib.util.spec_from_file_location("lab_s08_supervisor", PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_baseline_and_supervised_stop_conditions() -> None:
    item = MODULE.WorkItem("M01", "summarize synthetic note")
    assert MODULE.single_agent_baseline(item).approved
    assert MODULE.supervised_flow(item).approved
    assert not MODULE.supervised_flow(item, total_budget=1).approved
    assert MODULE.supervised_flow(MODULE.WorkItem("M02", "")).stop_reason == "no_progress"


def test_multi_agent_comparison_reports_cost_latency_and_error_amplification() -> None:
    items = [
        MODULE.WorkItem("M01", "summarize synthetic note"),
        MODULE.WorkItem("M02", ""),
    ]
    report = MODULE.compare(items)
    assert report["baseline"]["success_rate"] == report["supervised"]["success_rate"]
    assert report["supervised"]["cost_units"] > report["baseline"]["cost_units"]
    assert report["baseline"]["latency_ms"] >= 0
    assert isinstance(report["error_amplification"], int)
    assert report["recommendation"] == "single_agent"


def test_reviewer_and_round_budget_stop_explicitly() -> None:
    long_item = MODULE.WorkItem("M03", "x" * 201)
    assert MODULE.supervised_flow(long_item).stop_reason == "review_rejected"
    assert MODULE.supervised_flow(long_item, max_rounds=1).stop_reason == "budget_denied"
