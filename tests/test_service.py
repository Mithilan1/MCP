from __future__ import annotations

import shutil
import unittest
from pathlib import Path
from uuid import uuid4

from app.data_store import JsonFileStore
from app.service import AppointmentService


class AppointmentServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(__file__).resolve().parent / ".tmp" / uuid4().hex
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.store = JsonFileStore(self.temp_dir / "appointments.json")
        self.service = AppointmentService(self.store)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_appointment_persists_record(self) -> None:
        appointment = self.service.create_appointment(
            customer_name="Jordan Lee",
            phone_number="555-0147",
            appointment_type="Dental cleaning",
            scheduled_at="2026-03-25T09:00",
            preferred_channel="text",
        )

        self.assertEqual(appointment["customer_name"], "Jordan Lee")
        self.assertEqual(len(self.service.list_appointments("2026-03-25T08:45")), 1)

    def test_create_appointment_rejects_blank_customer_name(self) -> None:
        with self.assertRaises(ValueError):
            self.service.create_appointment(
                customer_name="   ",
                phone_number="555-0147",
                appointment_type="Dental cleaning",
                scheduled_at="2026-03-25T09:00",
            )

    def test_follow_up_requires_thirty_minutes_of_lateness(self) -> None:
        appointment = self.service.create_appointment(
            customer_name="Chris Park",
            phone_number="555-0182",
            appointment_type="Massage therapy",
            scheduled_at="2026-03-25T09:00",
        )

        with self.assertRaises(ValueError):
            self.service.send_follow_up(appointment["id"], "text", "2026-03-25T09:20")

    def test_follow_up_records_selected_channel(self) -> None:
        appointment = self.service.create_appointment(
            customer_name="Taylor Nguyen",
            phone_number="555-0170",
            appointment_type="Eye exam",
            scheduled_at="2026-03-25T09:00",
            preferred_channel="text",
        )

        updated = self.service.send_follow_up(appointment["id"], "call", "2026-03-25T09:35")

        self.assertEqual(updated["status"], "follow_up_sent")
        self.assertEqual(updated["last_follow_up_channel"], "call")
        self.assertEqual(updated["follow_up_count"], 1)

    def test_reschedule_updates_slot_after_follow_up(self) -> None:
        appointment = self.service.create_appointment(
            customer_name="Morgan Ellis",
            phone_number="555-0119",
            appointment_type="Therapy session",
            scheduled_at="2026-03-25T09:00",
        )
        self.service.send_follow_up(appointment["id"], "text", "2026-03-25T09:35")

        updated = self.service.reschedule_appointment(
            appointment["id"],
            new_scheduled_at="2026-03-25T11:00",
            reference_time="2026-03-25T09:40",
        )

        self.assertEqual(updated["status"], "rescheduled")
        self.assertEqual(updated["scheduled_at"], "2026-03-25T11:00")
        self.assertEqual(updated["reschedule_count"], 1)
        self.assertIn("new appointment", updated["latest_activity"])


if __name__ == "__main__":
    unittest.main()
