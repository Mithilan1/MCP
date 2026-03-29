from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from uuid import uuid4

from .data_store import JsonFileStore
from .models import Habit

VALID_FREQUENCIES = {"daily", "weekly"}


class HabitService:
    def __init__(self, store: JsonFileStore) -> None:
        self.store = store

    def list_habits(self, reference_date: str | None = None) -> list[dict[str, object]]:
        target_date = self._parse_date(reference_date) if reference_date else date.today()
        return [self._habit_view(habit, target_date) for habit in self.store.load()]

    def create_habit(
        self,
        name: str,
        description: str = "",
        frequency: str = "daily",
    ) -> dict[str, object]:
        clean_name = name.strip()
        clean_description = description.strip()
        clean_frequency = frequency.strip().lower()

        if not clean_name:
            raise ValueError("Habit name is required.")
        if clean_frequency not in VALID_FREQUENCIES:
            raise ValueError("Frequency must be daily or weekly.")

        habits = self.store.load()
        habit = Habit(
            id=uuid4().hex[:8],
            name=clean_name,
            description=clean_description,
            frequency=clean_frequency,
            created_at=datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            completions=[],
        )
        habits.append(habit)
        self.store.save(habits)
        return self._habit_view(habit, date.today())

    def complete_habit(self, habit_id: str, on_date: str | None = None) -> dict[str, object]:
        target_date = self._parse_date(on_date) if on_date else date.today()
        habits = self.store.load()

        for habit in habits:
            if habit.id != habit_id:
                continue

            completion_key = target_date.isoformat()
            if completion_key not in habit.completions:
                habit.completions.append(completion_key)
            self.store.save(habits)
            return self._habit_view(habit, target_date)

        raise KeyError(f"Unknown habit: {habit_id}")

    def dashboard(self, reference_date: str | None = None) -> dict[str, object]:
        target_date = self._parse_date(reference_date) if reference_date else date.today()
        habits = [self._habit_view(habit, target_date) for habit in self.store.load()]

        return {
            "reference_date": target_date.isoformat(),
            "total_habits": len(habits),
            "completed_for_current_period": sum(1 for item in habits if item["is_complete_now"]),
            "best_streak": max((int(item["current_streak"]) for item in habits), default=0),
            "habits": habits,
        }

    def _habit_view(self, habit: Habit, reference_date: date) -> dict[str, object]:
        return {
            **habit.to_dict(),
            "current_streak": self._current_streak(habit, reference_date),
            "is_complete_now": self._is_complete_for_reference(habit, reference_date),
            "current_period_label": self._current_period_label(habit.frequency, reference_date),
        }

    def _current_streak(self, habit: Habit, reference_date: date) -> int:
        completion_dates = sorted(self._parse_date(value) for value in set(habit.completions))
        if not completion_dates:
            return 0

        if habit.frequency == "daily":
            completion_set = {value.isoformat() for value in completion_dates}
            cursor = reference_date
            streak = 0

            while cursor.isoformat() in completion_set:
                streak += 1
                cursor -= timedelta(days=1)

            return streak

        completed_weeks = {self._week_key(item) for item in completion_dates}
        cursor = reference_date
        streak = 0

        while self._week_key(cursor) in completed_weeks:
            streak += 1
            cursor -= timedelta(days=7)

        return streak

    def _is_complete_for_reference(self, habit: Habit, reference_date: date) -> bool:
        completion_dates = [self._parse_date(value) for value in set(habit.completions)]
        if habit.frequency == "daily":
            return reference_date in completion_dates

        reference_key = self._week_key(reference_date)
        return any(self._week_key(item) == reference_key for item in completion_dates)

    @staticmethod
    def _current_period_label(frequency: str, reference_date: date) -> str:
        if frequency == "weekly":
            iso_year, iso_week, _ = reference_date.isocalendar()
            return f"Week {iso_week}, {iso_year}"
        return reference_date.isoformat()

    @staticmethod
    def _parse_date(value: str) -> date:
        return date.fromisoformat(value)

    @staticmethod
    def _week_key(value: date) -> tuple[int, int]:
        iso_year, iso_week, _ = value.isocalendar()
        return iso_year, iso_week
