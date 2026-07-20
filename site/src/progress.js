(() => {
  const STORAGE_KEY = "agent-learning-hub-progress-v2";
  const BACKUP_PREFIX = "agent-learning-hub-progress-backup-";
  const STATES = new Set([
    "not_started", "learning", "concept_verified", "lab_verified_offline",
    "lab_verified_live", "complete", "blocked", "needs_revalidation", "validation_failed",
  ]);
  function emptyProgress(now = new Date().toISOString()) {
    return {
      schema_version: "2.0.0",
      roadmap_version: "2.0.0",
      updated_at: now,
      origin: window.location.origin === "null" ? "file://" : window.location.origin,
      task_progress: {},
      project_progress: {},
    };
  }

  function validateRecord(record) {
    return (
      record &&
      STATES.has(record.state) &&
      typeof record.updated_at === "string" &&
      Array.isArray(record.evidence_paths) &&
      typeof record.review === "string" &&
      typeof record.environment === "string" &&
      typeof record.next_anchor === "string"
    );
  }

  function validateProgress(value, taskIds, projectIds) {
    if (!value || value.schema_version !== "2.0.0" || value.roadmap_version !== "2.0.0") {
      throw new Error("进度版本不支持。");
    }
    for (const [id, record] of Object.entries(value.task_progress ?? {})) {
      if (!taskIds.has(id) || !validateRecord(record)) throw new Error(`无效任务进度：${id}`);
    }
    for (const [id, record] of Object.entries(value.project_progress ?? {})) {
      if (!projectIds.has(id) || !validateRecord(record)) throw new Error(`无效项目进度：${id}`);
    }
    return value;
  }

  function record(state) {
    return {
      state,
      updated_at: new Date().toISOString(),
      evidence_paths: [],
      review: "浏览器记录，需补证据",
      environment: navigator.userAgent,
      next_anchor: "补充 Lab 证据",
    };
  }

  function loadProgress(storage = localStorage) {
    const raw = storage.getItem(STORAGE_KEY);
    if (!raw) return emptyProgress();
    try {
      return JSON.parse(raw);
    } catch {
      return emptyProgress();
    }
  }

  function saveProgress(value, storage = localStorage) {
    value.updated_at = new Date().toISOString();
    storage.setItem(STORAGE_KEY, JSON.stringify(value));
  }

  function migrateV1(value, mapping) {
    const rawState = typeof value.state === "string" ? JSON.parse(value.state || "{}") : value.state ?? {};
    const taskMap = new Map(mapping.task_mappings.map((item) => [item.old_id, item.new_id]));
    const projectMap = new Map(mapping.project_mappings.map((item) => [item.old_id, item.new_id]));
    const output = emptyProgress();
    const report = { successful: [], downgraded: [], unmapped: [], conflicts: [], rejected: [] };
    const targets = new Map();
    for (const [key, checked] of Object.entries(rawState)) {
      if (typeof checked !== "boolean") {
        report.rejected.push(key);
        continue;
      }
      if (key.startsWith("ladder-")) {
        const number = Number(key.slice(7));
        const id = projectMap.get(`V1-P${String(number).padStart(2, "0")}`);
        if (!id) report.unmapped.push(key);
        else {
          output.project_progress[id] = record(checked ? "needs_revalidation" : "not_started");
          const category = checked ? "downgraded" : "successful";
          report[category].push(key);
          targets.set(`project:${id}`, { category, key });
        }
        continue;
      }
      const match = /^stage(\d+)-(\d+)$/.exec(key);
      const oldId = match ? `V1-S${match[1]}-T${String(Number(match[2]) + 1).padStart(2, "0")}` : null;
      const id = oldId ? taskMap.get(oldId) : null;
      if (!id) {
        report.unmapped.push(key);
        continue;
      }
      let state = checked ? "lab_verified_offline" : "not_started";
      if (checked && id.startsWith("S00-")) state = "complete";
      if (id === "S03-T01") state = "needs_revalidation";
      if (id === "S04-T01") state = "validation_failed";
      if (id === "S03-T02") state = "lab_verified_offline";
      output.task_progress[id] = record(state);
      const category =
        checked && !["complete", "lab_verified_live"].includes(state)
          ? "downgraded"
          : "successful";
      report[category].push(key);
      targets.set(`task:${id}`, { category, key });
    }
    report.total = Object.values(report).filter(Array.isArray).reduce((sum, items) => sum + items.length, 0);
    report.input_total = Object.keys(rawState).length;
    report.reconciled = report.total === report.input_total;
    Object.defineProperty(report, "targets", { value: targets, enumerable: false });
    return { output, report };
  }

  function prepareImport(
    value,
    mapping,
    taskIds,
    projectIds,
    current = loadProgress(),
  ) {
    const isV2 = value.schema_version === "2.0.0";
    const migrated = isV2
      ? {
          output: value,
          report: {
            mode: "v2",
            successful: [
              ...Object.keys(value.task_progress ?? {}).map((id) => `task:${id}`),
              ...Object.keys(value.project_progress ?? {}).map((id) => `project:${id}`),
            ],
            downgraded: [],
            unmapped: [],
            conflicts: [],
            rejected: [],
          },
        }
      : migrateV1(value, mapping);
    validateProgress(migrated.output, taskIds, projectIds);
    const report = migrated.report;
    const imported = [
      ...Object.entries(migrated.output.task_progress)
        .map(([id, record]) => [`task:${id}`, record, current.task_progress[id]]),
      ...Object.entries(migrated.output.project_progress)
        .map(([id, record]) => [`project:${id}`, record, current.project_progress[id]]),
    ];
    for (const [target, incoming, existing] of imported) {
      if (!existing || existing.state === incoming.state) continue;
      const tracked = report.targets?.get(target);
      const category = tracked?.category ?? "successful";
      const key = tracked?.key ?? target;
      const index = report[category].indexOf(key);
      if (index >= 0) report[category].splice(index, 1);
      report.conflicts.push(key);
    }
    report.input_total = isV2
      ? Object.keys(value.task_progress ?? {}).length + Object.keys(value.project_progress ?? {}).length
      : report.input_total;
    report.total = [report.successful, report.downgraded, report.unmapped,
      report.conflicts, report.rejected].reduce((sum, items) => sum + items.length, 0);
    report.reconciled = report.total === report.input_total;
    if (!report.reconciled) throw new Error("迁移对账失败。");
    return migrated;
  }

  function atomicReplace(value, storage = localStorage) {
    const previous = storage.getItem(STORAGE_KEY);
    const createdAt = new Date().toISOString();
    const backupKey = `${BACKUP_PREFIX}${createdAt}`;
    let parsed;
    try {
      parsed = previous === null ? null : JSON.parse(previous);
    } catch {
      parsed = null;
    }
    const backup = {
      backup_schema_version: "1.0.0",
      created_at: createdAt,
      origin: parsed?.origin ?? (window.location.origin === "null" ? "file://" : window.location.origin),
      progress_schema_version: parsed?.schema_version ?? null,
      content_summary: {
        utf8_bytes: previous === null ? 0 : new TextEncoder().encode(previous).length,
        task_records: Object.keys(parsed?.task_progress ?? {}).length,
        project_records: Object.keys(parsed?.project_progress ?? {}).length,
      },
      previous,
    };
    storage.setItem(backupKey, JSON.stringify(backup));
    try {
      storage.setItem(STORAGE_KEY, JSON.stringify(value));
    } catch (error) {
      if (previous === null) storage.removeItem(STORAGE_KEY);
      else storage.setItem(STORAGE_KEY, previous);
      throw error;
    }
    return backupKey;
  }

  function latestBackupKey(storage = localStorage) {
    const keys = [];
    for (let index = 0; index < storage.length; index += 1) {
      const key = storage.key(index);
      if (key?.startsWith(BACKUP_PREFIX)) keys.push(key);
    }
    return keys.sort().at(-1) ?? null;
  }

  function restoreBackup(backupKey, storage = localStorage) {
    const raw = storage.getItem(backupKey);
    if (!raw) throw new Error("备份不存在。");
    const backup = JSON.parse(raw);
    if (backup.backup_schema_version !== "1.0.0" || !("previous" in backup)) {
      throw new Error("备份格式无效。");
    }
    if (backup.previous === null) storage.removeItem(STORAGE_KEY);
    else storage.setItem(STORAGE_KEY, backup.previous);
    return backup;
  }

  globalThis.ALHProgress = {
    STORAGE_KEY, emptyProgress, validateProgress, loadProgress, saveProgress, migrateV1,
    prepareImport, atomicReplace, latestBackupKey, restoreBackup, record,
  };
})();
