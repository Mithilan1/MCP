from __future__ import annotations

import shutil
import unittest
from pathlib import Path
from uuid import uuid4

from app.data_store import JsonFileStore
from app.service import HabitService


class HabitServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(__file__).resolve().parent / ".tmp" / uuid4().hex
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.store = JsonFileStore(self.temp_dir / "habits.json")
        self.service = HabitService(self.store)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_habit_persists_record(self) -> None:
        habit = self.service.create_habit("Read", "Read 20 minutes", "daily")

        self.assertEqual(habit["name"], "Read")
        self.assertEqual(len(self.service.list_habits()), 1)

    def test_create_habit_rejects_blank_name(self) -> None:
        with self.assertRaises(ValueError):
            self.service.create_habit("   ")

    def test_complete_habit_is_idempotent_for_same_day(self) -> None:
        habit = self.service.create_habit("Walk")

        updated = self.service.complete_habit(habit["id"], "2026-03-25")
        updated_again = self.service.complete_habit(habit["id"], "2026-03-25")

        self.assertTrue(updated["is_complete_now"])
        self.assertEqual(updated_again["completions"], ["2026-03-25"])

    def test_daily_streak_counts_consecutive_days(self) -> None:
        habit = self.service.create_habit("Journal")
        self.service.complete_habit(habit["id"], "2026-03-23")
        self.service.complete_habit(habit["id"], "2026-03-24")
        updated = self.service.complete_habit(habit["id"], "2026-03-25")

        self.assertEqual(updated["current_streak"], 3)

    def test_weekly_streak_counts_consecutive_weeks(self) -> None:
        habit = self.service.create_habit("Meal prep", frequency="weekly")
        self.service.complete_habit(habit["id"], "2026-03-11")
        self.service.complete_habit(habit["id"], "2026-03-18")
        updated = self.service.complete_habit(habit["id"], "2026-03-25")

        self.assertEqual(updated["current_streak"], 3)


if __name__ == "__main__":
    unittest.main()
