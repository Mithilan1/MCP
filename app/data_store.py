from __future__ import annotations

import json
from pathlib import Path

from .models import Habit


class JsonFileStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def load(self) -> list[Habit]:
        if not self.path.exists():
            return []

        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return [Habit.from_dict(item) for item in payload]

    def save(self, habits: list[Habit]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [habit.to_dict() for habit in habits]
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
