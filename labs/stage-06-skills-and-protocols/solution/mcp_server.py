"""Minimal read-only MCP server backed only by synthetic in-memory fixtures."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

NOTES = {
    "NOTE-01": "Agent loops need explicit stop conditions.",
    "NOTE-02": "Tool calls should use structured inputs and outputs.",
}

mcp = FastMCP("agent-learning-hub-read-only")


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    )
)
def read_course_note(note_id: str) -> dict[str, str]:
    """Read one allow-listed synthetic course note by ID."""
    try:
        content = NOTES[note_id]
    except KeyError as exc:
        raise ValueError("unknown synthetic note ID") from exc
    return {"note_id": note_id, "content": content, "source": "synthetic-fixture"}


if __name__ == "__main__":
    mcp.run()
