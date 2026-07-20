# 发布流程

本目录描述 Agent Learning Hub 的发布候选、正式发布和回滚流程。仓库中的
版本号、CHANGELOG 或候选说明不等于已经发布；commit、push、tag 和 Pages
正式部署分别需要维护者明确确认。

## 发布顺序

1. 在执行分支完成 `release/VERIFY.md` 的本地门禁。
2. 经确认后按 `EXECUTION_PLAN.md` 的里程碑边界提交并推送。
3. 在全新 Windows 和 Ubuntu checkout 中复现质量门禁；Ubuntu 证据由 CI 产生。
4. 记录源 commit、CI workflow run 和 Pages artifact 标识。
5. 经单独确认后创建 `v2.0.0-rc.1`，执行预览和一次回滚演练。
6. 收口 RC 问题并重新执行全量 review-fix-re-review。
7. 再次确认范围和历史后创建 `v2.0.0`，随后才允许 Pages 正式部署。

正式站点不收集分析数据。legacy 入口至少保留到 `v2.1.0` 发布或 V2 正式发布
满 30 天，以较晚者为准。

## 记录要求

每次部署或回滚至少记录：

- 发布版本和 `roadmap_version`
- 完整源 commit SHA
- CI workflow run URL/ID
- Pages artifact ID
- 验证时间、执行人和结果
- 迁移检查、已知限制和回滚目标

回滚步骤见 `release/ROLLBACK.md`；当前候选状态见
`release/v2.0.0-rc.1.md`。
