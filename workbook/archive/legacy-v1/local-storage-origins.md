# V1 浏览器本地状态登记

旧站点的 localStorage 只存在于用户实际打开过的浏览器 origin 中；仓库脚本和 CI 不读取浏览器数据。

| Origin | 状态 | 维护者确认（2026-07-20） |
| --- | --- | --- |
| `file://`（直接打开旧 `index.html`） | 无数据 | 不需要导出 |
| `http://localhost:8000` | 无数据 | 不需要导出 |
| `https://lliangcol.github.io/Agent-Learning-Hub/` | 从未使用 | 不存在需要迁移的浏览器状态 |

维护者未报告其他实际使用过的 V1 origin。若发布前发现遗漏的端口、主机名、协议或
浏览器配置文件，必须把它作为独立 origin 补充登记，并在继续发布前完成“无数据”或
“已导出”确认。

导出范围必须包含：

- `agent-learning-hub-state`
- 所有 `note-*` 键
- `agent-learning-theme`
- 导出 schema 版本、origin 和导出时间

在迁移测试通过前，V2 不删除或覆盖这些旧键。导出文件是个人数据，不得提交到仓库。
