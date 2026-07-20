from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from agent_learning_hub.core import Message
from agent_learning_hub.providers.openai_provider import OpenAIResponsesProvider


class FakeResponses:
    def __init__(self, output: list[Any], output_text: str = "") -> None:
        self.output = output
        self.output_text = output_text
        self.request: dict[str, Any] | None = None

    def create(self, **kwargs: Any) -> Any:
        self.request = kwargs
        return SimpleNamespace(output=self.output, output_text=self.output_text)


def provider_with(fake: FakeResponses) -> OpenAIResponsesProvider:
    provider = OpenAIResponsesProvider.__new__(OpenAIResponsesProvider)
    provider._client = SimpleNamespace(responses=fake)  # type: ignore[attr-defined]
    provider._model = "fixture-model"  # type: ignore[attr-defined]
    return provider


def test_responses_provider_preserves_function_call_and_output_protocol_items() -> None:
    fake = FakeResponses([], output_text="done")
    provider = provider_with(fake)
    response = provider.respond(
        [
            Message("user", "calculate"),
            Message(
                "assistant",
                {
                    "type": "tool_call",
                    "name": "calculator",
                    "arguments": {"expression": "2+2"},
                    "call_id": "call-1",
                },
            ),
            Message(
                "tool",
                {
                    "status": "ok",
                    "data": {"value": 4},
                    "error_code": None,
                    "message": None,
                    "call_id": "call-1",
                },
                name="calculator",
            ),
        ],
        [],
        timeout=3,
    )
    assert response.text == "done"
    assert fake.request is not None
    assert fake.request["input"][1] == {
        "type": "function_call",
        "call_id": "call-1",
        "name": "calculator",
        "arguments": '{"expression": "2+2"}',
    }
    assert fake.request["input"][2]["type"] == "function_call_output"
    assert fake.request["timeout"] == 3


def test_responses_provider_parses_tool_calls_and_rejects_bad_arguments() -> None:
    valid = SimpleNamespace(
        type="function_call",
        arguments='{"expression":"3+3"}',
        name="calculator",
        call_id="call-2",
    )
    response = provider_with(FakeResponses([valid])).respond([], [], timeout=1)
    assert response.tool_arguments == {"expression": "3+3"}
    assert response.call_id == "call-2"

    for arguments in ("not-json", "[]"):
        invalid = SimpleNamespace(
            type="function_call",
            arguments=arguments,
            name="calculator",
            call_id="call-bad",
        )
        assert provider_with(FakeResponses([invalid])).respond([], [], timeout=1).kind == "unknown"


def test_responses_provider_returns_unknown_without_text_or_tool_call() -> None:
    item = SimpleNamespace(type="message")
    assert provider_with(FakeResponses([item])).respond([], [], timeout=1).kind == "unknown"
