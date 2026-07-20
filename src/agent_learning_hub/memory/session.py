from __future__ import annotations

from collections.abc import Callable

from agent_learning_hub.core.models import Message


class SessionMemory:
    def __init__(self, window_size: int = 4) -> None:
        if window_size < 1:
            raise ValueError("window_size must be positive")
        self.window_size = window_size
        self.audit_log: list[Message] = []
        self.summary = ""
        self._summarized_count = 0

    def add(self, message: Message) -> None:
        self.audit_log.append(message)

    def context(self, summarizer: Callable[[str, list[Message]], str]) -> list[Message]:
        split = max(0, len(self.audit_log) - self.window_size)
        newly_dropped = self.audit_log[self._summarized_count : split]
        if newly_dropped:
            self.summary = summarizer(self.summary, newly_dropped)
            self._summarized_count = split
        recent = self.audit_log[split:]
        if self.summary:
            return [Message("system", f"会话摘要：{self.summary}"), *recent]
        return list(recent)
