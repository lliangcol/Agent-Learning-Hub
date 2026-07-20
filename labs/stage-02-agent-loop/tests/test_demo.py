import importlib.util
from pathlib import Path

from agent_learning_hub.core import StopReason

PATH = Path(__file__).parents[1] / "solution" / "demo.py"
SPEC = importlib.util.spec_from_file_location("lab_s02_demo", PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_agent_answer_uses_tool_result() -> None:
    result = MODULE.build_runner().run("计算")
    assert result.stop_reason is StopReason.COMPLETED
    assert "9801" in result.answer
    assert result.state.tool_calls == 1


def test_final_answer_changes_with_the_real_tool_result() -> None:
    result = MODULE.build_runner("12 * 12").run("计算")
    assert result.answer == "工具结果是 144。"
