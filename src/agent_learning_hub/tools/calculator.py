from __future__ import annotations

import ast
import math
import operator
from collections.abc import Callable
from dataclasses import dataclass

_BINARY_OPERATORS: dict[type[ast.operator], Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPERATORS: dict[type[ast.unaryop], Callable[[float], float]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


@dataclass(frozen=True, slots=True)
class CalculationResult:
    ok: bool
    value: int | float | None = None
    error_code: str | None = None
    message: str | None = None

    def as_dict(self) -> dict[str, object]:
        if self.ok:
            return {"status": "ok", "result": self.value}
        return {"status": "fatal_error", "error_code": self.error_code, "message": self.message}


class _SafeEvaluator:
    def __init__(self, *, max_nodes: int, max_abs_value: float, max_exponent: int) -> None:
        self.max_nodes = max_nodes
        self.max_abs_value = max_abs_value
        self.max_exponent = max_exponent
        self.visited = 0

    def evaluate(self, node: ast.AST) -> int | float:
        self.visited += 1
        if self.visited > self.max_nodes:
            raise ValueError("expression_too_complex")
        if isinstance(node, ast.Expression):
            return self.evaluate(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
                raise ValueError("unsupported_literal")
            return self._bounded(node.value)
        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
            return self._bounded(
                _UNARY_OPERATORS[type(node.op)](float(self.evaluate(node.operand)))
            )
        if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > self.max_exponent:
                raise ValueError("exponent_too_large")
            return self._bounded(_BINARY_OPERATORS[type(node.op)](left, right))
        raise ValueError("unsupported_syntax")

    def _bounded(self, value: int | float) -> int | float:
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError("non_finite_result")
        if abs(value) > self.max_abs_value:
            raise ValueError("result_too_large")
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return value


def safe_calculate(
    expression: str,
    *,
    max_length: int = 200,
    max_nodes: int = 64,
    max_abs_value: float = 1e100,
    max_exponent: int = 10,
) -> CalculationResult:
    if not isinstance(expression, str) or not expression.strip():
        return CalculationResult(False, error_code="empty_expression", message="请输入算术表达式。")
    if len(expression) > max_length:
        return CalculationResult(
            False, error_code="expression_too_long", message="表达式超过长度限制。"
        )
    try:
        tree = ast.parse(expression, mode="eval")
        value = _SafeEvaluator(
            max_nodes=max_nodes,
            max_abs_value=max_abs_value,
            max_exponent=max_exponent,
        ).evaluate(tree)
    except SyntaxError:
        return CalculationResult(False, error_code="invalid_syntax", message="表达式语法无效。")
    except ZeroDivisionError:
        return CalculationResult(False, error_code="division_by_zero", message="除数不能为零。")
    except (ArithmeticError, ValueError) as exc:
        code = str(exc) if str(exc) else "calculation_failed"
        return CalculationResult(False, error_code=code, message="表达式不在允许的安全范围内。")
    return CalculationResult(True, value=value)
