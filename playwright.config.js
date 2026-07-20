import { defineConfig } from "@playwright/test";

const executablePath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE;
const browserUse = executablePath ? { launchOptions: { executablePath } } : {};

export default defineConfig({
  testDir: "tests/e2e",
  fullyParallel: true,
  retries: 0,
  reporter: "list",
  use: {
    baseURL: "http://127.0.0.1:8123/Agent-Learning-Hub/",
    trace: "retain-on-failure",
  },
  projects: [
    { name: "desktop", use: { ...browserUse, viewport: { width: 1280, height: 800 } } },
    { name: "tablet", use: { ...browserUse, viewport: { width: 768, height: 900 } } },
    { name: "mobile", use: { ...browserUse, viewport: { width: 360, height: 800 } } },
  ],
  webServer: {
    command: "uv run python tools/serve_site.py --port 8123",
    url: "http://127.0.0.1:8123/Agent-Learning-Hub/",
    reuseExistingServer: false,
    timeout: 120000,
  },
});
