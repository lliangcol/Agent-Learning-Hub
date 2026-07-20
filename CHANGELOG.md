# Changelog

本项目遵循语义化 Git 发布版本；课程数据使用独立 `roadmap_version`。所有日期采用 `YYYY-MM-DD`。

## Unreleased

- 等待维护者确认 V1 各实际 origin 的浏览器状态导出/无数据结论。
- 等待 commit、push、RC tag、GitHub Release 与正式 Pages 部署的分别确认。

## 2.0.0-rc.1 - release candidate source

Roadmap version: `2.0.0`。此节是候选说明，不表示 tag 或 release 已创建。

### Added

- 10 阶段、50 个稳定课程任务与 11 个独立项目的结构化事实源、schema 和生成站点。
- Stage 1-9 离线核心 Lab/模板，安全工具调用、RAG 引用、SQLite 记忆、评测、Skill、浏览器和多 Agent 示例。
- Python/Node 锁文件、跨平台测试、内容校验、浏览器安全与无障碍门禁。
- V1 进度 dry-run/原子迁移、浏览器导出入口、隐私边界及 legacy 档案。

### Changed

- README 改为从 curriculum 数据生成；公共课程状态不再包含个人完成勾选。
- 默认 Provider 为离线 mock；真实 OpenAI Responses Provider 需显式配置，离线/真实证据分离。
- 站点改为 MkDocs 静态构建，本地依赖、CSP、净化 Markdown、无账号和无跟踪分析。

### Security

- 移除模型控制路径的危险 `eval/exec`，普通子进程不再声称为沙箱。
- 增加路径、工具权限、重试/幂等、脱敏、导入回滚和 XSS 回归测试。

### Compatibility and rollback

- V1 导出、旧 key 迁移与 legacy 资产按 ADR-0008 保留。
- 进度导入先预览和计数对账，再原子替换；失败恢复备份。
- Pages 回滚从最后验证的源 commit 重新构建 artifact，不强推历史。
