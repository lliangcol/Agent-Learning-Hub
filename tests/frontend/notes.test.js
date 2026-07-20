import createDOMPurify from "dompurify";
import { marked } from "marked";
import { beforeAll, describe, expect, test } from "vitest";

beforeAll(async () => {
  await import("../../site/src/notes.js");
});

describe("Markdown note sanitization", () => {
  test.each([
    "<script>globalThis.pwned=true</script>",
    '<img src=x onerror="globalThis.pwned=true">',
    "[click](javascript:alert(1))",
    '<svg onload="alert(1)"><circle /></svg>',
    '<a href="javascript:alert(1)">bad</a>',
  ])("removes executable payload: %s", (payload) => {
    const purifier = createDOMPurify(window);
    const rendered = ALHNotes.renderMarkdown(payload, marked, purifier);
    const container = document.createElement("div");
    container.innerHTML = rendered.html;
    expect(container.querySelector("script,svg,[onerror],[onload]")).toBeNull();
    expect(container.innerHTML.toLowerCase()).not.toContain("javascript:");
  });

  test("uses text fallback when parser is unavailable", () => {
    const container = document.createElement("div");
    ALHNotes.displayPreview(container, "<b>raw</b>", null, null);
    expect(container.innerHTML).toBe("&lt;b&gt;raw&lt;/b&gt;");
  });
});
