# V1 基线资产清单

- 快照时间：2026-07-20（Asia/Shanghai）
- 基线分支：`main`
- 基线提交：`842d45fc1ebac4ca03f280f973d0bdcdab5bd3e6`
- 远端状态：快照时 `HEAD == origin/main`
- 跟踪文件数：21
- 说明：`EXECUTION_PLAN.md` 在执行开始时是未跟踪的用户提供文件，因此不属于上述 21 个基线跟踪文件，但会随 V2 工作保留。

## 跟踪文件与 SHA-256

| SHA-256 | 路径 |
| --- | --- |
| `fe07aeae2cfd1ff2ce4c0c5911dfbb550a3f1065e213175039abadfc3a5a15bb` | `.gitignore` |
| `353d4a887346c21aa139d38a5eca0ff437df6896745205292702a6920dd81008` | `CLAUDE.md` |
| `bdd4643f79089ef86a0a1d57ec1f5d787dd3bbb02913c2f3fd5d98effb6a4d2b` | `CONTRIBUTING.md` |
| `d452c451d60aa13038fcda877a4705065f694a2a6dabc23d37770e2ea7fc037f` | `LICENSE` |
| `5f38886ff66afb730ce3c0d4d78a60be4c367a970a3c2ad910f95d965ddf0c5a` | `README.md` |
| `0d7c9ec4cf26ca22695c93d928f75f68f0c1ba6bd046d7b10c7a96a1862c282d` | `index.html` |
| `f25f14c75b6ea8342ea5240464abc50cfc70d3e0b0c9dba8970f12b54ca7ea96` | `learning-notes/PROGRESS.md` |
| `279e578233c76510a0f3c03591ea73e71897ebd10330407d725fa9465f554a1c` | `learning-notes/README.md` |
| `ba092cdd5f5fbaaf35e7720e4e25c6e05349ec8384be3be69a16cd3f6d90e3eb` | `learning-notes/stage-0-agent-basics.md` |
| `01b14ed8ed277729831bbce98911ab4148ca16a8bfbb1957d43a42b3c2658d4b` | `learning-notes/stage-1-minimal-agent-loop.md` |
| `fc8a692a0953acd6085816da7b993ccc8c1ae0f0dd5cdb4df8ed2cab25417db8` | `learning-notes/stage-2-tool-use-rag-memory.md` |
| `842e9543ab23222758adbde7d49257998b873ec572f29df46481d3aaf960829a` | `learning-notes/templates/stage-note-template.md` |
| `9a2328de06b958054f7915f3e0ab521a6bed2d8e77d4ea723327e208769aa986` | `stage-1/chat.py` |
| `8cb7d39cc6079f2c815ed8f913bc8b76f91eb02ab745a0b88ab7921741e47a71` | `stage-1/task2_json.py` |
| `509136a465c609226d993a0c578a1748502e8f897f1a060a3ddee7d85482ffc3` | `stage-1/task3_tools.py` |
| `d3043edc803d66e852eb06eaa2e82864c0886c15b3bb9e115d2a2b73c9db21e2` | `stage-1/task4_tool_call.py` |
| `9f1a66351f132a7f6dcf45554e14a648b9efb5eaffd8d19abc467a204e1c1851` | `stage-1/task5_execute.py` |
| `5503a56ee06d9bdee81868288b0302d4434f55cef2289d78ae6ffd3989f0c02f` | `stage-1/task6_agent_loop.py` |
| `d1a283eb6f139a5aea69d9eb923fc2b94787608a12642486a97021b89976f564` | `stage-2/memory.py` |
| `2771e61a0e19128fe752f992151680bd10cf969970729452292ae8e4cbf57215` | `stage-2/rag.py` |
| `8c040f474fa69bbfc67213b5b593fa2be054bbcfddd01fff1e44c57986fa4011` | `stage-2/tools_safety.py` |

## 学习状态快照

- README 课程任务：50 项，其中 11 项勾选。
- Stage 2 笔记：Task 1-3 共 3 项勾选。
- 当前锚点：Stage 2 Task 4，等待回答“工具失败、空结果、重复调用、幻觉引用”的 4 道检查题。
- 最后记录日期：2026-07-18。
- Project Ladder：11 项；V1 没有独立的结构化项目进度命名空间。

## 运行环境与基线结果

- Windows / PowerShell
- Python `3.12.13`
- uv `0.11.19`
- Node.js `v24.16.0`
- npm `11.13.0`

以下脚本在 2026-07-20 直接以 `python <path>` 运行：

| 脚本 | 结果 |
| --- | --- |
| `stage-1/chat.py` | 退出码 0 |
| `stage-1/task2_json.py` | 退出码 0 |
| `stage-1/task3_tools.py` | 退出码 0；包含危险 `eval()` |
| `stage-1/task4_tool_call.py` | 退出码 0 |
| `stage-1/task5_execute.py` | 退出码 0；包含危险 `eval()` |
| `stage-1/task6_agent_loop.py` | 退出码 0；包含危险 `eval()` |
| `stage-2/rag.py` | 退出码 0；经 PowerShell 管道捕获时中文乱码 |
| `stage-2/memory.py` | 退出码 0；经 PowerShell 管道捕获时中文乱码，且所谓长期记忆仅在进程内 |
| `stage-2/tools_safety.py` | 退出码 1；Windows 缺少 `resource` 模块 |

## 已知恢复路径

- Git 文件：以基线提交 `842d45f` 为不可变参照，不创建 tag、不重写历史。
- 学习笔记：迁移时使用 `git mv`，本清单保留原路径和哈希。
- 浏览器数据：见 `local-storage-origins.md`；在 V2 导入验证完成前保留旧键和旧导出入口。
