from __future__ import annotations

from collections import deque
from collections.abc import Iterable, Sequence

from agent_learning_hub.core.models import Message, ProviderResponse
from agent_learning_hub.tools.registry import ToolSpec


class SequenceProvider:
    """Deterministic offline provider for labs and tests."""

    def __init__(self, responses: Iterable[ProviderResponse]) -> None:
        self._responses = deque(responses)

    def respond(
        self,
        messages: Sequence[Message],
        tools: Sequence[ToolSpec],
        *,
        timeout: float,
    ) -> ProviderResponse:
        del messages, tools, timeout
        if not self._responses:
            return ProviderResponse(kind="unknown")
        return self._responses.popleft()


class ToolResultEchoProvider:
    """Request one tool, then derive the final text from its structured result."""

    def __init__(self, tool_name: str, arguments: dict[str, object], *, result_field: str) -> None:
        self.tool_name = tool_name
        self.arguments = arguments
        self.result_field = result_field

    def respond(
        self,
        messages: Sequence[Message],
        tools: Sequence[ToolSpec],
        *,
        timeout: float,
    ) -> ProviderResponse:
        del tools, timeout
        tool_message = next(
            (message for message in reversed(messages) if message.role == "tool"), None
        )
        if tool_message is None:
            return ProviderResponse(
                kind="tool_call",
                tool_name=self.tool_name,
                tool_arguments=self.arguments,
            )
        content = tool_message.content
        if not isinstance(content, dict) or content.get("status") != "ok":
            return ProviderResponse(kind="text", text="工具未成功，停止并保留结构化错误。")
        data = content.get("data")
        value = data.get(self.result_field) if isinstance(data, dict) else None
        return ProviderResponse(kind="text", text=f"工具结果是 {value}。")
