from __future__ import annotations

import io
import json
import shutil
import unittest
from pathlib import Path
from uuid import uuid4
from wsgiref.util import setup_testing_defaults

from app.data_store import JsonFileStore
from app.server import create_app
from app.service import HabitService


def call_app(app, method: str, path: str, payload: dict[str, object] | None = None) -> tuple[str, dict[str, str], dict[str, object]]:
    raw_body = json.dumps(payload).encode("utf-8") if payload is not None else b""
    route, _, query_string = path.partition("?")
    environ: dict[str, object] = {}
    setup_testing_defaults(environ)
    environ["REQUEST_METHOD"] = method
    environ["PATH_INFO"] = route
    environ["QUERY_STRING"] = query_string
    environ["CONTENT_LENGTH"] = str(len(raw_body))
    environ["wsgi.input"] = io.BytesIO(raw_body)

    status = ""
    headers: list[tuple[str, str]] = []

    def start_response(inner_status: str, inner_headers: list[tuple[str, str]]) -> None:
        nonlocal status, headers
        status = inner_status
        headers = inner_headers

    response = b"".join(app(environ, start_response))
    parsed_headers = {key: value for key, value in headers}
    body = json.loads(response.decode("utf-8")) if response else {}
    return status, parsed_headers, body


class ServerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(__file__).resolve().parent / ".tmp" / uuid4().hex
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        store = JsonFileStore(self.temp_dir / "habits.json")
        self.app = create_app(HabitService(store))

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_health_endpoint(self) -> None:
        status, _, body = call_app(self.app, "GET", "/api/health")
        self.assertEqual(status, "200 OK")
        self.assertEqual(body["status"], "ok")

    def test_create_complete_and_read_dashboard(self) -> None:
        _, _, created = call_app(
            self.app,
            "POST",
            "/api/habits",
            {"name": "Stretch", "description": "Five minutes", "frequency": "daily"},
        )
        status, _, completed = call_app(
            self.app,
            "POST",
            f"/api/habits/{created['id']}/complete",
            {"date": "2026-03-25"},
        )
        dashboard_status, _, dashboard = call_app(self.app, "GET", "/api/dashboard?date=2026-03-25")

        self.assertEqual(status, "200 OK")
        self.assertTrue(completed["is_complete_now"])
        self.assertEqual(dashboard_status, "200 OK")
        self.assertEqual(dashboard["completed_for_current_period"], 1)

    def test_invalid_habit_payload_returns_bad_request(self) -> None:
        status, _, body = call_app(self.app, "POST", "/api/habits", {"name": ""})

        self.assertEqual(status, "400 Bad Request")
        self.assertIn("error", body)


if __name__ == "__main__":
    unittest.main()
