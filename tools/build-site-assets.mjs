import { copyFile, mkdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const vendor = resolve(root, "site", "assets", "vendor");
const labAssets = resolve(root, "site", "assets", "labs");
await mkdir(vendor, { recursive: true });
await mkdir(labAssets, { recursive: true });
await Promise.all([
  copyFile(resolve(root, "node_modules", "marked", "lib", "marked.umd.js"), resolve(vendor, "marked.js")),
  copyFile(resolve(root, "node_modules", "dompurify", "dist", "purify.min.js"), resolve(vendor, "purify.min.js")),
  copyFile(
    resolve(root, "labs", "stage-07-browser-and-computer-use", "fixtures", "controlled-page.html"),
    resolve(labAssets, "stage-07-controlled-page.html"),
  ),
]);
