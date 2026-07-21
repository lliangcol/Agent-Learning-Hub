import json

import pytest

from agent_learning_hub.tools import calculator
from agent_learning_hub.tools.calculator import safe_calculate


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("2 + 3 * 4", 14),
        ("(2 + 3) * 4", 20),
        ("-5 + +2", -3),
        ("7 // 2", 3),
        ("7 % 4", 3),
        ("2 ** 10", 1024),
    ],
)
def test_safe_calculate_accepts_explicit_arithmetic(expression: str, expected: int) -> None:
    result = safe_calculate(expression)
    assert result.ok
    assert result.value == expected
    assert result.as_dict() == {"status": "ok", "result": expected}


@pytest.mark.parametrize(
    ("expression", "code"),
    [
        ("", "empty_expression"),
        ("1 / 0", "division_by_zero"),
        ("x + 1", "unsupported_syntax"),
        ("__import__('os')", "unsupported_syntax"),
        ("(1).__class__", "unsupported_syntax"),
        ("sum([1, 2])", "unsupported_syntax"),
        ("2 ** 1000000", "exponent_too_large"),
        ("[1, 2]", "unsupported_syntax"),
        ("True + 1", "unsupported_literal"),
        ("1e101", "result_too_large"),
        ("1 +", "invalid_syntax"),
    ],
)
def test_safe_calculate_rejects_unsafe_or_invalid_input(expression: str, code: str) -> None:
    result = safe_calculate(expression)
    assert not result.ok
    assert result.error_code == code
    assert result.as_dict()["status"] == "fatal_error"


def test_safe_calculate_enforces_length_and_ast_limits() -> None:
    assert safe_calculate(None).error_code == "empty_expression"  # type: ignore[arg-type]
    assert safe_calculate("1" * 201).error_code == "expression_too_long"
    assert safe_calculate("+".join(["1"] * 40), max_nodes=10).error_code == "expression_too_complex"


def test_safe_calculate_rejects_overflowing_intermediate_result() -> None:
    result = safe_calculate("1e100 * 10")
    assert not result.ok
    assert result.error_code in {"result_too_large", "non_finite_result"}


def test_safe_calculate_rejects_complex_results_and_remains_json_serializable() -> None:
    result = safe_calculate("(-1) ** 0.5")
    assert not result.ok
    assert result.error_code == "non_real_result"
    assert json.loads(json.dumps(result.as_dict()))["status"] == "fatal_error"


def test_safe_calculate_rejects_non_finite_literal_and_unsupported_operators() -> None:
    assert safe_calculate("1e309").error_code == "non_finite_result"
    assert safe_calculate("~1").error_code == "unsupported_syntax"
    assert safe_calculate("1 & 2").error_code == "unsupported_syntax"


def test_safe_calculate_uses_generic_code_for_empty_arithmetic_error(monkeypatch) -> None:
    def fail_without_message(self, node):  # type: ignore[no-untyped-def]
        raise ValueError

    monkeypatch.setattr(calculator._SafeEvaluator, "evaluate", fail_without_message)
    assert safe_calculate("1").error_code == "calculation_failed"
