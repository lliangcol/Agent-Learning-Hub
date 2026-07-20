# ADR-0009：站点性能与离线退化预算

- 状态：Accepted
- 日期：2026-07-20

## 基线

V1 单页为 75,376 bytes。首次 V2 严格构建为 2,934,083 bytes、67 个文件；其中自定义 JavaScript 14,280 bytes，锁定并本地托管的 marked/DOMPurify 共 72,218 bytes。V2 增量主要来自 MkDocs Material、搜索索引和 80 条结构化资源，而不是远程运行时依赖。

## 决策

- 构建总量不超过 3,500,000 bytes。
- 自定义 JavaScript 不超过 20,000 bytes。
- vendored JavaScript 不超过 90,000 bytes。
- 构建文件不超过 80 个。
- 预算由 `site/performance-budget.json` 固定，CI 运行 `tools/check_site_budget.py`。

任何提高预算的 PR 都必须给出用户收益、体积来源、移动端/离线影响和回退方案。核心课程正文由静态 HTML 提供；JavaScript、搜索或本地状态失败不得阻止阅读。

## 等价性能检查

V2 RC 使用构建体积预算、Playwright 三视口核心流程、axe、断开 JavaScript 后静态正文验证，以及“无外部运行时请求”检查作为可重复的 Lighthouse 等价门禁。正式发布前若 Pages 环境可用，再补一次 Lighthouse 抽查并记录结果；该外部抽查不能替代这些确定性门禁。
