# Pages 回滚手册

回滚的唯一发布路径是从最后一个已验证的源 commit 重新构建并部署新
artifact。不得强推、重写历史或直接编辑 Pages 产物。

## 前置证据

在开始前记录：

- 当前故障部署的版本、源 commit、workflow run 和 artifact ID
- 回滚目标的完整源 commit，以及它上一次通过的 CI run 和人工 smoke 结果
- 回滚原因、影响范围和维护者批准

## 演练和正式回滚

1. 在临时目录全新 checkout 回滚目标 commit；不要移动或删除现有工作区。
2. 按 `release/VERIFY.md` 安装锁定依赖并执行全部适用门禁。
3. 连续构建两次站点，对排序后的相对路径和文件 SHA-256 清单求摘要；两次必须一致。
4. 在 localhost 的 `/Agent-Learning-Hub/` 子路径验证首页、课程、工作簿、404、
   迁移 dry-run 和移动端导航。
5. 经 Pages 部署确认后，从该源 commit 重新运行 `pages.yml`，生成并部署新 artifact。
6. 记录新的 workflow run、artifact ID、Pages URL 和部署时间。
7. 部署后检查浏览器控制台、内部链接、版本标识和迁移入口。

## 失败和恢复

- 构建或验证失败：停止部署，保留当前在线 artifact，修复源代码后重新开始。
- 部署失败但旧站仍可用：不要修改 Pages 产物，重试受控 workflow。
- 数据迁移反馈异常：保留 legacy 键和入口，引导用户使用导出备份恢复；不得自动
  读取或覆盖用户浏览器数据。
- 找不到已验证 commit 或 CI 证据：停止回滚并请求维护者选择目标。

RC 阶段只有在真实源 commit、CI run 和 Pages preview artifact 都存在后，才可把
本手册标记为“已演练”。本地未提交工作树的双构建一致性检查只是准备证据，不是
正式回滚演练。
