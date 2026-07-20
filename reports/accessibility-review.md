# V2 无障碍抽查记录

- 日期：2026-07-20
- 环境：Windows，系统 Chrome 150，Playwright 1.61.1
- 范围：首页、路线图、项目、工作簿、360px、768px、1280px

## 已验证

- Playwright 可用键盘聚焦并切换课程任务，刷新后状态保留。
- 360px 抽屉可访问全部一级导航；768px 和桌面核心路径通过。
- 原生 `nav`、`main`、heading、button 和 checkbox 语义存在；包含 skip link、
  可见焦点、状态播报和关联错误区域。
- axe 自动扫描未发现 critical 或 serious 问题。
- 无 JavaScript 时课程正文仍可阅读；颜色不是唯一状态表达。

## 手工门禁

本机未检测到 NVDA，因此没有伪造屏幕阅读器已验证结论。正式 RC 预览必须由维护者
或学习者使用 NVDA/JAWS/VoiceOver 至少抽查：一级导航、路线图 checkbox、搜索、
工作簿导入错误、笔记保存状态和 404 恢复链接。该人工结果需与源 commit、浏览器和
屏幕阅读器版本一起记录。
