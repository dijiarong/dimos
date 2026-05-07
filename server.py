#!/usr/bin/env python3
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class HelloHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/":
            body = b"helloworld"
        elif self.path == "/time":
            body = datetime.now().astimezone().isoformat().encode("utf-8")
        else:
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if self.path != "/login":
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._send_json(400, {"ok": False, "message": "invalid json"})
            return

        username = payload.get("username")
        password = payload.get("password")
        if username == "root" and password == "123456":
            self._send_json(200, {"ok": True, "message": "login success"})
            return

        self._send_json(401, {"ok": False, "message": "invalid credentials"})

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return


def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    server = HTTPServer((host, port), HelloHandler)
    print(f"HTTP server listening on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
