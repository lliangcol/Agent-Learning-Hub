from __future__ import annotations

import argparse
import json
from pathlib import Path


def collect(paths: list[Path]) -> list[dict[str, str]]:
    records = []
    for path in paths:
        if path.suffix.casefold() != ".md" or not path.is_file():
            raise ValueError(f"not an existing Markdown file: {path}")
        records.append({"source": str(path), "content": path.read_text(encoding="utf-8")})
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    print(json.dumps(collect(args.paths), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
