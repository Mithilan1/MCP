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
from .service import AppointmentService

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"
DATA_FILE = BASE_DIR / "data" / "appointments.json"

StartResponse = Callable[[str, list[tuple[str, str]]], None]


def create_app(service: AppointmentService | None = None) -> Callable[[dict, StartResponse], Iterable[bytes]]:
    appointment_service = service or AppointmentService(JsonFileStore(DATA_FILE))

    def app(environ: dict, start_response: StartResponse) -> Iterable[bytes]:
        method = environ.get("REQUEST_METHOD", "GET")
        path = environ.get("PATH_INFO", "/")

        if path.startswith("/api/"):
            return _handle_api(appointment_service, environ, start_response, method, path)

        return _serve_static(start_response, path)

    return app


def _handle_api(
    service: AppointmentService,
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
            reference_time = params.get("time", [None])[0]
            return _json_response(start_response, 200, service.dashboard(reference_time))

        if method == "GET" and path == "/api/appointments":
            params = parse_qs(environ.get("QUERY_STRING", ""))
            reference_time = params.get("time", [None])[0]
            return _json_response(start_response, 200, {"appointments": service.list_appointments(reference_time)})

        if method == "POST" and path == "/api/appointments":
            payload = _read_json_body(environ)
            appointment = service.create_appointment(
                customer_name=str(payload.get("customer_name", "")),
                phone_number=str(payload.get("phone_number", "")),
                appointment_type=str(payload.get("appointment_type", "")),
                scheduled_at=str(payload.get("scheduled_at", "")),
                preferred_channel=str(payload.get("preferred_channel", "text")),
                notes=str(payload.get("notes", "")),
            )
            return _json_response(start_response, 201, appointment)

        if method == "POST" and path.startswith("/api/appointments/") and path.endswith("/follow-up"):
            appointment_id = path.removeprefix("/api/appointments/").removesuffix("/follow-up").strip("/")
            payload = _read_json_body(environ)
            appointment = service.send_follow_up(
                appointment_id,
                channel=str(payload.get("channel", "")),
                reference_time=str(payload.get("reference_time", "")) or None,
            )
            return _json_response(start_response, 200, appointment)

        if method == "POST" and path.startswith("/api/appointments/") and path.endswith("/reschedule"):
            appointment_id = path.removeprefix("/api/appointments/").removesuffix("/reschedule").strip("/")
            payload = _read_json_body(environ)
            appointment = service.reschedule_appointment(
                appointment_id,
                new_scheduled_at=str(payload.get("new_scheduled_at", "")),
                reference_time=str(payload.get("reference_time", "")) or None,
            )
            return _json_response(start_response, 200, appointment)

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
    host = os.environ.get("RECALLFLOW_HOST", "127.0.0.1")
    port = int(os.environ.get("RECALLFLOW_PORT", "8000"))

    with make_server(host, port, create_app()) as server:
        print(f"RecallFlow running at http://{host}:{port}")
        server.serve_forever()


if __name__ == "__main__":
    main()
