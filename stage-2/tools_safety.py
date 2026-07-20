"""Stage 2 Task 2：搜索、数据库、文件与代码执行工具的安全边界。

`run_code_with_timeout_demo` 只是受超时约束的教学子进程，不是安全沙箱，也不能用于
执行模型或用户提供的不可信代码。真正的任意代码执行需要容器或等价的系统级隔离。
"""

from __future__ import annotations

import sqlite3
import subprocess
import sys
from pathlib import Path

try:
    import resource
except ImportError:  # Windows does not provide the Unix resource module.
    resource = None  # type: ignore[assignment]


def build_demo_db() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    connection.executemany(
        "INSERT INTO users (id, name) VALUES (?, ?)",
        [(1, "alice"), (2, "bob")],
    )
    connection.commit()
    return connection


def safe_db_query(connection: sqlite3.Connection, user_id: str) -> list[tuple[int, str]]:
    """Treat user input as a bound parameter, never as SQL syntax."""
    cursor = connection.execute("SELECT id, name FROM users WHERE id = ?", (user_id,))
    return cursor.fetchall()


def _limit_unix_cpu() -> None:
    if resource is not None:
        resource.setrlimit(resource.RLIMIT_CPU, (2, 2))


def run_code_with_timeout_demo(code: str, timeout: float = 2) -> dict[str, object]:
    """Run trusted lesson code in a child process with a timeout; this is not a sandbox."""
    try:
        result = subprocess.run(  # noqa: S603 - executable is the current trusted interpreter
            [sys.executable, "-I", "-c", code],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
            preexec_fn=_limit_unix_cpu if resource is not None else None,
        )
    except subprocess.TimeoutExpired:
        return {"status": "fatal_error", "error_code": "timeout", "message": "演示代码执行超时。"}
    return {
        "status": "ok" if result.returncode == 0 else "fatal_error",
        "returncode": result.returncode,
        "stdout": result.stdout[:2000],
        "stderr": result.stderr[:2000],
    }


def truncate_content(text: str, max_chars: int = 200) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"…（截断，原文 {len(text)} 字符）"


def resolve_safe_path(base_dir: str | Path, user_path: str) -> Path:
    base = Path(base_dir).resolve()
    target = (base / user_path).resolve()
    if base not in target.parents and target != base:
        raise ValueError("拒绝访问允许目录之外的路径。")
    return target


def read_file_safe(base_dir: str | Path, user_path: str) -> str:
    return resolve_safe_path(base_dir, user_path).read_text(encoding="utf-8")


def write_file_safe(base_dir: str | Path, user_path: str, content: str) -> str:
    path = resolve_safe_path(base_dir, user_path)
    path.write_text(content, encoding="utf-8")
    return str(path)


if __name__ == "__main__":
    import tempfile

    print("=== 参数化查询防注入 ===")
    connection = build_demo_db()
    malicious_input = "1; DROP TABLE users; --"
    print("恶意输入结果：", safe_db_query(connection, malicious_input))
    print("正常查询结果：", safe_db_query(connection, "1"))

    print("\n=== 受超时约束的教学子进程（不是安全沙箱） ===")
    print("正常示例：", run_code_with_timeout_demo("print(1 + 1)"))
    print("超时示例：", run_code_with_timeout_demo("while True: pass", timeout=1))

    print("\n=== 路径穿越防护 ===")
    with tempfile.TemporaryDirectory() as temp_dir:
        write_file_safe(temp_dir, "notes.txt", "hello")
        print("正常读取：", read_file_safe(temp_dir, "notes.txt"))
        try:
            read_file_safe(temp_dir, "../../outside.txt")
        except ValueError as error:
            print("路径穿越被拒绝：", error)
