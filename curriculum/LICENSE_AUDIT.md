# License and attribution audit

审计日期：2026-07-20。

| 资产 | 来源与权利 | 处理结论 |
| --- | --- | --- |
| 新增 Python、JavaScript、课程文本与模板 | 本仓库原创整改内容 | 由仓库 MIT License 覆盖 |
| V1 README、HTML、示例和学习笔记 | 基线仓库；MIT，版权声明为 jjyaoao | 保留原 LICENSE、维护者署名与 legacy 档案 |
| Datawhale 上游 | `datawhalechina/Agent-Learning-Hub`；MIT | 保留链接与署名；吸收改动前单独比对和 review |
| 外部学习资源 | `resources.yaml` 所列站点 | 仅链接和短说明，不再分发正文；逐项记录访问说明 |
| MkDocs Material、marked、DOMPurify、测试依赖 | 锁文件安装的第三方软件 | 不复制其源码到课程；构建所需 marked/DOMPurify 文件由锁定包生成，许可证随 npm 包可审计 |
| 图标 | MkDocs Material 主题内建资源 | 随锁定主题构建，无自制或额外抓取图标 |
| 字体、图片、音视频 | 无仓库自带资产 | 站点禁用远程字体；新增前必须确认再分发权利 |
| 测试页面与数据 | 本仓库合成 fixture | 不含个人、公司或第三方受限数据 |
| 公开工作簿示例 | V1 内容脱敏审计与合成迁移结果 | 隐私审计通过；公开前继续保留来源说明，不包含浏览器真实导出 |

审计未授予对外部链接内容的再分发许可。贡献者必须遵守 `CONTRIBUTING.md` 的来源、引用和个人数据要求。
