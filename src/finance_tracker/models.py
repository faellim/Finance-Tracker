from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(slots=True)
class User:
    id: int | None
    full_name: str
    email: str
    password_hash: str


@dataclass(slots=True)
class Category:
    id: int | None
    name: str
    description: str | None = None


@dataclass(slots=True)
class Expense:
    id: int | None
    user_id: int | None
    category_id: int
    title: str
    amount: Decimal
    expense_date: date
    notes: str | None = None
    category_name: str | None = None


@dataclass(slots=True)
class MonthlySummary:
    month: str
    total_expenses: Decimal
    number_of_expenses: int


@dataclass(slots=True)
class CategorySummary:
    category_name: str
    total_amount: Decimal
    expense_count: int
