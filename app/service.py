from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from .data_store import JsonFileStore
from .models import Appointment

VALID_CHANNELS = {"call", "text"}
LATE_THRESHOLD_MINUTES = 30


class AppointmentService:
    def __init__(self, store: JsonFileStore) -> None:
        self.store = store

    def list_appointments(self, reference_time: str | None = None) -> list[dict[str, object]]:
        target_time = self._parse_datetime(reference_time) if reference_time else self._now()
        return [self._appointment_view(appointment, target_time) for appointment in self.store.load()]

    def create_appointment(
        self,
        customer_name: str,
        phone_number: str,
        appointment_type: str,
        scheduled_at: str,
        preferred_channel: str = "text",
        notes: str = "",
    ) -> dict[str, object]:
        clean_customer_name = customer_name.strip()
        clean_phone_number = phone_number.strip()
        clean_appointment_type = appointment_type.strip()
        clean_preferred_channel = preferred_channel.strip().lower()
        clean_notes = notes.strip()

        if not clean_customer_name:
            raise ValueError("Customer name is required.")
        if not clean_phone_number:
            raise ValueError("Phone number is required.")
        if not clean_appointment_type:
            raise ValueError("Appointment type is required.")
        if clean_preferred_channel not in VALID_CHANNELS:
            raise ValueError("Preferred channel must be call or text.")

        scheduled_time = self._parse_datetime(scheduled_at)
        appointments = self.store.load()
        appointment = Appointment(
            id=uuid4().hex[:8],
            customer_name=clean_customer_name,
            phone_number=clean_phone_number,
            appointment_type=clean_appointment_type,
            scheduled_at=scheduled_time.isoformat(timespec="minutes"),
            preferred_channel=clean_preferred_channel,
            created_at=self._timestamp_label(self._now()),
            notes=clean_notes,
            status="scheduled",
            activity_log=[],
        )
        appointments.append(appointment)
        self.store.save(appointments)
        return self._appointment_view(appointment, self._now())

    def send_follow_up(
        self,
        appointment_id: str,
        channel: str | None = None,
        reference_time: str | None = None,
    ) -> dict[str, object]:
        target_time = self._parse_datetime(reference_time) if reference_time else self._now()
        appointments = self.store.load()

        for appointment in appointments:
            if appointment.id != appointment_id:
                continue

            chosen_channel = (channel or appointment.preferred_channel).strip().lower()
            if chosen_channel not in VALID_CHANNELS:
                raise ValueError("Follow-up channel must be call or text.")
            if not self._is_late(appointment, target_time):
                raise ValueError("Appointment is not 30 minutes late yet.")
            if appointment.status == "follow_up_sent":
                raise ValueError("Follow-up already sent for this appointment.")

            appointment.status = "follow_up_sent"
            appointment.activity_log.append(
                {
                    "type": "follow_up",
                    "timestamp": self._timestamp_label(target_time),
                    "channel": chosen_channel,
                    "summary": f"MCP sent a {chosen_channel} follow-up with a reschedule option.",
                }
            )
            self.store.save(appointments)
            return self._appointment_view(appointment, target_time)

        raise KeyError(f"Unknown appointment: {appointment_id}")

    def reschedule_appointment(
        self,
        appointment_id: str,
        new_scheduled_at: str,
        reference_time: str | None = None,
    ) -> dict[str, object]:
        target_time = self._parse_datetime(reference_time) if reference_time else self._now()
        updated_time = self._parse_datetime(new_scheduled_at)
        appointments = self.store.load()

        for appointment in appointments:
            if appointment.id != appointment_id:
                continue

            if appointment.status != "follow_up_sent":
                raise ValueError("Send follow-up before rescheduling this appointment.")
            if updated_time <= target_time:
                raise ValueError("Rescheduled appointment must be after the current reference time.")

            previous_slot = appointment.scheduled_at
            appointment.scheduled_at = updated_time.isoformat(timespec="minutes")
            appointment.status = "rescheduled"
            appointment.activity_log.append(
                {
                    "type": "reschedule",
                    "timestamp": self._timestamp_label(target_time),
                    "from": previous_slot,
                    "to": appointment.scheduled_at,
                    "summary": f"Customer accepted a new appointment for {self._format_datetime(updated_time)}.",
                }
            )
            self.store.save(appointments)
            return self._appointment_view(appointment, target_time)

        raise KeyError(f"Unknown appointment: {appointment_id}")

    def dashboard(self, reference_time: str | None = None) -> dict[str, object]:
        target_time = self._parse_datetime(reference_time) if reference_time else self._now()
        appointments = [self._appointment_view(appointment, target_time) for appointment in self.store.load()]

        return {
            "reference_time": target_time.isoformat(timespec="minutes"),
            "reference_time_label": self._format_datetime(target_time),
            "total_appointments": len(appointments),
            "late_appointments": sum(1 for item in appointments if item["is_late"]),
            "follow_ups_sent": sum(1 for item in appointments if int(item["follow_up_count"]) > 0),
            "rescheduled_appointments": sum(1 for item in appointments if int(item["reschedule_count"]) > 0),
            "appointments": appointments,
        }

    def _appointment_view(self, appointment: Appointment, reference_time: datetime) -> dict[str, object]:
        latest_activity = appointment.activity_log[-1] if appointment.activity_log else None
        follow_up_events = [item for item in appointment.activity_log if item.get("type") == "follow_up"]
        reschedule_events = [item for item in appointment.activity_log if item.get("type") == "reschedule"]
        scheduled_time = self._parse_datetime(appointment.scheduled_at)

        return {
            **appointment.to_dict(),
            "scheduled_for_label": self._format_datetime(scheduled_time),
            "minutes_late": self._minutes_late(appointment, reference_time),
            "timing_status": self._timing_status(appointment, reference_time),
            "is_late": self._is_late(appointment, reference_time),
            "needs_follow_up": self._needs_follow_up(appointment, reference_time),
            "can_reschedule": appointment.status == "follow_up_sent",
            "status_label": self._status_label(appointment.status),
            "follow_up_count": len(follow_up_events),
            "reschedule_count": len(reschedule_events),
            "latest_activity": latest_activity["summary"] if latest_activity else "No outreach yet.",
            "last_follow_up_channel": follow_up_events[-1]["channel"] if follow_up_events else None,
        }

    def _needs_follow_up(self, appointment: Appointment, reference_time: datetime) -> bool:
        return self._is_late(appointment, reference_time) and appointment.status != "follow_up_sent"

    def _is_late(self, appointment: Appointment, reference_time: datetime) -> bool:
        scheduled_time = self._parse_datetime(appointment.scheduled_at)
        return reference_time >= scheduled_time + timedelta(minutes=LATE_THRESHOLD_MINUTES)

    def _minutes_late(self, appointment: Appointment, reference_time: datetime) -> int:
        scheduled_time = self._parse_datetime(appointment.scheduled_at)
        late_delta = reference_time - scheduled_time
        if late_delta.total_seconds() <= 0:
            return 0
        return int(late_delta.total_seconds() // 60)

    @staticmethod
    def _timing_status(appointment: Appointment, reference_time: datetime) -> str:
        scheduled_time = datetime.fromisoformat(appointment.scheduled_at)
        delta_minutes = int((reference_time - scheduled_time).total_seconds() // 60)

        if delta_minutes < 0:
            return f"Starts in {abs(delta_minutes)} minutes"
        if delta_minutes < LATE_THRESHOLD_MINUTES:
            return f"{delta_minutes} minutes into the grace period"
        return f"{delta_minutes} minutes late"

    @staticmethod
    def _status_label(status: str) -> str:
        return {
            "scheduled": "Scheduled",
            "follow_up_sent": "Follow-up sent",
            "rescheduled": "Rescheduled",
        }.get(status, status.replace("_", " ").title())

    @staticmethod
    def _parse_datetime(value: str) -> datetime:
        return datetime.fromisoformat(str(value))

    @staticmethod
    def _format_datetime(value: datetime) -> str:
        return value.strftime("%b %d, %Y at %I:%M %p")

    @staticmethod
    def _timestamp_label(value: datetime) -> str:
        return value.isoformat(timespec="minutes")

    @staticmethod
    def _now() -> datetime:
        return datetime.now(UTC).astimezone().replace(second=0, microsecond=0, tzinfo=None)
