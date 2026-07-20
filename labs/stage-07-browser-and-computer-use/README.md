# Stage 07 Lab：Browser 与 Computer Use

## 目标

只在仓库受控 localhost 页面上完成观察、点击、状态记录和失败恢复。

## 前置条件

Node 24、锁定的 Playwright Chromium，以及已构建的 `site-build/`。

## 运行命令

`npm run build && uv run mkdocs build --strict && npx playwright test tests/e2e/browser-lab.spec.js`

## 预期输出

测试记录 DOM snapshot、动作日志、PNG screenshot 和明确停止原因。

## 失败场景

页面选择器变化、元素缺失、弹窗、404 加载失败和最大步骤。

## 安全限制

只允许 localhost/127.0.0.1；不登录、不处理验证码、不绕过权限或访问外部站点。

## 完成标准

固定 fixture、允许域名策略、恢复路径、截图和 action log 测试通过。

## 扩展任务

增加一个受控延迟页面，验证等待预算与停止证据。
