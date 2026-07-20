# ADR-0008：版本、弃用与兼容策略

- 状态：Accepted
- 日期：2026-07-20

## 决策

仓库 Git tag 是发布版本，例如 `v2.0.0-rc.1`；Python 包和静态站点共享该发布版本。课程使用独立 `roadmap_version`，因为课程内容可在不改变运行时代码契约时演进。`CHANGELOG.md` 必须记录两者的映射。

当前文件中的 `2.0.0-rc.1` 只标识候选源码，不代表 tag、release 或正式 Pages 已创建。任何 tag、release、正式部署都需要维护者分别确认。

## 兼容窗口

- V1 导出入口、旧 key 只读迁移和 legacy 档案至少保留到 `v2.1.0` 或 V2 正式发布满 30 天，以较晚者为准。
- `deprecated` 项必须给出 replacement 和最早删除版本；稳定 ID 不复用。
- 破坏性 schema 变更必须提供 dry-run 迁移、原子备份、回滚以及至少一个小版本兼容窗口。
- 发布回滚从最后验证的源 commit 重新构建新 artifact，不强推历史、不手改 Pages 产物。

## 后果

版本号可追溯但不会混淆课程与软件契约。生成候选说明是本地可逆动作；创建 Git tag、GitHub Release 或正式部署不是。
