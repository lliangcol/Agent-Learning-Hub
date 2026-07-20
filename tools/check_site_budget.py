"""Enforce the reviewed static-site artifact budget."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).parents[1]
SITE = ROOT / "site-build"
CONFIG = ROOT / "site" / "performance-budget.json"


def total_size(paths: list[Path]) -> int:
    return sum(path.stat().st_size for path in paths if path.is_file())


def measurements() -> dict[str, int]:
    if not SITE.is_dir():
        raise FileNotFoundError("site-build does not exist; run mkdocs build first")
    files = [path for path in SITE.rglob("*") if path.is_file()]
    custom_javascript = list((SITE / "src").rglob("*.js"))
    vendored_javascript = list((SITE / "assets" / "vendor").rglob("*.js"))
    return {
        "site_bytes": total_size(files),
        "custom_javascript_bytes": total_size(custom_javascript),
        "vendored_javascript_bytes": total_size(vendored_javascript),
        "file_count": len(files),
    }


def main() -> int:
    config = cast(dict[str, Any], json.loads(CONFIG.read_text(encoding="utf-8")))
    budget = cast(dict[str, int], config["budget"])
    actual = measurements()
    failed = False
    for name, value in actual.items():
        limit = budget[name]
        state = "PASS" if value <= limit else "FAIL"
        print(f"{state} {name}: {value} <= {limit}")
        failed = failed or value > limit
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
