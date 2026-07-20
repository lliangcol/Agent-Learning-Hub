import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";

test("static course remains readable and progress namespaces are separate", async ({ page }) => {
  await page.goto("generated/roadmap/");
  await expect(page.getByRole("heading", { name: "课程路线" })).toBeVisible();
  await expect(page.getByText(/课程 0\/50；可选项目 0\/11/)).toBeVisible();
  await page.locator('[data-task-id="S00-T01"]').check();
  await expect(page.getByText(/课程 1\/50；可选项目 0\/11/)).toBeVisible();
  await page.goto("generated/projects/");
  await page.locator('[data-project-id="P01"]').check();
  await expect(page.getByText(/课程 1\/50；可选项目 1\/11/)).toBeVisible();
  await page.reload();
  await expect(page.locator('[data-project-id="P01"]')).toBeChecked();
});

test("note preview neutralizes executable Markdown", async ({ page }) => {
  await page.goto("pages/workbook/");
  await page.locator("[data-note-input]").fill(
    '<script>window.pwned=true</script><img src=x onerror="window.pwned=true">[x](javascript:alert(1))',
  );
  await page.locator("[data-note-preview]").click();
  await expect(page.locator("[data-note-output] script, [data-note-output] [onerror]")).toHaveCount(0);
  await expect(page.locator('[data-note-output] [href^="javascript:"]')).toHaveCount(0);
  expect(await page.evaluate(() => window.pwned)).toBeUndefined();
});

test("V1 import previews, reconciles, replaces once and rolls back", async ({ page }) => {
  await page.goto("pages/workbook/");
  await page.locator("[data-progress-import]").setInputFiles({
    name: "v1-progress.json",
    mimeType: "application/json",
    buffer: Buffer.from(
      JSON.stringify({
        schema_version: "1.0.0",
        origin: "https://legacy.invalid",
        state: JSON.stringify({ "stage0-0": true, "ladder-1": true }),
      }),
    ),
  });
  await expect(page.locator("[data-import-preview]")).toBeVisible();
  await expect(page.locator("[data-import-report]")).toContainText('"reconciled": true');
  await page.locator("[data-import-confirm]").click();
  await page.goto("generated/roadmap/");
  await expect(page.locator('[data-task-id="S00-T01"]')).toBeChecked();
  await page.goto("pages/workbook/");
  await page.locator("[data-progress-rollback]").click();
  await expect(page.locator("[data-progress-rollback-status]")).toContainText("已恢复备份");
  await page.goto("generated/roadmap/");
  await expect(page.locator('[data-task-id="S00-T01"]')).not.toBeChecked();
});

test("search text cannot inject DOM", async ({ page }) => {
  await page.goto("./");
  const search = page.locator('input[data-md-component="search-query"]');
  if (!(await search.isVisible())) {
    await page.locator('label[for="__search"]:visible').first().click();
  }
  await search.fill('<img data-attack src=x onerror="alert(1)">');
  await expect(page.locator("img[data-attack]")).toHaveCount(0);
});

test("core pages have no critical or serious axe violations", async ({ page }) => {
  await page.goto("./");
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations.filter((item) => ["critical", "serious"].includes(item.impact))).toEqual([]);
});

test("keyboard can toggle a task and state survives reload", async ({ page }) => {
  await page.goto("generated/roadmap/");
  const task = page.locator('[data-task-id="S00-T02"]');
  await expect(task).toBeEnabled();
  await task.focus();
  await page.keyboard.press("Space");
  await expect(task).toBeChecked();
  await page.reload();
  await expect(page.locator('[data-task-id="S00-T02"]')).toBeChecked();
});

test("site makes no runtime requests to third-party origins", async ({ page }) => {
  const origins = new Set();
  page.on("request", (request) => origins.add(new URL(request.url()).origin));
  await page.goto("./");
  await page.goto("generated/roadmap/");
  expect([...origins]).toEqual(["http://127.0.0.1:8123"]);
});

test("core curriculum remains readable without JavaScript", async ({ browser }, testInfo) => {
  test.skip(testInfo.project.name !== "desktop", "one deterministic no-JavaScript check is enough");
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  await page.goto("http://127.0.0.1:8123/Agent-Learning-Hub/generated/roadmap/");
  await expect(page.getByRole("heading", { name: "课程路线" })).toBeVisible();
  await expect(page.getByText("S00-T01")).toBeVisible();
  await context.close();
});

test("mobile drawer exposes every primary destination", async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== "mobile", "mobile navigation behavior");
  await page.goto("./");
  await page.locator('.md-header label[for="__drawer"]:visible').click();
  const drawerNavigation = page
    .locator(".md-sidebar--primary:visible")
    .getByRole("navigation", { name: "导航栏" });
  for (const name of [
    "开始学习",
    "课程路线",
    "实验室",
    "项目阶梯",
    "资源目录",
    "我的工作簿",
    "贡献指南",
  ]) {
    // Material renders the active destination as current text instead of a link.
    await expect(drawerNavigation.getByText(name, { exact: true }).first()).toBeVisible();
  }
});

test("unknown route uses the custom recovery page", async ({ page }) => {
  await page.goto("missing-route/");
  await expect(page.getByRole("heading", { name: "页面未找到" })).toBeVisible();
});
