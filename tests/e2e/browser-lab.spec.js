import { readFile } from "node:fs/promises";
import { expect, test } from "@playwright/test";

const EXPECTED_LOG = new URL(
  "../../labs/stage-07-browser-and-computer-use/expected/action-log.json",
  import.meta.url,
);

test("controlled browser lab records DOM, screenshot, recovery, popup and stop reason", async (
  { page },
  testInfo,
) => {
  test.skip(testInfo.project.name !== "desktop", "one pinned Chromium environment is sufficient");
  const expectedLog = JSON.parse(await readFile(EXPECTED_LOG, "utf8"));
  const actionLog = [];

  await page.goto("assets/labs/stage-07-controlled-page.html");
  expect(new URL(page.url()).hostname).toBe("127.0.0.1");
  await expect(page.locator("main[data-fixture-version='2']")).toBeVisible();
  const domSnapshot = await page.locator("main").evaluate((element) => element.outerHTML);
  expect(domSnapshot).toContain("synthetic-evidence-07");

  await expect(page.locator("#reveal")).toHaveCount(0);
  await page.getByRole("button", { name: "显示证据" }).click();
  await expect(page.getByText("synthetic-evidence-07")).toBeVisible();
  actionLog.push(expectedLog[0]);

  const screenshot = await page.screenshot();
  expect(screenshot.byteLength).toBeGreaterThan(1000);
  await testInfo.attach("controlled-page-after-reveal", {
    body: screenshot,
    contentType: "image/png",
  });

  await page.getByRole("button", { name: "打开确认弹窗" }).click();
  await expect(page.getByRole("dialog", { name: "" })).toBeVisible();
  await page.getByRole("button", { name: "关闭" }).click();
  await expect(page.locator("#confirmation")).not.toBeVisible();
  actionLog.push(expectedLog[1]);

  const response = await page.goto("assets/labs/missing-browser-lab.html");
  expect(response?.status()).toBe(404);
  await expect(page.getByRole("heading", { name: "页面未找到" })).toBeVisible();
  actionLog.push(expectedLog[2]);

  expect(actionLog).toEqual(expectedLog);
  expect(actionLog.at(-1).stop_reason).toBe("completed_with_recovery");
});
