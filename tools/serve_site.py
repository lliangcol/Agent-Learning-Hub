"""Serve the built static site for local browser tests."""

from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class SiteHandler(SimpleHTTPRequestHandler):
    """Static handler that mirrors GitHub Pages custom 404 behavior."""

    base_path = "/Agent-Learning-Hub"

    def translate_path(self, path: str) -> str:
        if path == self.base_path:
            path = "/"
        elif path.startswith(f"{self.base_path}/"):
            path = path[len(self.base_path) :]
        return super().translate_path(path)

    def send_error(
        self,
        code: int,
        message: str | None = None,
        explain: str | None = None,
    ) -> None:
        if code == 404:
            content = (Path(self.directory or ".") / "404.html").read_bytes()
            self.send_response(404, message)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(content)
            return
        super().send_error(code, message, explain)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8123, type=int)
    parser.add_argument("--directory", default="site-build", type=Path)
    args = parser.parse_args()

    directory = args.directory.resolve()
    if not directory.is_dir():
        raise SystemExit(f"Built site directory does not exist: {directory}")

    handler = partial(SiteHandler, directory=str(directory))
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Serving {directory} at http://{args.host}:{args.port}/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
