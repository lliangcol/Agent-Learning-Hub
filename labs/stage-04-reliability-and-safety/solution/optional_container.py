from __future__ import annotations

import shutil


def docker_available() -> bool:
    return shutil.which("docker") is not None


def isolated_python_command(image: str = "python:3.12-alpine") -> list[str]:
    """Return a reviewed command; callers still need explicit approval before execution."""
    return [
        "docker",
        "run",
        "--rm",
        "--network",
        "none",
        "--read-only",
        "--tmpfs",
        "/work:rw,noexec,nosuid,size=16m",
        "--workdir",
        "/work",
        "--user",
        "65534:65534",
        "--cpus",
        "0.5",
        "--memory",
        "128m",
        "--pids-limit",
        "64",
        image,
        "python",
        "-I",
        "-c",
        "print('trusted optional container smoke')",
    ]
