# EXECUTION_PLAN.md 完成度审计

- 审计日期：2026-07-20
- 基线：`842d45f`
- 执行分支：`feature/agent-learning-hub-v2`
- 修复后候选：`0ad2da4` 之上的未提交工作区；提交后必须补写最终源 commit
- 证据边界：当前为未推送的本地执行分支；本地绿色不等于 GitHub CI、RC 或 Pages 已发布。

状态定义：`local-complete` 表示本地实现与对应门禁完成；`user-gate` 表示计划明确
要求维护者亲自确认；`external-gate` 表示必须由提交后的 GitHub/Pages 环境产生证据；
`verified-skip` 表示可选能力具备明确且经测试的跳过条件。

## Phase 0-2

| ID | 状态 | 证据与剩余门禁 |
| --- | --- | --- |
| P0-01 | local-complete | 分支基于 `842d45f`；未创建 `v1-baseline` tag。 |
| P0-02 | local-complete | `workbook/archive/legacy-v1/manifest.md` 记录 21 个基线文件、50 个任务及哈希。 |
| P0-03 | local-complete | 维护者确认 `file://` 与 `http://localhost:8000` 无数据、GitHub Pages 从未使用；导出、dry-run、冲突预览、数量对账、备份和回滚已自动验证。 |
| P0-04 | local-complete | `privacy-audit.md` 逐文件审计为可公开并已迁移；维护者于 2026-07-20 明确允许公开。 |
| P1-01 | local-complete | 受限 AST 计算器和逃逸语料；关键模块 100% 分支覆盖。 |
| P1-02 | verified-skip | Windows 教学流程通过；普通子进程不再称沙箱；容器命令具备隔离参数，未设置 `ALH_RUN_CONTAINER_SMOKE=1` 时明确 skip。本机 Docker daemon 不可用，未执行容器。 |
| P1-03 | local-complete | DOMPurify、文本节点搜索、CSP、Vitest 和 Playwright 恶意输入回归通过。 |
| P1-04 | local-complete | 迁移状态使用证据等级；README、课程与 archived V1 说明一致。 |
| P1-05 | local-complete | `SECURITY.md` 和威胁模型已完成；维护者指定 `lliang@outlook.com` 为私下安全报告入口。GitHub Private Vulnerability Reporting 保持 disabled，文档不声称已启用。 |
| P2-01 | local-complete | Python/Node 元数据、锁文件、extras、双安装路径和忽略规则齐全；Windows 3.11/3.12/3.14 已验证。Ubuntu 安装由 CI 待证。 |
| P2-02 | local-complete | UTF-8、LF、显式文件编码和跨平台入口规范已落盘。 |
| P2-03 | local-complete | core/providers/tools/policies/retrieval/memory/tracing 边界与可选 OpenAI Provider 已实现。 |
| P2-04 | local-complete | 92 项 Python 用例中 91 passed、可选容器 1 verified skip；整体分支覆盖率 92.99%，三项关键模块 100%。 |
| P2-05 | external-gate | Actions、Python 3.11/3.12/3.14、前端、浏览器、审计门禁均已定义；真实 Windows/Ubuntu GitHub run 必须在提交后产生。 |

## Phase 3-4

| ID | 状态 | 证据与剩余门禁 |
| --- | --- | --- |
| P3-01 | local-complete | roadmap/projects/resources/progress schema、引用和 DAG 校验通过。 |
| P3-02 | local-complete | 10 stages、50 tasks，旧 50 项均有稳定映射；每项含产出、rubric、失败与安全说明。 |
| P3-03 | local-complete | 80 项资源含信任、验证时间、状态和替代关系；内部引用检查通过。 |
| P3-04 | local-complete | README 与站点由事实源生成，`--check` 无漂移。 |
| P3-05 | local-complete | V1/V2 dry-run、未知 ID、损坏 JSON、冲突、原子替换和回滚已验证；实际 origin 已由维护者确认并登记。 |
| P3-06 | local-complete | 课程声明、资源状态和 `needs_revalidation` 边界已复核，不把可疑外链冒充可用或失效。 |
| P3-07 | local-complete | 11 个项目具备独立 ID、前置、rubric 与进度命名空间。 |
| P4-01 | local-complete | Mock 默认；OpenAI Responses 适配保留 tool call/output；严格结构化输出失败集通过。 |
| P4-02 | local-complete | 显式状态/停止原因/call ID；拒绝超过总时限才返回的 provider 结果；工具超时返回前等待工作线程结束，避免后台执行。 |
| P4-03 | local-complete | 中文离线检索、固定查询集、chunk 来源与人工标注 claim-to-chunk 引用集通过。 |
| P4-04 | local-complete | session 摘要与审计边界、SQLite schema 迁移/备份、TTL、同意、秘密拒绝和删除验证通过。 |
| P4-05 | local-complete | 统一 ToolResult、重试、幂等、缓存、审批、文件读写分权、原子写和错误脱敏通过。 |
| P4-06 | local-complete | Stage 1-9 目录与 README 八段契约由 `validate_labs.py` 强制。 |
| P4-07 | local-complete | 20 个固定场景分别实际运行最小裸 loop 与 ADR-0007 harness；结果从观察到的停止原因和工具状态计算，而非由场景标签直接赋值。 |
| P4-08 | local-complete | 可复用 Skill 和 MCP SDK 1.28.1 FastMCP 只读工具由官方内存会话测试。 |
| P4-09 | local-complete | 受控 localhost E2E 覆盖 DOM、截图、selector 变化、弹窗、404、动作日志与停止原因。 |
| P4-10 | local-complete | 单 Agent 基线与 supervisor/worker/reviewer 比较预算、轮次、无进展、成本、延迟和错误放大。 |
| P4-11 | local-complete | 三个 Capstone 方向、固定 CLI、5 个 eval case、失败用例与共享发布清单通过。 |

## Phase 5-7

| ID | 状态 | 证据与剩余门禁 |
| --- | --- | --- |
| P5-01 | local-complete | 固定导航、canonical、Open Graph、sitemap、404，无追踪脚本。 |
| P5-02 | local-complete | task/project 分离、稳定 ID、本地笔记、V1/V2 导入导出通过；V1 笔记和主题与进度在同一事务中备份、导入和回滚。 |
| P5-03 | external-gate | 360/768/桌面、键盘核心流与 axe serious/critical 为 0；语义审计完成。未安装 NVDA，正式 RC 前仍需真实屏幕阅读器抽查。 |
| P5-04 | local-complete | 稳定路由、构建搜索索引和文本安全高亮通过。 |
| P5-05 | local-complete | Vitest 16 passed；系统 Chrome 150 上 Playwright 31 passed/8 矩阵 skip。锁定 Chromium 1228 下载本轮超时，CI 需补正式证据。 |
| P5-06 | local-complete | 旧入口/锚点映射和 legacy 保留策略已实现。 |
| P5-07 | local-complete | 无 JS、无第三方运行时请求和断网可读验证通过；67 文件连续构建摘要 `70fbe914c6ac12b7d407b3729755f05c4113b3fa9163b55471d15b6b78d6f65d` 一致；四项性能预算通过。 |
| P6-01 | local-complete | 内部链接阻断、变更链接与每周全量外链工作流齐全。 |
| P6-02 | local-complete | 只读 upstream audit 生成报告，不自动合并或创建外部 Issue。 |
| P6-03 | local-complete | 贡献指南、PR/Issue 模板覆盖代码、课程、站点、测试、风险、迁移与回滚。 |
| P6-04 | external-gate | 锁文件、Dependabot、固定 Actions 与 pip/npm 审计通过；本轮修改了 Pages 工作流且新增 2 个候选文件，actionlint 与全历史 gitleaks 必须由提交后的供应链 CI 复验。GitHub 仓库级 Dependabot security updates 当前 disabled，是否启用属于外部设置。 |
| P6-05 | local-complete | LICENSE、上游署名、内容来源与隐私审计有记录。 |
| P6-06 | local-complete | `roadmap_version`、仓库 tag、弃用、兼容窗口和 RC 说明已定义；未创建 tag。 |
| P7-01 | external-gate | Pages preview/deploy 和回滚工作流已准备；需要 commit/push 后的 run、artifact、人工 smoke 与回滚演练。 |
| P7-02 | user-gate | RC 说明已更新；本轮 review 修复仍待 commit，commit、push 和 RC tag 均需分别获得明确授权。 |
| P7-03 | user-gate | CHANGELOG、兼容和回滚材料已准备；正式 tag/release/Pages 需再次确认。 |
| P7-04 | external-gate | 只能在实际发布后执行稳定观察，当前不可提前声称完成。 |

## 本地验证摘要

- Python 3.12：91 passed、1 个明确 opt-in 的容器测试 skipped；整体分支覆盖率 92.99%。
- Python 3.11.15 / 3.14.5：隔离环境各 91 passed、1 个容器 opt-in 测试 skipped。
- 前端：16 passed；Playwright：31 passed、8 个按矩阵设计 skip。
- 内容：10 stages、50 tasks、11 projects；Lab 与资源/内部链接校验通过。
- 构建：67 文件连续两次摘要均为
  `70fbe914c6ac12b7d407b3729755f05c4113b3fa9163b55471d15b6b78d6f65d`；总计
  3,028,341 bytes，定制 JavaScript 14,656 bytes。
- 供应链：pip/npm 已知漏洞 0；此前截至 `cba4191` 的 actionlint 与 gitleaks 证据仍有效，
  但不覆盖本轮未提交修复。当前候选为 227 个已跟踪文件加 2 个待跟踪文件，须由提交后的
  供应链 CI 补 actionlint 和全历史 gitleaks 证据。

## 当前停止线

本轮修复尚未 commit，且未授权 push、tag、修改仓库设置或部署 Pages。本地工作区门禁
已通过；后续仍必须由修复提交后的 GitHub Windows/Ubuntu CI、preview artifact、真实
屏幕阅读器抽查和维护者 smoke test 补齐外部证据。
