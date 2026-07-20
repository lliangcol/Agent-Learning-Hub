import importlib.util
from pathlib import Path
from types import ModuleType

import pytest


def load_legacy_module() -> ModuleType:
    path = Path(__file__).parents[2] / "stage-2" / "tools_safety.py"
    spec = importlib.util.spec_from_file_location("legacy_tools_safety", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_tools_safety_imports_on_current_platform_and_times_out() -> None:
    module = load_legacy_module()
    result = module.run_code_with_timeout_demo("while True: pass", timeout=0.1)
    assert result["error_code"] == "timeout"


def test_file_tool_blocks_path_traversal(tmp_path) -> None:
    module = load_legacy_module()
    with pytest.raises(ValueError, match="允许目录之外"):
        module.resolve_safe_path(tmp_path, "../../outside.txt")


def test_database_tool_uses_bound_parameters() -> None:
    module = load_legacy_module()
    connection = module.build_demo_db()
    assert module.safe_db_query(connection, "1; DROP TABLE users; --") == []
    assert module.safe_db_query(connection, "1") == [(1, "alice")]
