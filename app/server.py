from __future__ import annotations

import io
import json
import mimetypes
import os
from pathlib import Path
from typing import Callable, Iterable
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

from .data_store import JsonFileStore
from .service import HabitService

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"
DATA_FILE = BASE_DIR / "data" / "habits.json"

StartResponse = Callable[[str, list[tuple[str, str]]], None]


def create_app(service: HabitService | None = None) -> Callable[[dict, StartResponse], Iterable[bytes]]:
    habit_service = service or HabitService(JsonFileStore(DATA_FILE))

    def app(environ: dict, start_response: StartResponse) -> Iterable[bytes]:
        method = environ.get("REQUEST_METHOD", "GET")
        path = environ.get("PATH_INFO", "/")

        if path.startswith("/api/"):
            return _handle_api(habit_service, environ, start_response, method, path)

        return _serve_static(start_response, path)

    return app


def _handle_api(
    service: HabitService,
    environ: dict,
    start_response: StartResponse,
    method: str,
    path: str,
) -> Iterable[bytes]:
    try:
        if method == "GET" and path == "/api/health":
            return _json_response(start_response, 200, {"status": "ok"})

        if method == "GET" and path == "/api/dashboard":
            params = parse_qs(environ.get("QUERY_STRING", ""))
            reference_date = params.get("date", [None])[0]
            return _json_response(start_response, 200, service.dashboard(reference_date))

        if method == "GET" and path == "/api/habits":
            params = parse_qs(environ.get("QUERY_STRING", ""))
            reference_date = params.get("date", [None])[0]
            return _json_response(start_response, 200, {"habits": service.list_habits(reference_date)})

        if method == "POST" and path == "/api/habits":
            payload = _read_json_body(environ)
            habit = service.create_habit(
                name=str(payload.get("name", "")),
                description=str(payload.get("description", "")),
                frequency=str(payload.get("frequency", "daily")),
            )
            return _json_response(start_response, 201, habit)

        if method == "POST" and path.startswith("/api/habits/") and path.endswith("/complete"):
            habit_id = path.removeprefix("/api/habits/").removesuffix("/complete").strip("/")
            payload = _read_json_body(environ)
            habit = service.complete_habit(habit_id, payload.get("date"))
            return _json_response(start_response, 200, habit)

        return _json_response(start_response, 404, {"error": "Not found"})
    except ValueError as error:
        return _json_response(start_response, 400, {"error": str(error)})
    except KeyError as error:
        return _json_response(start_response, 404, {"error": str(error)})
    except json.JSONDecodeError:
        return _json_response(start_response, 400, {"error": "Body must be valid JSON."})


def _serve_static(start_response: StartResponse, path: str) -> Iterable[bytes]:
    relative_path = "index.html" if path == "/" else path.lstrip("/")
    target = (STATIC_DIR / relative_path).resolve()

    if not str(target).startswith(str(STATIC_DIR.resolve())) or not target.is_file():
        start_response("404 Not Found", [("Content-Type", "text/plain; charset=utf-8")])
        return [b"Not found"]

    content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
    start_response("200 OK", [("Content-Type", f"{content_type}; charset=utf-8")])
    return [target.read_bytes()]


def _read_json_body(environ: dict) -> dict[str, object]:
    content_length = environ.get("CONTENT_LENGTH") or "0"
    try:
        size = int(content_length)
    except ValueError:
        size = 0

    stream = environ.get("wsgi.input") or io.BytesIO()
    raw_body = stream.read(size) if size > 0 else b""
    if not raw_body:
        return {}
    return json.loads(raw_body.decode("utf-8"))


def _json_response(start_response: StartResponse, status_code: int, payload: dict[str, object]) -> Iterable[bytes]:
    body = json.dumps(payload).encode("utf-8")
    start_response(
        f"{status_code} {_status_text(status_code)}",
        [
            ("Content-Type", "application/json; charset=utf-8"),
            ("Content-Length", str(len(body))),
        ],
    )
    return [body]


def _status_text(status_code: int) -> str:
    return {
        200: "OK",
        201: "Created",
        400: "Bad Request",
        404: "Not Found",
    }.get(status_code, "OK")


def main() -> None:
    host = os.environ.get("HABITFLOW_HOST", "127.0.0.1")
    port = int(os.environ.get("HABITFLOW_PORT", "8000"))

    with make_server(host, port, create_app()) as server:
        print(f"HabitFlow running at http://{host}:{port}")
        server.serve_forever()


if __name__ == "__main__":
    main()
