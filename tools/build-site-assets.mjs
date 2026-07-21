import { copyFile, mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { minify } from "terser";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const vendor = resolve(root, "site", "assets", "vendor");
const custom = resolve(root, "site", "assets", "custom");
const labAssets = resolve(root, "site", "assets", "labs");
await mkdir(vendor, { recursive: true });
await mkdir(custom, { recursive: true });
await mkdir(labAssets, { recursive: true });
await Promise.all([
  copyFile(resolve(root, "node_modules", "marked", "lib", "marked.umd.js"), resolve(vendor, "marked.js")),
  copyFile(resolve(root, "node_modules", "dompurify", "dist", "purify.min.js"), resolve(vendor, "purify.min.js")),
  copyFile(
    resolve(root, "labs", "stage-07-browser-and-computer-use", "fixtures", "controlled-page.html"),
    resolve(labAssets, "stage-07-controlled-page.html"),
  ),
]);

await Promise.all(
  ["progress.js", "notes.js", "app.js"].map(async (name) => {
    const source = await readFile(resolve(root, "site", "src", name), "utf8");
    const result = await minify(source, { compress: true, mangle: true, ecma: 2022 });
    if (!result.code) throw new Error(`Terser produced no output for ${name}`);
    await writeFile(resolve(custom, name.replace(".js", ".min.js")), `${result.code}\n`, "utf8");
  }),
);
