import importlib.util
import os
import shutil
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
    docker = shutil.which("docker")
    assert docker is not None
    try:
        daemon = subprocess.run(  # noqa: S603 - resolved Docker binary, fixed arguments
            [docker, "info"],
            capture_output=True,
            check=False,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        pytest.skip(f"Docker daemon preflight unavailable: {type(error).__name__}")
    if daemon.returncode != 0:
        pytest.skip("Docker daemon is unavailable")
    image = MODULE.isolated_python_command()[-5]
    try:
        image_check = subprocess.run(  # noqa: S603 - resolved Docker binary, fixed arguments
            [docker, "image", "inspect", image],
            capture_output=True,
            check=False,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        pytest.skip(f"Docker image preflight unavailable: {type(error).__name__}")
    if image_check.returncode != 0:
        pytest.skip(f"reviewed image is unavailable locally: {image}")
    try:
        completed = subprocess.run(  # noqa: S603 - fixed reviewed command, explicit opt-in
            MODULE.isolated_python_command(),
            capture_output=True,
            check=False,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        pytest.fail(f"reviewed container command failed: {type(error).__name__}")
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.strip() == "trusted optional container smoke"
