import { beforeEach, describe, expect, test } from "vitest";

beforeEach(() => {
  document.body.innerHTML = '<p id="origin"></p><p id="summary"></p><button id="export"></button>';
  localStorage.clear();
});

describe("V1 migration export", () => {
  test("collects only documented legacy keys", async () => {
    localStorage.setItem("agent-learning-hub-state", '{"stage0-0":true}');
    localStorage.setItem("note-stage0", "<script>alert(1)</script>");
    localStorage.setItem("agent-learning-theme", "dark");
    localStorage.setItem("unrelated", "do-not-export");
    const { collectLegacyData } = await import("../../site/src/legacy-migration.js");
    const payload = collectLegacyData(localStorage);
    expect(payload.state).toContain("stage0-0");
    expect(payload.notes["note-stage0"]).toContain("<script>");
    expect(payload.theme).toBe("dark");
    expect(payload).not.toHaveProperty("unrelated");
  });
});
