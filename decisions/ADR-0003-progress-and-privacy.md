# ADR-0003：进度与隐私

- 状态：Accepted
- 日期：2026-07-20

## 决策

个人课程进度和项目进度分别存入 `task_progress` 与 `project_progress`，使用稳定 ID、schema version、roadmap version、证据路径和 review 结果。浏览器站点只使用版本化 localStorage，并提供预览、导入、导出、备份和冲突处理。

个人工作簿默认位于 `workbook/local/` 并被 Git 忽略；公开模板、合成示例和经审计的 legacy 档案可版本化。

## 后果

- 不提供远端同步或用户追踪。
- 导入在校验完成前不得修改现有状态。
- 凭据、完整隐私文本和未获许可的长期记忆默认拒绝持久化。
