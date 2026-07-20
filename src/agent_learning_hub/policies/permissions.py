from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PermissionPolicy:
    """Deny by default; read-only tools can be explicitly allowed."""

    allowed_read_tools: set[str] = field(default_factory=set)
    approved_idempotency_keys: set[str] = field(default_factory=set)

    def allows(
        self, tool_name: str, *, read_only: bool, idempotency_key: str | None = None
    ) -> bool:
        if read_only:
            return tool_name in self.allowed_read_tools
        return idempotency_key is not None and idempotency_key in self.approved_idempotency_keys

    def approve_once(self, idempotency_key: str) -> None:
        if not idempotency_key.strip():
            raise ValueError("idempotency key must not be empty")
        self.approved_idempotency_keys.add(idempotency_key)
