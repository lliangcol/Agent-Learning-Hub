"""Validate internal references and audit the external resource catalog."""

from __future__ import annotations

import argparse
import concurrent.futures
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, cast

import yaml

ROOT = Path(__file__).parents[1]
CATALOG = ROOT / "curriculum" / "resources.yaml"
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
MARKDOWN_ROOTS = (
    "README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "curriculum",
    "decisions",
    "labs",
    "site",
    "workbook",
)


@dataclass(frozen=True)
class LinkResult:
    resource_id: str
    url: str
    ok: bool
    detail: str


def load_catalog() -> dict[str, Any]:
    return cast(dict[str, Any], yaml.safe_load(CATALOG.read_text(encoding="utf-8")))


def markdown_files() -> list[Path]:
    files: list[Path] = []
    for name in MARKDOWN_ROOTS:
        path = ROOT / name
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(path.rglob("*.md"))
    return sorted(path for path in files if "archive" not in path.parts)


def check_internal() -> list[str]:
    errors: list[str] = []
    catalog = load_catalog()
    resources = cast(list[dict[str, Any]], catalog.get("resources", []))
    resource_ids = [str(resource.get("id", "")) for resource in resources]
    if len(resource_ids) != len(set(resource_ids)):
        errors.append("resource IDs are not unique")

    for resource in resources:
        resource_id = str(resource.get("id", "<missing>"))
        url = str(resource.get("url", ""))
        status = resource.get("status")
        verified = resource.get("last_verified_at")
        replacement = resource.get("replacement_id")
        if not url.startswith("https://"):
            errors.append(f"{resource_id}: URL must use HTTPS")
        if status == "active" and not verified:
            errors.append(f"{resource_id}: active resource has no verification date")
        if status == "replaced" and not replacement:
            errors.append(f"{resource_id}: replaced resource has no replacement_id")
        if replacement and replacement not in resource_ids:
            errors.append(f"{resource_id}: unknown replacement_id {replacement}")

    for source in markdown_files():
        text = source.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("#", "https://", "http://", "mailto:")):
                continue
            parsed = urllib.parse.urlsplit(target)
            relative = urllib.parse.unquote(parsed.path)
            if not relative:
                continue
            resolved = (source.parent / relative).resolve()
            if not resolved.exists():
                errors.append(f"{source.relative_to(ROOT)}: missing link target {target}")
    return errors


def request_url(resource_id: str, url: str, timeout: float, retries: int) -> LinkResult:
    if urllib.parse.urlsplit(url).scheme != "https":
        return LinkResult(resource_id, url, False, "rejected non-HTTPS URL")
    headers = {
        "User-Agent": "Agent-Learning-Hub-link-audit/2.0 (+https://github.com/lliangcol/Agent-Learning-Hub)"
    }
    last_detail = "not attempted"
    for attempt in range(retries + 1):
        for method in ("HEAD", "GET"):
            try:
                request = urllib.request.Request(url, headers=headers, method=method)  # noqa: S310
                with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
                    code = response.status
                    if 200 <= code < 400:
                        return LinkResult(resource_id, url, True, f"HTTP {code}")
                    last_detail = f"HTTP {code}"
            except urllib.error.HTTPError as error:
                last_detail = f"HTTP {error.code}"
                if error.code not in {403, 405, 429} and error.code < 500:
                    break
            except (urllib.error.URLError, TimeoutError, OSError) as error:
                last_detail = f"{type(error).__name__}: {error}"
                break
        if attempt < retries:
            time.sleep(min(2**attempt, 4))
    return LinkResult(resource_id, url, False, last_detail)


def check_external(
    timeout: float, retries: int, workers: int, selected_ids: set[str] | None = None
) -> list[LinkResult]:
    resources = cast(list[dict[str, Any]], load_catalog()["resources"])
    if selected_ids:
        resources = [item for item in resources if str(item["id"]) in selected_ids]
        found = {str(item["id"]) for item in resources}
        unknown = selected_ids - found
        if unknown:
            raise ValueError(f"Unknown resource IDs: {', '.join(sorted(unknown))}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(request_url, str(item["id"]), str(item["url"]), timeout, retries)
            for item in resources
        ]
        return sorted(
            (future.result() for future in futures), key=lambda result: result.resource_id
        )


def update_catalog(results: list[LinkResult]) -> None:
    catalog = load_catalog()
    by_id = {result.resource_id: result for result in results}
    for resource in cast(list[dict[str, Any]], catalog["resources"]):
        result = by_id.get(str(resource["id"]))
        if result is None:
            continue
        resource["last_verified_at"] = date.today().isoformat()
        if result.ok:
            resource["status"] = "active"
        elif resource.get("status") == "active":
            resource["status"] = "suspect"
    CATALOG.write_text(
        yaml.safe_dump(catalog, allow_unicode=True, sort_keys=False, width=1000),
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--internal", action="store_true")
    mode.add_argument("--external", action="store_true")
    parser.add_argument(
        "--update", action="store_true", help="Update verification dates and status"
    )
    parser.add_argument("--timeout", type=float, default=12.0)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--ids", nargs="*", help="Only audit selected resource IDs")
    args = parser.parse_args()

    if args.internal:
        errors = check_internal()
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print("Resource catalog and internal Markdown links are valid.")
        return 0

    results = check_external(args.timeout, args.retries, args.workers, set(args.ids or []))
    if args.update:
        update_catalog(results)
    for result in results:
        state = "OK" if result.ok else "SUSPECT"
        print(f"{state} {result.resource_id} {result.detail} {result.url}")
    failed = sum(not result.ok for result in results)
    print(f"External audit: {len(results) - failed} active, {failed} suspect.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
