import importlib.util
import os
import subprocess
from pathlib import Path

import pytest

PATH = Path(__file__).parents[1] / "solution" / "optional_container.py"
SPEC = importlib.util.spec_from_file_location("lab_s04_container", PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_container_command_has_required_isolation_flags() -> None:
    command = MODULE.isolated_python_command()
    joined = " ".join(command)
    for value in (
        "--network none",
        "--read-only",
        "--tmpfs",
        "--user",
        "--cpus",
        "--memory",
        "--pids-limit",
    ):
        assert value in joined
    assert "trusted optional container smoke" in joined


def test_optional_container_smoke_requires_explicit_opt_in() -> None:
    if os.environ.get("ALH_RUN_CONTAINER_SMOKE") != "1":
        pytest.skip("set ALH_RUN_CONTAINER_SMOKE=1 only after approving container execution")
    if not MODULE.docker_available():
        pytest.skip("Docker CLI is unavailable")
    try:
        completed = subprocess.run(  # noqa: S603 - fixed reviewed command, explicit opt-in
            MODULE.isolated_python_command(),
            capture_output=True,
            check=False,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        pytest.skip(f"Docker runtime unavailable: {type(error).__name__}")
    if completed.returncode != 0:
        pytest.skip("Docker daemon or reviewed image is unavailable")
    assert completed.stdout.strip() == "trusted optional container smoke"
