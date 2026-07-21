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


def test_tool_timeout_returns_only_after_the_slow_thread_has_stopped() -> None:
    finished = False

    def slow() -> ToolResult:
        nonlocal finished
        time.sleep(0.05)
        finished = True
        return ToolResult(ToolStatus.OK)

    tool = ToolSpec("slow", "slow fixture", {"type": "object"}, slow)
    provider = SequenceProvider(
        [ProviderResponse(kind="tool_call", tool_name="slow", tool_arguments={})]
    )
    started = time.perf_counter()
    result = AgentRunner(provider, ToolRegistry([tool]), tool_timeout=0.01).run("timeout")
    assert time.perf_counter() - started >= 0.05
    assert finished
    assert result.stop_reason is StopReason.DEADLINE
    assert result.trace.steps[-1].event == "tool_timeout"


def test_agent_rejects_provider_result_that_arrives_after_total_deadline() -> None:
    observed_timeout = 0.0

    class SlowProvider:
        def respond(self, messages, tools, *, timeout):  # type: ignore[no-untyped-def]
            nonlocal observed_timeout
            del messages, tools
            observed_timeout = timeout
            time.sleep(0.03)
            return ProviderResponse(kind="text", text="too late")

    result = AgentRunner(
        SlowProvider(),
        registry(),
        total_deadline=0.005,
        provider_timeout=1,
    ).run("deadline")
    assert observed_timeout <= 0.005
    assert result.stop_reason is StopReason.DEADLINE
    assert result.answer is None
    assert result.trace.steps[-1].event == "provider_deadline"


def test_agent_classifies_late_provider_exception_as_deadline() -> None:
    class SlowFailingProvider:
        def respond(self, messages, tools, *, timeout):  # type: ignore[no-untyped-def]
            del messages, tools, timeout
            time.sleep(0.02)
            raise RuntimeError("late synthetic failure")

    result = AgentRunner(
        SlowFailingProvider(),
        registry(),
        total_deadline=0.005,
        provider_timeout=1,
    ).run("deadline")
    assert result.stop_reason is StopReason.DEADLINE
    assert result.trace.steps[-1].event == "provider_deadline"
    assert result.trace.steps[-1].error_code == "timeout"
