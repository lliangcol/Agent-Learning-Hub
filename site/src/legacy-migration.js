(() => {
  const STATE_KEY = "agent-learning-hub-state";
  const THEME_KEY = "agent-learning-theme";

  function currentOrigin() {
    return window.location.origin === "null" ? "file://" : window.location.origin;
  }

  function collectLegacyData(storage = window.localStorage) {
    const notes = {};
    for (let index = 0; index < storage.length; index += 1) {
      const key = storage.key(index);
      if (key?.startsWith("note-")) notes[key] = storage.getItem(key);
    }
    return {
      schema_version: "1.0.0",
      exported_at: new Date().toISOString(),
      origin: currentOrigin(),
      state: storage.getItem(STATE_KEY),
      notes,
      theme: storage.getItem(THEME_KEY),
    };
  }

  function downloadJson(payload) {
    const blob = new Blob([JSON.stringify(payload, null, 2)], {
      type: "application/json;charset=utf-8",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `agent-learning-hub-v1-${new Date().toISOString().replaceAll(":", "-")}.json`;
    document.body.append(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  }

  function init() {
    const payload = collectLegacyData();
    document.querySelector("#origin").textContent = `当前 origin：${payload.origin}`;
    const itemCount =
      (payload.state ? 1 : 0) + Object.keys(payload.notes).length + (payload.theme ? 1 : 0);
    document.querySelector("#summary").textContent =
      itemCount > 0 ? `检测到 ${itemCount} 组旧数据。` : "当前 origin 未检测到旧数据。";
    document
      .querySelector("#export")
      .addEventListener("click", () => downloadJson(collectLegacyData()));
  }

  globalThis.ALHLegacyMigration = { collectLegacyData, init };
  if (typeof document !== "undefined") init();
})();
