(() => {
  const NOTES_KEY = "agent-learning-hub-notes-v2";

  function renderMarkdown(markdown, parser = globalThis.marked, purifier = globalThis.DOMPurify) {
    if (!parser?.parse || !purifier?.sanitize) return { html: null, text: markdown };
    const parsed = parser.parse(markdown, { gfm: true, breaks: true });
    const html = purifier.sanitize(parsed, {
      USE_PROFILES: { html: true },
      FORBID_TAGS: ["style", "svg", "math", "iframe", "object"],
      FORBID_ATTR: ["style"],
    });
    return { html, text: null };
  }

  function displayPreview(container, markdown, parser, purifier) {
    const rendered = renderMarkdown(markdown, parser, purifier);
    container.replaceChildren();
    if (rendered.html !== null) container.innerHTML = rendered.html;
    else container.textContent = rendered.text;
  }

  function loadNote(storage = localStorage) {
    return storage.getItem(NOTES_KEY) ?? "";
  }

  function saveNote(value, storage = localStorage) {
    storage.setItem(NOTES_KEY, value);
  }

  globalThis.ALHNotes = { NOTES_KEY, renderMarkdown, displayPreview, loadNote, saveNote };
})();
