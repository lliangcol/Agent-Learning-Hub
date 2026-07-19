"""Stage 2 Task 2: 把搜索/数据库/文件/代码执行接成工具时的安全设计示范。

这里的"沙箱"是教学简化版（子进程 + 资源限制 + 超时），
生产系统通常还需要容器/namespace 级别的隔离，这里只演示核心思路。
"""

import resource
import sqlite3
import subprocess
import sys


# ---------- 1. 数据库工具：参数化查询防 SQL 注入 ----------

def build_demo_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    conn.executemany(
        "INSERT INTO users (id, name) VALUES (?, ?)",
        [(1, "alice"), (2, "bob")],
    )
    conn.commit()
    return conn


def safe_db_query(conn, user_id):
    """参数化查询：user_id 无论是什么字符串，都只会被当作参数值，不会被当成 SQL 语法执行。"""
    cursor = conn.execute("SELECT id, name FROM users WHERE id = ?", (user_id,))
    return cursor.fetchall()


# ---------- 2. 代码执行工具：子进程 + 资源限制 + 超时 ----------

def _limit_resources():
    """在子进程里设置 CPU 时间上限（Unix only），教学简化版沙箱的一部分。

    内存上限（RLIMIT_AS）在部分沙箱化环境里会被系统拒绝设置，这里只保留 CPU 限制；
    真正兜底的是下面的 subprocess timeout，不依赖 RLIMIT_AS 也能防止失控代码卡死。
    """
    resource.setrlimit(resource.RLIMIT_CPU, (2, 2))


def run_code_sandboxed(code, timeout=2):
    """在独立子进程中执行代码，带超时和资源限制；不用 eval/exec 直接在主进程跑。"""
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout,
            preexec_fn=_limit_resources if sys.platform != "win32" else None,
        )
        return {"stdout": result.stdout[:2000], "stderr": result.stderr[:2000]}
    except subprocess.TimeoutExpired:
        return {"error": f"执行超时（>{timeout}s），已终止"}


# ---------- 3. 搜索/浏览器工具：超长内容截断 ----------

def truncate_content(text, max_chars=200):
    """硬性长度截断，是比摘要更便宜的第一层防线，避免超长网页/搜索结果撑爆 context。"""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"...(截断，原文 {len(text)} 字符)"


# ---------- 4. 文件工具：路径校验防穿越 ----------

def resolve_safe_path(base_dir, user_path):
    """把用户/模型给的路径规范化后，校验它仍然落在 base_dir 之内，否则拒绝（防路径穿越）。"""
    from pathlib import Path

    base = Path(base_dir).resolve()
    target = (base / user_path).resolve()
    if base not in target.parents and target != base:
        raise ValueError(f"拒绝访问 base 目录之外的路径: {user_path}")
    return target


def read_file_safe(base_dir, user_path):
    path = resolve_safe_path(base_dir, user_path)
    return path.read_text()


def write_file_safe(base_dir, user_path, content):
    path = resolve_safe_path(base_dir, user_path)
    path.write_text(content)
    return str(path)


if __name__ == "__main__":
    print("=== 1. 参数化查询防注入 ===")
    conn = build_demo_db()
    malicious_input = "1; DROP TABLE users; --"
    rows = safe_db_query(conn, malicious_input)
    print(f"用恶意输入 {malicious_input!r} 查询，结果: {rows}（空结果，未被当成 SQL 执行）")
    print("正常查询 id=1:", safe_db_query(conn, "1"))

    print("\n=== 2. 沙箱化代码执行 ===")
    print("正常代码:", run_code_sandboxed("print(1 + 1)"))
    print("死循环代码（应超时终止）:", run_code_sandboxed("while True: pass", timeout=1))

    print("\n=== 3. 超长内容截断 ===")
    long_text = "这是一段很长的网页正文。" * 20
    print(truncate_content(long_text, max_chars=50))

    print("\n=== 4. 路径穿越防护 ===")
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        write_file_safe(tmp, "notes.txt", "hello")
        print("正常写入/读取:", read_file_safe(tmp, "notes.txt"))
        try:
            read_file_safe(tmp, "../../etc/passwd")
        except ValueError as e:
            print("路径穿越被拒绝:", e)
