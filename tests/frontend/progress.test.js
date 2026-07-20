import { beforeAll, beforeEach, describe, expect, test, vi } from "vitest";

beforeAll(async () => {
  await import("../../site/src/progress.js");
});

beforeEach(() => localStorage.clear());

const mapping = {
  task_mappings: [
    { old_id: "V1-S0-T01", new_id: "S00-T01" },
    { old_id: "V1-S2-T01", new_id: "S03-T01" },
  ],
  project_mappings: [{ old_id: "V1-P01", new_id: "P01" }],
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
