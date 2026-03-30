from __future__ import annotations

import json
from pathlib import Path

from .models import Appointment


class JsonFileStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def load(self) -> list[Appointment]:
        if not self.path.exists():
            return []

        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return [Appointment.from_dict(item) for item in payload]

    def save(self, appointments: list[Appointment]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [appointment.to_dict() for appointment in appointments]
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
