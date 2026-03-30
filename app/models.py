from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Appointment:
    id: str
    customer_name: str
    phone_number: str
    appointment_type: str
    scheduled_at: str
    preferred_channel: str
    created_at: str
    notes: str = ""
    status: str = "scheduled"
    activity_log: list[dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "phone_number": self.phone_number,
            "appointment_type": self.appointment_type,
            "scheduled_at": self.scheduled_at,
            "preferred_channel": self.preferred_channel,
            "created_at": self.created_at,
            "notes": self.notes,
            "status": self.status,
            "activity_log": list(self.activity_log),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "Appointment":
        return cls(
            id=str(payload["id"]),
            customer_name=str(payload["customer_name"]),
            phone_number=str(payload["phone_number"]),
            appointment_type=str(payload["appointment_type"]),
            scheduled_at=str(payload["scheduled_at"]),
            preferred_channel=str(payload.get("preferred_channel", "text")),
            created_at=str(payload["created_at"]),
            notes=str(payload.get("notes", "")),
            status=str(payload.get("status", "scheduled")),
            activity_log=[
                {str(key): str(value) for key, value in item.items()}
                for item in payload.get("activity_log", [])
                if isinstance(item, dict)
            ],
        )
