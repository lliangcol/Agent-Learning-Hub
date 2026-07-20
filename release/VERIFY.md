# 发布验证清单

所有命令必须从全新 checkout 执行。Windows 使用 PowerShell；Ubuntu 使用 CI
中的 shell。失败必须回到对应 Phase 修复，不能在发布步骤临时跳过门禁。

## 安装与静态门禁

```text
uv sync --all-extras --dev --locked
npm ci
uv run ruff format --check .
uv run ruff check .
uv run mypy src tools
uv run python tools/validate_content.py
uv run python tools/validate_labs.py
uv run python tools/build_readme.py --check
uv run python tools/check_resource_catalog.py --internal
npm test
npm run lint:md
```

## 测试、构建与浏览器

```text
uv run pytest --cov=agent_learning_hub --cov-report=term-missing
uv run pytest tests/unit/test_calculator.py tests/unit/test_registry_and_policies.py tests/unit/test_retrieval.py --cov=agent_learning_hub.tools.calculator --cov=agent_learning_hub.policies.permissions --cov=agent_learning_hub.retrieval.validation --cov-branch --cov-report=term-missing --cov-fail-under=100
uv run python tools/build_site_content.py
npm run build
git diff --exit-code -- README.md site/generated
uv run python tools/check_worktree_clean.py
uv run mkdocs build --strict
uv run python tools/check_site_budget.py
npx playwright install chromium
npm run test:e2e
git diff --check
```

浏览器门禁必须从受控 localhost 打开 `site-build/`，并使用
`/Agent-Learning-Hub/` 项目子路径。验收覆盖 360px、768px、桌面、键盘、无
JavaScript、404、axe、注入回归和第三方运行时请求。

## 迁移与安全

- 对无数据、V1 完整数据、损坏 JSON、未知 ID 和冲突数据分别执行 dry-run。
- 确认导入前备份、数量对账、用户确认、原子替换和回滚。
- 对每个实际使用过的浏览器 origin 记录“无数据”或用户主动导出的文件。
- 执行危险 `eval/exec`、未净化 `innerHTML`、凭据和 `latest` CDN 残余搜索。
- `uv run pip-audit --local` 与 `npm audit --omit=dev --audit-level=high` 必须通过。

## 发布证据

- [ ] Windows Python 3.11 和 3.14 全绿
- [ ] Ubuntu Python 3.11 和 3.14 全绿
- [ ] Ubuntu 前端、浏览器、构建、依赖和秘密扫描全绿
- [ ] 源 commit、run ID 和 artifact ID 已记录
- [ ] RC 预览已人工 smoke test
- [ ] `release/ROLLBACK.md` 已用最后一个已验证源 commit 演练
- [ ] 全量 fresh re-review 无新增 P0/P1
- [ ] tag 已获得单独确认
- [ ] Pages 正式部署已获得单独确认
