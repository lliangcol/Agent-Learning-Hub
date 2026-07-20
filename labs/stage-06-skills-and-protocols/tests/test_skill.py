import importlib.util
import json
from pathlib import Path

import pytest
import yaml
from mcp.shared.memory import create_connected_server_and_client_session

ROOT = Path(__file__).parents[1]
SKILL = ROOT / "solution" / "research-brief"


def test_skill_metadata_resources_and_read_only_contract(tmp_path) -> None:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---", 2)[1])
    assert metadata["name"] == "research-brief"
    assert "Use when" in metadata["description"]
    assert (SKILL / "scripts" / "collect_notes.py").is_file()
    assert (SKILL / "assets" / "brief-template.md").is_file()
    contract = json.loads((ROOT / "solution" / "mcp-contract.json").read_text(encoding="utf-8"))
    assert contract["annotations"]["readOnlyHint"] is True

    note = tmp_path / "note.md"
    note.write_text("synthetic evidence", encoding="utf-8")
    spec = importlib.util.spec_from_file_location(
        "collect_notes", SKILL / "scripts" / "collect_notes.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.collect([note])[0]["content"] == "synthetic evidence"


def test_read_only_mcp_tool_rejects_unknown_notes() -> None:
    spec = importlib.util.spec_from_file_location(
        "lab_s06_mcp_server", ROOT / "solution" / "mcp_server.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.read_course_note("NOTE-01")["source"] == "synthetic-fixture"
    with pytest.raises(ValueError, match="unknown synthetic"):
        module.read_course_note("../../secret")


@pytest.mark.anyio
async def test_mcp_client_lists_and_calls_the_tool() -> None:
    spec = importlib.util.spec_from_file_location(
        "lab_s06_mcp_protocol", ROOT / "solution" / "mcp_server.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    async with create_connected_server_and_client_session(
        module.mcp, raise_exceptions=True
    ) as session:
        listed = await session.list_tools()
        tool = next(item for item in listed.tools if item.name == "read_course_note")
        assert tool.annotations is not None
        assert tool.annotations.readOnlyHint is True
        result = await session.call_tool("read_course_note", {"note_id": "NOTE-02"})
        assert result.isError is False
        assert result.structuredContent == {
            "note_id": "NOTE-02",
            "content": "Tool calls should use structured inputs and outputs.",
            "source": "synthetic-fixture",
        }
