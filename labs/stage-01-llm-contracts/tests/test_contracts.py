import importlib.util
import sys
from pathlib import Path

import pytest

PATH = Path(__file__).parents[1] / "solution" / "contracts.py"
SPEC = importlib.util.spec_from_file_location("lab_s01_contracts", PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_parses_one_strict_object() -> None:
    answer = MODULE.parse_structured_answer('{"answer":"离线回答","confidence":0.8}')
    assert answer.answer == "离线回答"


@pytest.mark.parametrize(
    "value",
    [
        "not json",
        '{"answer":"a","confidence":0.5} {"answer":"b","confidence":0.6}',
        '{"answer":"a"}',
        '{"answer":1,"confidence":0.5}',
        '{"answer":"a","confidence":true}',
        '{"answer":"a","confidence":2}',
        "x" * 2001,
    ],
)
def test_rejects_contract_failures(value: str) -> None:
    with pytest.raises(ValueError):
        MODULE.parse_structured_answer(value)
