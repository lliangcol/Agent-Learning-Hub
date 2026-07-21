from __future__ import annotations

import runpy
import sys
from collections.abc import Callable
from pathlib import Path
from typing import cast


def main() -> int:
    """Validate curriculum content in an Agent Learning Hub source checkout."""
    script = Path.cwd() / "tools" / "validate_content.py"
    if not script.is_file():
        print(
            "alh-validate-content must be run from an Agent Learning Hub source checkout",
            file=sys.stderr,
        )
        return 2
    namespace = runpy.run_path(str(script))
    validator = cast(Callable[[], int], namespace["main"])
    return validator()


if __name__ == "__main__":
    raise SystemExit(main())
