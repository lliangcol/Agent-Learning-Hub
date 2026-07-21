(() => {
  const STORAGE_KEY = "agent-learning-hub-progress-v2";
  const BACKUP_PREFIX = "agent-learning-hub-progress-backup-";
  const NOTES_KEY = "agent-learning-hub-notes-v2";
  const LEGACY_THEME_KEY = "agent-learning-theme";
  const STATES = new Set([
    "not_started", "learning", "concept_verified", "lab_verified_offline",
    "lab_verified_live", "complete", "blocked", "needs_revalidation", "validation_failed",
  ]);
  const TOP_LEVEL_FIELDS = new Set([
    "schema_version", "roadmap_version", "updated_at", "origin", "task_progress",
    "project_progress",
  ]);
  const REQUIRED_TOP_LEVEL_FIELDS = [
    "schema_version", "roadmap_version", "updated_at", "task_progress", "project_progress",
  ];
  const RECORD_FIELDS = new Set([
    "state", "updated_at", "evidence_paths", "review", "environment", "next_anchor",
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

  function isPlainObject(value) {
    return value !== null && typeof value === "object" && !Array.isArray(value);
  }

  function hasOnlyKeys(value, allowed) {
    return Object.keys(value).every((key) => allowed.has(key));
  }

  function isDateTime(value) {
    if (typeof value !== "string") return false;
    const match =
      /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d+)?(Z|[+-](\d{2}):(\d{2}))$/.exec(
        value,
      );
    if (!match) return false;
    const [, year, month, day, hour, minute, second, , zoneHour, zoneMinute] = match;
    const numericYear = Number(year);
    const numericMonth = Number(month);
    const maxDay = new Date(Date.UTC(numericYear, numericMonth, 0)).getUTCDate();
    return (
      numericMonth >= 1 &&
      numericMonth <= 12 &&
      Number(day) >= 1 &&
      Number(day) <= maxDay &&
      Number(hour) <= 23 &&
      Number(minute) <= 59 &&
      Number(second) <= 59 &&
      (zoneHour === undefined || (Number(zoneHour) <= 23 && Number(zoneMinute) <= 59)) &&
      Number.isFinite(Date.parse(value))
    );
  }

  function validateRecord(record) {
    return (
      isPlainObject(record) &&
      hasOnlyKeys(record, RECORD_FIELDS) &&
      [...RECORD_FIELDS].every((key) => Object.hasOwn(record, key)) &&
      STATES.has(record.state) &&
      isDateTime(record.updated_at) &&
      Array.isArray(record.evidence_paths) &&
      record.evidence_paths.every((path) => typeof path === "string") &&
      typeof record.review === "string" &&
      typeof record.environment === "string" &&
      typeof record.next_anchor === "string" &&
      (record.state !== "complete" || record.evidence_paths.length > 0)
    );
  }

  function validateProgress(value, taskIds, projectIds) {
    if (
      !isPlainObject(value) ||
      !hasOnlyKeys(value, TOP_LEVEL_FIELDS) ||
      !REQUIRED_TOP_LEVEL_FIELDS.every((key) => Object.hasOwn(value, key)) ||
      value.schema_version !== "2.0.0" ||
      value.roadmap_version !== "2.0.0" ||
      !isDateTime(value.updated_at) ||
      !(value.origin === undefined || value.origin === null || typeof value.origin === "string") ||
      !isPlainObject(value.task_progress) ||
      !isPlainObject(value.project_progress)
    ) {
      throw new Error("进度版本不支持。");
    }
    for (const [id, record] of Object.entries(value.task_progress)) {
      if (!taskIds.has(id) || !validateRecord(record)) throw new Error(`无效任务进度：${id}`);
    }
    for (const [id, record] of Object.entries(value.project_progress)) {
      if (!projectIds.has(id) || !validateRecord(record)) throw new Error(`无效项目进度：${id}`);
    }
    return value;
  }

  function record(
    state,
    {
      evidencePaths = [],
      review = "需补证据",
      environment = navigator.userAgent,
      nextAnchor = "补充 Lab 证据",
    } = {},
  ) {
    return {
      state,
      updated_at: new Date().toISOString(),
      evidence_paths: evidencePaths,
      review,
      environment,
      next_anchor: nextAnchor,
    };
  }

  function legacyRecord(state) {
    return record(state, {
      evidencePaths: ["workbook/archive/legacy-v1/learning-notes/PROGRESS.md"],
      review: "从 V1 布尔状态迁移；按 V2 rubric 复核证据。",
      environment: "V1 legacy snapshot; environment evidence incomplete",
      nextAnchor: "按 V2 task rubric 复核并记录新证据",
    });
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
    if (!isPlainObject(value)) throw new Error("V1 导入必须是对象。");
    const rawState = typeof value.state === "string" ? JSON.parse(value.state || "{}") : value.state ?? {};
    if (!isPlainObject(rawState)) throw new Error("V1 进度必须是对象。");
    const taskMap = new Map(mapping.task_mappings.map((item) => [item.old_id, item.new_id]));
    const projectMap = new Map(mapping.project_mappings.map((item) => [item.old_id, item.new_id]));
    const checkedStates = mapping.checked_state_by_task ?? {};
    const output = emptyProgress();
    output.origin = value.origin ?? output.origin;
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
          output.project_progress[id] = legacyRecord(
            checked ? "needs_revalidation" : "not_started",
          );
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
      const state = checked
        ? (checkedStates[id] ?? (id.startsWith("S00-") ? "complete" : "lab_verified_offline"))
        : "not_started";
      output.task_progress[id] = legacyRecord(state);
      const category =
        checked && !["complete", "lab_verified_live"].includes(state)
          ? "downgraded"
          : "successful";
      report[category].push(key);
      targets.set(`task:${id}`, { category, key });
    }
    const auxiliary = prepareLegacyAuxiliary(value);
    for (const key of auxiliary.noteKeys) report.successful.push(`note:${key}`);
    if (Object.hasOwn(auxiliary, "theme")) report.successful.push("theme");
    report.total = Object.values(report)
      .filter(Array.isArray)
      .reduce((sum, items) => sum + items.length, 0);
    report.input_total =
      Object.keys(rawState).length + auxiliary.noteKeys.length +
      (Object.hasOwn(auxiliary, "theme") ? 1 : 0);
    report.reconciled = report.total === report.input_total;
    Object.defineProperty(report, "targets", { value: targets, enumerable: false });
    return { output, report, auxiliary };
  }

  function prepareLegacyAuxiliary(value) {
    const rawNotes = value.notes ?? {};
    if (!isPlainObject(rawNotes)) throw new Error("V1 笔记必须是对象。");
    const notes = [];
    for (const [key, note] of Object.entries(rawNotes).sort(([left], [right]) => left.localeCompare(right))) {
      if (!/^note-[A-Za-z0-9._-]+$/.test(key) || typeof note !== "string") {
        throw new Error(`无效 V1 笔记：${key}`);
      }
      notes.push([key, note]);
    }
    if (!(value.theme === undefined || value.theme === null || typeof value.theme === "string")) {
      throw new Error("V1 主题必须是字符串。");
    }
    const auxiliary = { noteKeys: notes.map(([key]) => key) };
    if (notes.length > 0) {
      auxiliary.note = notes
        .map(([key, note]) => `## V1 笔记：${key}\n\n${note}`)
        .join("\n\n---\n\n");
    }
    if (typeof value.theme === "string") auxiliary.theme = value.theme;
    return auxiliary;
  }

  function prepareImport(
    value,
    mapping,
    taskIds,
    projectIds,
    current = loadProgress(),
    storage = localStorage,
  ) {
    const isV2 = isPlainObject(value) && value.schema_version === "2.0.0";
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
          auxiliary: null,
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
    if (migrated.auxiliary?.noteKeys.length) {
      const currentNote = storage.getItem(NOTES_KEY);
      if (currentNote !== null && currentNote !== migrated.auxiliary.note) {
        for (const key of migrated.auxiliary.noteKeys) {
          const label = `note:${key}`;
          const index = report.successful.indexOf(label);
          if (index >= 0) report.successful.splice(index, 1);
          report.conflicts.push(label);
        }
      }
    }
    if (Object.hasOwn(migrated.auxiliary ?? {}, "theme")) {
      const currentTheme = storage.getItem(LEGACY_THEME_KEY);
      if (currentTheme !== null && currentTheme !== migrated.auxiliary.theme) {
        const index = report.successful.indexOf("theme");
        if (index >= 0) report.successful.splice(index, 1);
        report.conflicts.push("theme");
      }
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

  function restoreStorageValue(storage, key, value) {
    if (value === null) storage.removeItem(key);
    else storage.setItem(key, value);
  }

  function atomicReplace(value, storage = localStorage, auxiliary = null) {
    const previous = storage.getItem(STORAGE_KEY);
    const touchesNote = Object.hasOwn(auxiliary ?? {}, "note");
    const touchesTheme = Object.hasOwn(auxiliary ?? {}, "theme");
    const previousNote = touchesNote ? storage.getItem(NOTES_KEY) : null;
    const previousTheme = touchesTheme ? storage.getItem(LEGACY_THEME_KEY) : null;
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
      auxiliary: {
        touches_note: touchesNote,
        previous_note: previousNote,
        touches_theme: touchesTheme,
        previous_theme: previousTheme,
      },
    };
    storage.setItem(backupKey, JSON.stringify(backup));
    try {
      storage.setItem(STORAGE_KEY, JSON.stringify(value));
      if (touchesNote) storage.setItem(NOTES_KEY, auxiliary.note);
      if (touchesTheme) storage.setItem(LEGACY_THEME_KEY, auxiliary.theme);
    } catch (error) {
      restoreStorageValue(storage, STORAGE_KEY, previous);
      if (touchesNote) restoreStorageValue(storage, NOTES_KEY, previousNote);
      if (touchesTheme) restoreStorageValue(storage, LEGACY_THEME_KEY, previousTheme);
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
    restoreStorageValue(storage, STORAGE_KEY, backup.previous);
    if (backup.auxiliary?.touches_note) {
      restoreStorageValue(storage, NOTES_KEY, backup.auxiliary.previous_note);
    }
    if (backup.auxiliary?.touches_theme) {
      restoreStorageValue(storage, LEGACY_THEME_KEY, backup.auxiliary.previous_theme);
    }
    return backup;
  }

  globalThis.ALHProgress = {
    STORAGE_KEY, NOTES_KEY, LEGACY_THEME_KEY, emptyProgress, validateProgress, loadProgress,
    saveProgress, migrateV1, prepareImport, atomicReplace, latestBackupKey, restoreBackup, record,
  };
})();
