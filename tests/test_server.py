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
from app.service import AppointmentService


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
        store = JsonFileStore(self.temp_dir / "appointments.json")
        self.app = create_app(AppointmentService(store))

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_health_endpoint(self) -> None:
        status, _, body = call_app(self.app, "GET", "/api/health")
        self.assertEqual(status, "200 OK")
        self.assertEqual(body["status"], "ok")

    def test_create_follow_up_reschedule_and_read_dashboard(self) -> None:
        _, _, created = call_app(
            self.app,
            "POST",
            "/api/appointments",
            {
                "customer_name": "Avery Shaw",
                "phone_number": "555-0136",
                "appointment_type": "Consultation",
                "scheduled_at": "2026-03-25T09:00",
                "preferred_channel": "text",
                "notes": "First-time visit",
            },
        )
        follow_up_status, _, follow_up = call_app(
            self.app,
            "POST",
            f"/api/appointments/{created['id']}/follow-up",
            {"channel": "text", "reference_time": "2026-03-25T09:35"},
        )
        reschedule_status, _, rescheduled = call_app(
            self.app,
            "POST",
            f"/api/appointments/{created['id']}/reschedule",
            {"new_scheduled_at": "2026-03-25T11:00", "reference_time": "2026-03-25T09:40"},
        )
        dashboard_status, _, dashboard = call_app(self.app, "GET", "/api/dashboard?time=2026-03-25T09:45")

        self.assertEqual(follow_up_status, "200 OK")
        self.assertEqual(follow_up["status"], "follow_up_sent")
        self.assertEqual(reschedule_status, "200 OK")
        self.assertEqual(rescheduled["status"], "rescheduled")
        self.assertEqual(dashboard_status, "200 OK")
        self.assertEqual(dashboard["follow_ups_sent"], 1)
        self.assertEqual(dashboard["rescheduled_appointments"], 1)

    def test_follow_up_before_threshold_returns_bad_request(self) -> None:
        _, _, created = call_app(
            self.app,
            "POST",
            "/api/appointments",
            {
                "customer_name": "Jamie Cole",
                "phone_number": "555-0181",
                "appointment_type": "Checkup",
                "scheduled_at": "2026-03-25T09:00",
                "preferred_channel": "call",
            },
        )

        status, _, body = call_app(
            self.app,
            "POST",
            f"/api/appointments/{created['id']}/follow-up",
            {"channel": "call", "reference_time": "2026-03-25T09:10"},
        )

        self.assertEqual(status, "400 Bad Request")
        self.assertIn("30 minutes late", body["error"])

    def test_invalid_appointment_payload_returns_bad_request(self) -> None:
        status, _, body = call_app(
            self.app,
            "POST",
            "/api/appointments",
            {"customer_name": "", "phone_number": "555-0100", "appointment_type": "Checkup", "scheduled_at": "2026-03-25T09:00"},
        )

        self.assertEqual(status, "400 Bad Request")
        self.assertIn("error", body)


if __name__ == "__main__":
    unittest.main()
