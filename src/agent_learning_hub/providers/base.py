from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from agent_learning_hub.core.models import Message, ProviderResponse
from agent_learning_hub.tools.registry import ToolSpec


class LLMClient(Protocol):
    def respond(
        self,
        messages: Sequence[Message],
        tools: Sequence[ToolSpec],
        *,
        timeout: float,
    ) -> ProviderResponse: ...
