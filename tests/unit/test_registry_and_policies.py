import pytest

from agent_learning_hub.policies import PermissionPolicy, RetryPolicy, run_with_retry
from agent_learning_hub.tools import (
    ToolRegistry,
    ToolResult,
    ToolSpec,
    ToolStatus,
    WorkspaceFiles,
)


def test_registry_denies_side_effect_without_approval() -> None:
    tool = ToolSpec(
        "write_file",
        "write",
        {"type": "object"},
        lambda path: ToolResult(ToolStatus.OK, {"path": path}),
        read_only=False,
    )
    registry = ToolRegistry([tool])
    assert registry.run("write_file", {"path": "x"}).status is ToolStatus.DENIED
    assert registry.run("write_file", {"path": "x"}, allow_side_effects=True).error_code == (
        "idempotency_key_required"
    )
    assert (
        registry.run(
            "write_file", {"path": "x"}, allow_side_effects=True, idempotency_key="write-x"
        ).status
        is ToolStatus.OK
    )


def test_registry_validates_tool_and_arguments_and_redacts_exceptions() -> None:
    def boom(value: str) -> ToolResult:
        raise RuntimeError(f"secret={value}")

    registry = ToolRegistry([ToolSpec("boom", "boom", {"type": "object"}, boom)])
    assert registry.run("missing", {}).error_code == "unknown_tool"
    assert registry.run("boom", {}).error_code == "invalid_arguments"
    failed = registry.run("boom", {"value": "token"})
    assert failed.error_code == "tool_failed"
    assert "token" not in (failed.message or "")


def test_permission_policy_is_deny_by_default() -> None:
    policy = PermissionPolicy(allowed_read_tools={"search"})
    assert policy.allows("search", read_only=True)
    assert not policy.allows("read_file", read_only=True)
    assert not policy.allows("publish", read_only=False)
    assert not policy.allows("publish", read_only=False, idempotency_key="unknown")
    policy.approve_once("publish-123")
    assert policy.allows("publish", read_only=False, idempotency_key="publish-123")
    with pytest.raises(ValueError, match="must not be empty"):
        policy.approve_once("  ")


def test_retry_only_retries_retryable_errors() -> None:
    results = iter(
        [
            ToolResult(ToolStatus.RETRYABLE_ERROR, error_code="temporary"),
            ToolResult(ToolStatus.OK, {"value": 1}),
        ]
    )
    delays: list[float] = []
    result = run_with_retry(
        lambda: next(results),
        RetryPolicy(max_attempts=3, base_delay=1, jitter=0),
        sleep=delays.append,
    )
    assert result.status is ToolStatus.OK
    assert delays == [1]


def test_registry_caches_reads_and_deduplicates_side_effects() -> None:
    calls = {"read": 0, "write": 0}

    def read(value: str) -> ToolResult:
        calls["read"] += 1
        return ToolResult(ToolStatus.OK, {"value": value})

    def write(value: str) -> ToolResult:
        calls["write"] += 1
        return ToolResult(ToolStatus.OK, {"value": value})

    registry = ToolRegistry(
        [
            ToolSpec("read", "read", {"type": "object"}, read, cacheable=True),
            ToolSpec("write", "write", {"type": "object"}, write, read_only=False),
        ]
    )
    assert registry.run("read", {"value": "a"}) == registry.run("read", {"value": "a"})
    assert calls["read"] == 1
    first = registry.run(
        "write", {"value": "a"}, allow_side_effects=True, idempotency_key="operation-1"
    )
    repeated = registry.run(
        "write", {"value": "a"}, allow_side_effects=True, idempotency_key="operation-1"
    )
    assert repeated == first
    assert calls["write"] == 1
    conflict = registry.run(
        "write", {"value": "b"}, allow_side_effects=True, idempotency_key="operation-1"
    )
    assert conflict.error_code == "idempotency_conflict"


def test_workspace_file_tools_block_traversal_and_require_overwrite_policy(tmp_path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    files = WorkspaceFiles(workspace)
    assert files.write_text("notes/a.md", "one").status is ToolStatus.OK
    assert files.read_text("notes/a.md").data["content"] == "one"
    assert files.write_text("notes/a.md", "two").error_code == "overwrite_denied"
    assert files.write_text("notes/a.md", "two", overwrite=True).status is ToolStatus.OK
    assert files.read_text("../outside.txt").error_code == "invalid_path_or_encoding"
    assert files.write_text("../outside.txt", "x").error_code == "invalid_path_or_encoding"
    assert files.read_text("missing.txt").error_code == "file_not_found"
    read_spec, write_spec = files.specs()
    assert read_spec.read_only and not write_spec.read_only
