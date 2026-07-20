# Contributing

Agent Learning Hub 接受小而可验证的贡献。公共课程、Labs、资源、站点与个人工作簿具有不同边界；请不要直接编辑生成的 `README.md` 或 `site/generated/`。

## 开始前

1. 创建议题或在 PR 中明确动机、影响 ID 与非目标。
2. 安装 Python 3.11+、Node 24 和锁定依赖。
3. 从结构化事实源修改，运行对应生成器与检查器。
4. 不提交 API key、个人笔记、浏览器导出、SQLite 记忆或测试 trace。

## 变更类型

### 课程修改

修改 `curriculum/roadmap.yaml` 与对应 `curriculum/stages/` 正文。永久 ID 不复用；弃用任务必须给出 replacement 与最早删除版本。运行内容 schema、DAG、README 和站点生成检查，并说明 rubric、失败场景及安全边界。

### 资源新增、替换或归档

在 `curriculum/resources.yaml` 中提供来源类型、发布者、关联阶段、可信度、验证日期和许可证/访问说明。优先官方文档、论文和维护者仓库。一次失败只标记 `suspect`；人工确认后才能归档或替换。

### Lab 代码

同时提交 starter、solution、固定 fixture、expected output 和测试。默认必须离线；真实 Provider 必须显式选择并区分证据。不得把普通子进程描述成沙箱，不得默认运行不可信代码。

### 网站交互

保持静态、无跟踪分析、无云同步。用户内容只能使用 `textContent` 或经锁定解析器与 DOMPurify 清洗。验证 360px、768px、桌面、键盘、恶意输入及 axe。

### 个人示例工作簿

只有合成、脱敏、获得公开许可且完成版权检查的内容可进入 `workbook/examples/`。真实个人状态只能放在被忽略的 `workbook/local/` 或浏览器本地存储。

### 安全问题

不要公开提交可利用的漏洞、密钥或个人数据。按照 `SECURITY.md` 使用维护者确认的
安全邮箱私下报告；不得把公开 Issue 当作替代入口。

## 验证

```powershell
uv sync --all-extras --dev --locked
uv run ruff format --check .
uv run ruff check .
uv run mypy src tools
uv run pytest --cov=agent_learning_hub --cov-report=term-missing
uv run python tools/validate_content.py
uv run python tools/validate_labs.py
uv run python tools/build_readme.py --check
uv run python tools/check_resource_catalog.py --internal
npm ci
npm test
npm run lint:md
npm run build
uv run mkdocs build --strict
uv run python tools/check_site_budget.py
npx playwright test
git diff --check
```

关键安全模块还必须达到 `release/VERIFY.md` 记录的 100% 分支覆盖率；发布候选另需执行依赖、秘密、外链、全新 checkout 和回滚门禁。

外链全量审计由每周 workflow 或维护者手动执行；PR 默认阻断内部引用错误，并审查本次新增/修改链接。

## PR 内容

PR 必须列出范围与动机、影响 ID、实际命令和输出、截图（UI 变更）、风险、迁移、回滚以及外部来源/许可证。上游同步只能提交差异报告或经人工选择的映射，不允许自动合并。

## 许可证与署名

提交即表示你有权按仓库 MIT 许可证提供新增代码和文本。外部内容只提供必要引用与链接，不复制未获许可材料；保留 Datawhale、原维护者与外部贡献者署名。
