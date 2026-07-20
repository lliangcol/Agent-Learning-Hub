# ADR-0004：静态站点技术栈

- 状态：Accepted
- 日期：2026-07-20

## 决策

站点使用 MkDocs Material 构建，少量交互使用无框架的模块化 JavaScript。前端依赖通过 npm 固定并锁定；用户 Markdown 使用固定版本解析器和 DOMPurify，解析失败时降级为纯文本。

部署目标是 GitHub Pages。PR 只构建 artifact，`main` 在门禁通过后才允许正式部署。

## 后果

- 不建设 SPA。
- 静态课程正文在 JavaScript 失败时仍须可读。
- CSP、无障碍、移动端、离线退化和 Playwright/axe 测试成为发布门禁。
