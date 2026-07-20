from __future__ import annotations

from agent_learning_hub.core import AgentRunner
from agent_learning_hub.providers import ToolResultEchoProvider
from agent_learning_hub.tools import ToolRegistry, ToolResult, ToolSpec, ToolStatus, safe_calculate


def calculate(expression: str) -> ToolResult:
    result = safe_calculate(expression)
    if result.ok:
        return ToolResult(ToolStatus.OK, {"value": result.value})
    return ToolResult(ToolStatus.FATAL_ERROR, error_code=result.error_code, message=result.message)


def build_runner(expression: str = "99 * 99") -> AgentRunner:
    provider = ToolResultEchoProvider(
        "calculator", {"expression": expression}, result_field="value"
    )
    tool = ToolSpec(
        "calculator",
        "只支持受限算术表达式。",
        {
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"],
            "additionalProperties": False,
        },
        calculate,
    )
    return AgentRunner(provider, ToolRegistry([tool]))


if __name__ == "__main__":
    result = build_runner().run("99 乘以 99 等于多少？")
    print(result.stop_reason.value, result.answer)
