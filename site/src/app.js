(() => {
  const searchDialog = document.querySelector('[data-md-component="search"][role="dialog"]');
  searchDialog?.setAttribute("aria-label", "站内搜索");

  let courseData;
  let projectData;
  let migrationData;
  let pendingImport;

  async function fetchJson(path) {
    const response = await fetch(path, { credentials: "same-origin" });
    if (!response.ok) throw new Error(`数据加载失败：${response.status}`);
    return response.json();
  }

  function dataUrl(name) {
    const appScript = [...document.scripts].find((script) => script.src.endsWith("/src/app.js"));
    return new URL(`../generated/data/${name}`, appScript?.src || document.baseURI).href;
  }

  function ids() {
    return {
      taskIds: new Set(courseData.stages.flatMap((stage) => stage.tasks.map((task) => task.id))),
      projectIds: new Set(projectData.projects.map((project) => project.id)),
    };
  }

  function stateIsChecked(state) {
    return ["concept_verified", "lab_verified_offline", "lab_verified_live", "complete"].includes(state);
  }

  function renderProgress() {
    const progress = ALHProgress.loadProgress();
    document.querySelectorAll("[data-task-id]").forEach((input) => {
      input.checked = stateIsChecked(progress.task_progress[input.dataset.taskId]?.state);
      if (input.dataset.progressBound !== "true") {
        input.addEventListener("change", () => {
          const current = ALHProgress.loadProgress();
          current.task_progress[input.dataset.taskId] = ALHProgress.record(
            input.checked ? "concept_verified" : "not_started",
          );
          ALHProgress.saveProgress(current);
          renderSummaries(current);
        });
        input.dataset.progressBound = "true";
      }
      input.disabled = false;
    });
    document.querySelectorAll("[data-project-id]").forEach((input) => {
      input.checked = stateIsChecked(progress.project_progress[input.dataset.projectId]?.state);
      if (input.dataset.progressBound !== "true") {
        input.addEventListener("change", () => {
          const current = ALHProgress.loadProgress();
          current.project_progress[input.dataset.projectId] = ALHProgress.record(
            input.checked ? "complete" : "not_started",
          );
          ALHProgress.saveProgress(current);
          renderSummaries(current);
        });
        input.dataset.progressBound = "true";
      }
      input.disabled = false;
    });
    renderSummaries(progress);
  }

  function renderSummaries(progress) {
    const { taskIds, projectIds } = ids();
    const taskDone = [...taskIds].filter((id) => stateIsChecked(progress.task_progress[id]?.state)).length;
    const projectDone = [...projectIds].filter((id) => stateIsChecked(progress.project_progress[id]?.state)).length;
    document.querySelectorAll("[data-progress-summary]").forEach((element) => {
      element.textContent = `课程 ${taskDone}/${taskIds.size}；可选项目 ${projectDone}/${projectIds.size}。`;
    });
  }

  function downloadJson(value, name) {
    const blob = new Blob([JSON.stringify(value, null, 2)], {
      type: "application/json;charset=utf-8",
    });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `${name}-${new Date().toISOString().replaceAll(":", "-")}.json`;
    document.body.append(link);
    link.click();
    URL.revokeObjectURL(link.href);
    link.remove();
  }

  function downloadProgress() {
    downloadJson(ALHProgress.loadProgress(), "agent-learning-hub-progress");
  }

  function collectLegacyData(storage = localStorage) {
    const notes = {};
    for (let index = 0; index < storage.length; index += 1) {
      const key = storage.key(index);
      if (key?.startsWith("note-")) notes[key] = storage.getItem(key);
    }
    return {
      schema_version: "1.0.0",
      exported_at: new Date().toISOString(),
      origin: window.location.origin === "null" ? "file://" : window.location.origin,
      state: storage.getItem("agent-learning-hub-state"),
      notes,
      theme: storage.getItem("agent-learning-theme"),
    };
  }

  function setupWorkbook() {
    const panel = document.querySelector("[data-workbook-progress]");
    if (!panel) return;
    const error = panel.querySelector("[data-progress-error]");
    const preview = panel.querySelector("[data-import-preview]");
    const report = panel.querySelector("[data-import-report]");
    panel.querySelector("[data-progress-export]").addEventListener("click", downloadProgress);
    panel.querySelector("[data-progress-rollback]").addEventListener("click", () => {
      try {
        const key = ALHProgress.latestBackupKey();
        if (!key) throw new Error("当前 origin 无导入备份。");
        ALHProgress.restoreBackup(key);
        error.textContent = "";
        panel.querySelector("[data-progress-rollback-status]").textContent =
          `已恢复备份 ${key}。`;
        renderProgress();
      } catch (caught) {
        error.textContent = caught instanceof Error ? caught.message : "恢复失败。";
      }
    });
    const legacy = collectLegacyData();
    const legacyCount =
      (legacy.state ? 1 : 0) + Object.keys(legacy.notes).length + (legacy.theme ? 1 : 0);
    panel.querySelector("[data-v1-summary]").textContent =
      legacyCount > 0
        ? `origin 有 ${legacyCount} 组 V1 数据；先导出再迁移。`
        : "origin 无 V1 数据";
    panel.querySelector("[data-v1-export]").addEventListener("click", () => {
      downloadJson(collectLegacyData(), "agent-learning-hub-v1");
    });
    const picker = panel.querySelector("[data-progress-import]");
    picker.addEventListener("change", async (event) => {
      error.textContent = "";
      try {
        const file = event.target.files[0];
        if (!file) return;
        const value = JSON.parse(await file.text());
        const knownIds = ids();
        pendingImport = ALHProgress.prepareImport(
          value,
          migrationData,
          knownIds.taskIds,
          knownIds.projectIds,
        );
        report.textContent = JSON.stringify(pendingImport.report, null, 2);
        preview.hidden = false;
      } catch (caught) {
        pendingImport = null;
        preview.hidden = true;
        error.textContent = caught instanceof Error ? caught.message : "导入失败。";
      }
    });
    picker.disabled = false;
    panel.querySelector("[data-import-confirm]").addEventListener("click", () => {
      if (!pendingImport) return;
      ALHProgress.atomicReplace(pendingImport.output);
      pendingImport = null;
      preview.hidden = true;
      renderProgress();
      panel.querySelector("[data-progress-rollback-status]").textContent =
        "导入完成；可从最近备份撤销。";
    });
    panel.querySelector("[data-import-cancel]").addEventListener("click", () => {
      pendingImport = null;
      preview.hidden = true;
    });

    const notePanel = document.querySelector("[data-workbook-notes]");
    const input = notePanel.querySelector("[data-note-input]");
    const output = notePanel.querySelector("[data-note-output]");
    const status = notePanel.querySelector("[data-note-status]");
    input.value = ALHNotes.loadNote();
    notePanel.querySelector("[data-note-preview]").addEventListener("click", () => {
      ALHNotes.displayPreview(output, input.value);
    });
    notePanel.querySelector("[data-note-save]").addEventListener("click", () => {
      ALHNotes.saveNote(input.value);
      status.textContent = "已保存";
    });
    notePanel.querySelector("[data-note-delete]").addEventListener("click", () => {
      localStorage.removeItem(ALHNotes.NOTES_KEY);
      input.value = "";
      output.replaceChildren();
      status.textContent = "笔记已删除。";
    });
  }

  async function init() {
    try {
      [courseData, projectData, migrationData] = await Promise.all([
        fetchJson(dataUrl("roadmap.json")),
        fetchJson(dataUrl("projects.json")),
        fetchJson(dataUrl("v1-to-v2.json")),
      ]);
      renderProgress();
      setupWorkbook();
    } catch (error) {
      document.querySelectorAll("[data-progress-summary]").forEach((element) => {
        element.textContent = "进度不可用；课程仍可阅读。";
      });
    }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
