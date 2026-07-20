---
title: 我的工作簿
description: 本地进度、笔记与 V1 数据迁移
---

# 我的工作簿

进度和笔记默认只保存在当前浏览器。不同 origin 的 localStorage 不共享；导出文件可能包含个人内容，不要提交到仓库。

<div class="workbook-panel" data-workbook-progress>
  <h2>进度数据</h2>
  <p data-progress-summary role="status" aria-live="polite">正在加载课程数据…</p>
  <div class="button-row">
    <button type="button" data-progress-export>导出 V2 JSON</button>
    <button type="button" data-v1-export>导出当前 origin 的 V1 JSON</button>
    <button type="button" data-progress-rollback>恢复最近导入备份</button>
    <label class="file-button">选择 V1/V2 JSON<input type="file" accept="application/json" data-progress-import></label>
  </div>
  <p data-v1-summary role="status"></p>
  <p data-progress-rollback-status role="status" aria-live="polite"></p>
  <div data-import-preview hidden>
    <h3>导入预览</h3>
    <pre data-import-report></pre>
    <button type="button" data-import-confirm>确认原子替换</button>
    <button type="button" data-import-cancel>取消</button>
  </div>
  <p data-progress-error class="error" role="alert"></p>
</div>

<div class="workbook-panel" data-workbook-notes>
  <h2>本地 Markdown 笔记</h2>
  <label for="workbook-note">笔记内容</label>
  <textarea id="workbook-note" rows="10" data-note-input></textarea>
  <div class="button-row">
    <button type="button" data-note-preview>安全预览</button>
    <button type="button" data-note-save>保存到当前浏览器</button>
    <button type="button" data-note-delete>删除本地笔记</button>
  </div>
  <p data-note-status role="status" aria-live="polite"></p>
  <div data-note-output class="note-output" aria-label="笔记安全预览"></div>
</div>
