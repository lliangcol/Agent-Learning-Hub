import { beforeAll, beforeEach, describe, expect, test, vi } from "vitest";

beforeAll(async () => {
  await import("../../site/src/progress.js");
});

beforeEach(() => localStorage.clear());

const mapping = {
  task_mappings: [
    { old_id: "V1-S0-T01", new_id: "S00-T01" },
    { old_id: "V1-S2-T01", new_id: "S03-T01" },
    { old_id: "V1-S2-T02", new_id: "S04-T01" },
    { old_id: "V1-S2-T03", new_id: "S03-T02" },
    { old_id: "V1-S2-T04", new_id: "S04-T02" },
    { old_id: "V1-S2-T05", new_id: "S03-T03" },
  ],
  project_mappings: [{ old_id: "V1-P01", new_id: "P01" }],
  checked_state_by_task: {
    "S03-T01": "needs_revalidation",
    "S04-T01": "validation_failed",
    "S03-T02": "lab_verified_offline",
    "S04-T02": "learning",
    "S03-T03": "not_started",
  },
};

describe("progress schema and migration", () => {
  test("separates task and project progress and reconciles counts", () => {
    const { output, report } = ALHProgress.migrateV1(
      {
        origin: "file://",
        state: JSON.stringify({ "stage0-0": true, "stage2-0": true, "ladder-1": true }),
      },
      mapping,
    );
    expect(output.task_progress["S00-T01"].state).toBe("complete");
    expect(output.task_progress["S03-T01"].state).toBe("needs_revalidation");
    expect(output.project_progress.P01.state).toBe("needs_revalidation");
    expect(report.total).toBe(3);
  });

  test("rejects unknown IDs before replacement", () => {
    const value = ALHProgress.emptyProgress();
    value.task_progress.unknown = ALHProgress.record("learning");
    expect(() => ALHProgress.validateProgress(value, new Set(["S00-T01"]), new Set())).toThrow(
      "无效任务进度",
    );
  });

  test("rejects null imports without dereferencing untrusted input", () => {
    expect(() =>
      ALHProgress.prepareImport(null, mapping, new Set(["S00-T01"]), new Set(["P01"])),
    ).toThrow("V1 导入必须是对象");
  });

  test("never promotes unchecked V1 tasks and applies shared checked-state policy", () => {
    const rawState = {
      "stage2-0": false,
      "stage2-1": false,
      "stage2-2": false,
      "stage2-3": false,
      "stage2-4": false,
    };
    const unchecked = ALHProgress.migrateV1({ state: rawState }, mapping).output.task_progress;
    expect(Object.values(unchecked).map((item) => item.state)).toEqual([
      "not_started", "not_started", "not_started", "not_started", "not_started",
    ]);

    for (const key of Object.keys(rawState)) rawState[key] = true;
    const checked = ALHProgress.migrateV1({ state: rawState }, mapping).output.task_progress;
    expect(Object.fromEntries(Object.entries(checked).map(([id, item]) => [id, item.state]))).toEqual(
      mapping.checked_state_by_task,
    );
  });

  test("enforces the complete V2 schema including formats, item types, and extra fields", () => {
    const taskIds = new Set(["S00-T01"]);
    const invalid = ALHProgress.emptyProgress();
    invalid.extra = true;
    expect(() => ALHProgress.validateProgress(invalid, taskIds, new Set())).toThrow();

    delete invalid.extra;
    invalid.updated_at = "not-a-date";
    expect(() => ALHProgress.validateProgress(invalid, taskIds, new Set())).toThrow();

    invalid.updated_at = "2026-02-31T00:00:00Z";
    expect(() => ALHProgress.validateProgress(invalid, taskIds, new Set())).toThrow();

    invalid.updated_at = new Date().toISOString();
    invalid.task_progress["S00-T01"] = {
      ...ALHProgress.record("learning"),
      evidence_paths: [42],
    };
    expect(() => ALHProgress.validateProgress(invalid, taskIds, new Set())).toThrow(
      "无效任务进度",
    );

    invalid.task_progress["S00-T01"] = ALHProgress.record("complete");
    expect(() => ALHProgress.validateProgress(invalid, taskIds, new Set())).toThrow(
      "无效任务进度",
    );
  });

  test("imports and rolls back V1 notes and theme in the same transaction", () => {
    localStorage.setItem(ALHProgress.NOTES_KEY, "current note");
    localStorage.setItem(ALHProgress.LEGACY_THEME_KEY, "light");
    const prepared = ALHProgress.prepareImport(
      {
        schema_version: "1.0.0",
        state: { "stage0-0": true },
        notes: { "note-stage0": "legacy note" },
        theme: "dark",
      },
      mapping,
      new Set(["S00-T01", "S03-T01", "S04-T01", "S03-T02", "S04-T02", "S03-T03"]),
      new Set(["P01"]),
    );
    expect(prepared.report.conflicts).toEqual(
      expect.arrayContaining(["note:note-stage0", "theme"]),
    );
    const backupKey = ALHProgress.atomicReplace(
      prepared.output,
      localStorage,
      prepared.auxiliary,
    );
    expect(localStorage.getItem(ALHProgress.NOTES_KEY)).toContain("legacy note");
    expect(localStorage.getItem(ALHProgress.LEGACY_THEME_KEY)).toBe("dark");

    ALHProgress.restoreBackup(backupKey);
    expect(localStorage.getItem(ALHProgress.NOTES_KEY)).toBe("current note");
    expect(localStorage.getItem(ALHProgress.LEGACY_THEME_KEY)).toBe("light");
  });

  test("classifies preview conflicts and reconciles every input item", () => {
    const current = ALHProgress.emptyProgress();
    current.task_progress["S00-T01"] = ALHProgress.record("learning");
    const prepared = ALHProgress.prepareImport(
      {
        origin: "file://",
        state: JSON.stringify({ "stage0-0": true, "unknown-item": true }),
      },
      mapping,
      new Set(["S00-T01", "S03-T01"]),
      new Set(["P01"]),
      current,
    );
    expect(prepared.report.conflicts).toEqual(["stage0-0"]);
    expect(prepared.report.unmapped).toEqual(["unknown-item"]);
    expect(prepared.report.total).toBe(prepared.report.input_total);
    expect(prepared.report.reconciled).toBe(true);
  });

  test("restores previous state when atomic replacement fails", () => {
    const data = new Map([[ALHProgress.STORAGE_KEY, '{"old":true}']]);
    const storage = {
      getItem: (key) => data.get(key) ?? null,
      setItem: vi.fn((key, value) => {
        if (key === ALHProgress.STORAGE_KEY && value.includes('"schema_version"')) {
          throw new Error("quota");
        }
        data.set(key, value);
      }),
      removeItem: (key) => data.delete(key),
    };
    expect(() => ALHProgress.atomicReplace(ALHProgress.emptyProgress(), storage)).toThrow("quota");
    expect(data.get(ALHProgress.STORAGE_KEY)).toBe('{"old":true}');
  });

  test("backup records metadata and can atomically restore previous state", () => {
    const previous = ALHProgress.emptyProgress("2026-07-20T00:00:00.000Z");
    previous.task_progress["S00-T01"] = ALHProgress.record("learning");
    localStorage.setItem(ALHProgress.STORAGE_KEY, JSON.stringify(previous));
    const key = ALHProgress.atomicReplace(ALHProgress.emptyProgress());
    const backup = JSON.parse(localStorage.getItem(key));
    expect(backup.backup_schema_version).toBe("1.0.0");
    expect(backup.origin).toBe(window.location.origin);
    expect(backup.progress_schema_version).toBe("2.0.0");
    expect(backup.content_summary.task_records).toBe(1);
    expect(backup.content_summary.utf8_bytes).toBeGreaterThan(0);
    expect(ALHProgress.latestBackupKey()).toBe(key);
    ALHProgress.restoreBackup(key);
    expect(JSON.parse(localStorage.getItem(ALHProgress.STORAGE_KEY))).toEqual(previous);
  });
});
