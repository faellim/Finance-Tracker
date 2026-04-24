from __future__ import annotations

import sqlite3
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from finance_tracker.database import initialize_database
from finance_tracker.repository import CategoryRepository, ExpenseRepository, UserRepository
from finance_tracker.services import AuthService, FinanceTrackerService


class FinanceTrackerServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        connection = sqlite3.connect(":memory:")
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON;")
        initialize_database(connection)
        self.auth_service = AuthService(UserRepository(connection))
        self.service = FinanceTrackerService(
            category_repository=CategoryRepository(connection),
            expense_repository=ExpenseRepository(connection),
        )
        self.user = self.auth_service.register_user(
            "Test User",
            "test@example.com",
            "secret123",
        )

    def test_create_category_and_register_expense(self) -> None:
        self.service.create_category("Food", "Daily meals")
        expense = self.service.register_expense(
            user_id=self.user.id,
            category_name="Food",
            title="Lunch",
            amount_text="32.50",
            expense_date_text="2026-04-18",
            notes="Workday lunch",
        )

        self.assertEqual(expense.title, "Lunch")
        self.assertEqual(str(expense.amount), "32.50")

        summary, by_category = self.service.get_monthly_summary("2026-04", user_id=self.user.id)
        self.assertEqual(str(summary.total_expenses), "32.50")
        self.assertEqual(summary.number_of_expenses, 1)
        self.assertEqual(by_category[0].category_name, "Food")

    def test_duplicate_category_is_rejected(self) -> None:
        self.service.create_category("Transport")

        with self.assertRaisesRegex(ValueError, "already exists"):
            self.service.create_category("Transport")

    def test_invalid_amount_is_rejected(self) -> None:
        self.service.create_category("Health")

        with self.assertRaisesRegex(ValueError, "valid number"):
            self.service.register_expense(
                user_id=self.user.id,
                category_name="Health",
                title="Medicine",
                amount_text="abc",
                expense_date_text="2026-04-11",
            )

    def test_authenticate_registered_user(self) -> None:
        user = self.auth_service.authenticate("test@example.com", "secret123")
        self.assertEqual(user.email, "test@example.com")


if __name__ == "__main__":
    unittest.main()
