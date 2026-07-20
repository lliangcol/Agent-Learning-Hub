# ADR-0002：课程唯一事实源

- 状态：Accepted
- 日期：2026-07-20

## 决策

`curriculum/roadmap.yaml`、`projects.yaml` 和 `resources.yaml` 是课程、项目与资源的唯一结构化事实源；Markdown 文件承载正文和教学解释。README、站点导航、搜索索引和统计均由这些源生成。

所有 stage、task、project 和 resource 使用永久稳定 ID。个人完成状态不写回课程生命周期状态。

## 后果

- 禁止在 README、HTML 或 JavaScript 中手工维护重复课程列表。
- schema 和内容验证器必须检查引用、路径、唯一性和依赖无环。
- 旧编号通过显式映射保留兼容关系。
