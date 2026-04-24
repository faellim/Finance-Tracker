from __future__ import annotations

import sqlite3
from datetime import date
from decimal import Decimal

from finance_tracker.money import cents_to_decimal, decimal_to_cents
from finance_tracker.models import Category, CategorySummary, Expense, MonthlySummary, User


class UserRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def create(self, full_name: str, email: str, password_hash: str) -> User:
        cursor = self.connection.execute(
            """
            INSERT INTO users (full_name, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (full_name.strip(), email.strip().lower(), password_hash),
        )
        self.connection.commit()
        return User(
            id=cursor.lastrowid,
            full_name=full_name.strip(),
            email=email.strip().lower(),
            password_hash=password_hash,
        )

    def get_by_email(self, email: str) -> User | None:
        row = self.connection.execute(
            """
            SELECT id, full_name, email, password_hash
            FROM users
            WHERE lower(email) = lower(?)
            """,
            (email.strip(),),
        ).fetchone()
        if row is None:
            return None
        return User(
            id=row["id"],
            full_name=row["full_name"],
            email=row["email"],
            password_hash=row["password_hash"],
        )


class CategoryRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def create(self, name: str, description: str | None = None) -> Category:
        cursor = self.connection.execute(
            """
            INSERT INTO categories (name, description)
            VALUES (?, ?)
            """,
            (name.strip(), description),
        )
        self.connection.commit()
        return Category(id=cursor.lastrowid, name=name.strip(), description=description)

    def get_by_name(self, name: str) -> Category | None:
        row = self.connection.execute(
            "SELECT id, name, description FROM categories WHERE lower(name) = lower(?)",
            (name.strip(),),
        ).fetchone()
        if row is None:
            return None
        return Category(id=row["id"], name=row["name"], description=row["description"])

    def list_all(self) -> list[Category]:
        rows = self.connection.execute(
            "SELECT id, name, description FROM categories ORDER BY name"
        ).fetchall()
        return [
            Category(id=row["id"], name=row["name"], description=row["description"])
            for row in rows
        ]


class ExpenseRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def create(
        self,
        user_id: int | None,
        category_id: int,
        title: str,
        amount: Decimal,
        expense_date: date,
        notes: str | None = None,
    ) -> Expense:
        cursor = self.connection.execute(
            """
            INSERT INTO expenses (user_id, category_id, title, amount_cents, expense_date, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                category_id,
                title.strip(),
                decimal_to_cents(amount),
                expense_date.isoformat(),
                notes,
            ),
        )
        self.connection.commit()
        return Expense(
            id=cursor.lastrowid,
            user_id=user_id,
            category_id=category_id,
            title=title.strip(),
            amount=amount,
            expense_date=expense_date,
            notes=notes,
        )

    def list_all(self, user_id: int | None = None) -> list[Expense]:
        if user_id is None:
            rows = self.connection.execute(
                """
                SELECT
                    e.id,
                    e.user_id,
                    e.category_id,
                    e.title,
                    e.amount_cents,
                    e.expense_date,
                    e.notes,
                    c.name AS category_name
                FROM expenses e
                INNER JOIN categories c ON c.id = e.category_id
                ORDER BY e.expense_date DESC, e.id DESC
                """
            ).fetchall()
            return [self._row_to_expense(row) for row in rows]

        rows = self.connection.execute(
            """
            SELECT
                e.id,
                e.user_id,
                e.category_id,
                e.title,
                e.amount_cents,
                e.expense_date,
                e.notes,
                c.name AS category_name
            FROM expenses e
            INNER JOIN categories c ON c.id = e.category_id
            WHERE e.user_id = ?
            ORDER BY e.expense_date DESC, e.id DESC
            """,
            (user_id,),
        ).fetchall()
        return [self._row_to_expense(row) for row in rows]

    def list_by_month(self, month: str, user_id: int | None = None) -> list[Expense]:
        if user_id is None:
            rows = self.connection.execute(
                """
                SELECT
                    e.id,
                    e.user_id,
                    e.category_id,
                    e.title,
                    e.amount_cents,
                    e.expense_date,
                    e.notes,
                    c.name AS category_name
                FROM expenses e
                INNER JOIN categories c ON c.id = e.category_id
                WHERE substr(e.expense_date, 1, 7) = ?
                ORDER BY e.expense_date DESC, e.id DESC
                """,
                (month,),
            ).fetchall()
            return [self._row_to_expense(row) for row in rows]

        rows = self.connection.execute(
            """
            SELECT
                e.id,
                e.user_id,
                e.category_id,
                e.title,
                e.amount_cents,
                e.expense_date,
                e.notes,
                c.name AS category_name
            FROM expenses e
            INNER JOIN categories c ON c.id = e.category_id
            WHERE substr(e.expense_date, 1, 7) = ?
              AND e.user_id = ?
            ORDER BY e.expense_date DESC, e.id DESC
            """,
            (month, user_id),
        ).fetchall()
        return [self._row_to_expense(row) for row in rows]

    def monthly_summary(self, month: str, user_id: int | None = None) -> MonthlySummary:
        if user_id is None:
            row = self.connection.execute(
                """
                SELECT
                    COALESCE(SUM(amount_cents), 0) AS total_expenses_cents,
                    COUNT(*) AS number_of_expenses
                FROM expenses
                WHERE substr(expense_date, 1, 7) = ?
                """,
                (month,),
            ).fetchone()
            return MonthlySummary(
                month=month,
                total_expenses=cents_to_decimal(row["total_expenses_cents"]),
                number_of_expenses=row["number_of_expenses"],
            )

        row = self.connection.execute(
            """
            SELECT
                COALESCE(SUM(amount_cents), 0) AS total_expenses_cents,
                COUNT(*) AS number_of_expenses
            FROM expenses
            WHERE substr(expense_date, 1, 7) = ?
              AND user_id = ?
            """,
            (month, user_id),
        ).fetchone()
        return MonthlySummary(
            month=month,
            total_expenses=cents_to_decimal(row["total_expenses_cents"]),
            number_of_expenses=row["number_of_expenses"],
        )

    def summary_by_category(self, month: str, user_id: int | None = None) -> list[CategorySummary]:
        if user_id is None:
            rows = self.connection.execute(
                """
                SELECT
                    c.name AS category_name,
                    COALESCE(SUM(e.amount_cents), 0) AS total_amount_cents,
                    COUNT(e.id) AS expense_count
                FROM expenses e
                INNER JOIN categories c ON c.id = e.category_id
                WHERE substr(e.expense_date, 1, 7) = ?
                GROUP BY c.name
                ORDER BY total_amount_cents DESC, c.name
                """,
                (month,),
            ).fetchall()
            return [
                CategorySummary(
                    category_name=row["category_name"],
                    total_amount=cents_to_decimal(row["total_amount_cents"]),
                    expense_count=row["expense_count"],
                )
                for row in rows
            ]

        rows = self.connection.execute(
            """
            SELECT
                c.name AS category_name,
                COALESCE(SUM(e.amount_cents), 0) AS total_amount_cents,
                COUNT(e.id) AS expense_count
            FROM expenses e
            INNER JOIN categories c ON c.id = e.category_id
            WHERE substr(e.expense_date, 1, 7) = ?
              AND e.user_id = ?
            GROUP BY c.name
            ORDER BY total_amount_cents DESC, c.name
            """,
            (month, user_id),
        ).fetchall()
        return [
            CategorySummary(
                category_name=row["category_name"],
                total_amount=cents_to_decimal(row["total_amount_cents"]),
                expense_count=row["expense_count"],
            )
            for row in rows
        ]

    @staticmethod
    def _row_to_expense(row: sqlite3.Row) -> Expense:
        return Expense(
            id=row["id"],
            user_id=row["user_id"],
            category_id=row["category_id"],
            title=row["title"],
            amount=cents_to_decimal(row["amount_cents"]),
            expense_date=date.fromisoformat(row["expense_date"]),
            notes=row["notes"],
            category_name=row["category_name"],
        )
