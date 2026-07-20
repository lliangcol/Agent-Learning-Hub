import time

from agent_learning_hub.core import AgentRunner, ProviderResponse, StopReason
from agent_learning_hub.providers import SequenceProvider, ToolResultEchoProvider
from agent_learning_hub.tools import ToolRegistry, ToolResult, ToolSpec, ToolStatus


def calculator(expression: str) -> ToolResult:
    return ToolResult(ToolStatus.OK, {"expression": expression, "value": 4})


def registry() -> ToolRegistry:
    return ToolRegistry(
        [
            ToolSpec(
                "calculator",
                "安全计算",
                {
                    "type": "object",
                    "properties": {"expression": {"type": "string"}},
                    "required": ["expression"],
                    "additionalProperties": False,
                },
                calculator,
            )
        ]
    )


def test_agent_uses_real_tool_result_then_completes() -> None:
    provider = SequenceProvider(
        [
            ProviderResponse(
                kind="tool_call", tool_name="calculator", tool_arguments={"expression": "2+2"}
            ),
            ProviderResponse(kind="text", text="工具返回 4。"),
        ]
    )
    result = AgentRunner(provider, registry()).run("2+2 等于多少？")
    assert result.stop_reason is StopReason.COMPLETED
    assert result.answer == "工具返回 4。"
    assert result.state.messages[-2].content["data"]["value"] == 4  # type: ignore[index]
    assert [step.event for step in result.trace.steps] == [
        "provider_tool_call",
        "tool_result",
        "provider_text",
    ]


def test_agent_stops_repeated_call_loop() -> None:
    repeated = ProviderResponse(
        kind="tool_call", tool_name="calculator", tool_arguments={"expression": "2+2"}
    )
    result = AgentRunner(
        SequenceProvider([repeated, repeated, repeated]), registry(), repeat_limit=2
    ).run("loop")
    assert result.stop_reason is StopReason.REPEATED_CALL
    assert result.state.tool_calls == 2


def test_agent_stops_for_tool_budget() -> None:
    responses = [
        ProviderResponse(
            kind="tool_call", tool_name="calculator", tool_arguments={"expression": str(index)}
        )
        for index in range(3)
    ]
    result = AgentRunner(SequenceProvider(responses), registry(), tool_budget=1).run("budget")
    assert result.stop_reason is StopReason.TOOL_BUDGET


def test_agent_handles_unknown_response_and_provider_error() -> None:
    unknown = AgentRunner(SequenceProvider([ProviderResponse(kind="unknown")]), registry()).run(
        "unknown"
    )
    assert unknown.stop_reason is StopReason.UNKNOWN_RESPONSE

    class FailingProvider:
        def respond(self, messages, tools, *, timeout):  # type: ignore[no-untyped-def]
            raise RuntimeError("secret internal detail")

    failed = AgentRunner(FailingProvider(), registry()).run("error")
    assert failed.stop_reason is StopReason.PROVIDER_ERROR
    assert failed.trace.steps[-1].error_code == "provider_failed"


def test_agent_stops_at_max_steps() -> None:
    responses = [
        ProviderResponse(
            kind="tool_call", tool_name="calculator", tool_arguments={"expression": str(index)}
        )
        for index in range(4)
    ]
    result = AgentRunner(SequenceProvider(responses), registry(), max_steps=2).run("steps")
    assert result.stop_reason is StopReason.MAX_STEPS


def test_mock_final_answer_is_derived_from_structured_tool_result() -> None:
    result = AgentRunner(
        ToolResultEchoProvider("calculator", {"expression": "fixture"}, result_field="value"),
        registry(),
    ).run("calculate")
    assert result.answer == "工具结果是 4。"


def test_tool_timeout_returns_without_waiting_for_the_slow_tool() -> None:
    def slow() -> ToolResult:
        time.sleep(0.2)
        return ToolResult(ToolStatus.OK)

    tool = ToolSpec("slow", "slow fixture", {"type": "object"}, slow)
    provider = SequenceProvider(
        [ProviderResponse(kind="tool_call", tool_name="slow", tool_arguments={})]
    )
    started = time.perf_counter()
    result = AgentRunner(provider, ToolRegistry([tool]), tool_timeout=0.01).run("timeout")
    assert time.perf_counter() - started < 0.1
    assert result.stop_reason is StopReason.DEADLINE
    assert result.trace.steps[-1].event == "tool_timeout"
