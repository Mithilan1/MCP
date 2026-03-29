from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Habit:
    id: str
    name: str
    description: str
    frequency: str
    created_at: str
    completions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "frequency": self.frequency,
            "created_at": self.created_at,
            "completions": sorted(set(self.completions)),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "Habit":
        return cls(
            id=str(payload["id"]),
            name=str(payload["name"]),
            description=str(payload.get("description", "")),
            frequency=str(payload.get("frequency", "daily")),
            created_at=str(payload["created_at"]),
            completions=[str(item) for item in payload.get("completions", [])],
        )
