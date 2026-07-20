from __future__ import annotations

import json
import os
from collections.abc import Sequence
from typing import Any

from agent_learning_hub.core.models import Message, ProviderResponse
from agent_learning_hub.tools.registry import ToolSpec


class OpenAIResponsesProvider:
    """Optional live provider. The offline curriculum never requires an API key."""

    def __init__(self, *, model: str | None = None) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise RuntimeError("Install the provider extra: uv sync --extra provider") from exc
        if not os.environ.get("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is required only for the optional live lab")
        self._client: Any = OpenAI()
        self._model = model or os.environ.get("OPENAI_MODEL", "gpt-5.6-terra")

    def respond(
        self,
        messages: Sequence[Message],
        tools: Sequence[ToolSpec],
        *,
        timeout: float,
    ) -> ProviderResponse:
        input_items: list[dict[str, Any]] = []
        for message in messages:
            if isinstance(message.content, str):
                input_items.append({"role": message.role, "content": message.content})
                continue
            if message.role == "assistant" and message.content.get("type") == "tool_call":
                input_items.append(
                    {
                        "type": "function_call",
                        "call_id": message.content["call_id"],
                        "name": message.content["name"],
                        "arguments": json.dumps(
                            message.content["arguments"], ensure_ascii=False, sort_keys=True
                        ),
                    }
                )
                continue
            if message.role == "tool":
                input_items.append(
                    {
                        "type": "function_call_output",
                        "call_id": message.content["call_id"],
                        "output": json.dumps(message.content, ensure_ascii=False, sort_keys=True),
                    }
                )
                continue
            input_items.append(
                {
                    "role": message.role,
                    "content": json.dumps(message.content, ensure_ascii=False, sort_keys=True),
                }
            )
        response = self._client.responses.create(
            model=self._model,
            input=input_items,
            tools=[tool.as_openai_tool() for tool in tools],
            timeout=timeout,
        )
        for item in response.output:
            if item.type == "function_call":
                try:
                    arguments = json.loads(item.arguments)
                except json.JSONDecodeError:
                    return ProviderResponse(kind="unknown")
                if not isinstance(arguments, dict):
                    return ProviderResponse(kind="unknown")
                return ProviderResponse(
                    kind="tool_call",
                    tool_name=item.name,
                    tool_arguments=arguments,
                    call_id=item.call_id,
                )
        if response.output_text:
            return ProviderResponse(kind="text", text=response.output_text)
        return ProviderResponse(kind="unknown")
