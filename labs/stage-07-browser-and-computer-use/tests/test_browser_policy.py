import importlib.util
import sys
from pathlib import Path

PATH = Path(__file__).parents[1] / "solution" / "browser_policy.py"
SPEC = importlib.util.spec_from_file_location("lab_s07_policy", PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_browser_policy_allows_only_controlled_local_hosts() -> None:
    assert MODULE.is_allowed_url("http://localhost:8000/lab")
    assert MODULE.is_allowed_url("http://127.0.0.1:8000/lab")
    assert not MODULE.is_allowed_url("file:///etc/passwd")
    assert not MODULE.is_allowed_url("https://example.com/login")


def test_step_budget_stops() -> None:
    records = [MODULE.ActionRecord(index, "o", "a", "r") for index in range(8)]
    assert not MODULE.enforce_step_budget(records)
