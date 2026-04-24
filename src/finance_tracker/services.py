from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation

from werkzeug.security import check_password_hash, generate_password_hash

from finance_tracker.models import Category, CategorySummary, Expense, MonthlySummary, User
from finance_tracker.repository import CategoryRepository, ExpenseRepository, UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def register_user(self, full_name: str, email: str, password: str) -> User:
        clean_name = full_name.strip()
        clean_email = email.strip().lower()
        if len(clean_name) < 3:
            raise ValueError("Full name must have at least 3 characters.")
        if "@" not in clean_email or "." not in clean_email:
            raise ValueError("Email must be valid.")
        if len(password) < 6:
            raise ValueError("Password must have at least 6 characters.")
        if self.user_repository.get_by_email(clean_email):
            raise ValueError("This email is already registered.")
        return self.user_repository.create(
            full_name=clean_name,
            email=clean_email,
            password_hash=generate_password_hash(password),
        )

    def authenticate(self, email: str, password: str) -> User:
        user = self.user_repository.get_by_email(email)
        if user is None or not check_password_hash(user.password_hash, password):
            raise ValueError("Invalid email or password.")
        return user


class FinanceTrackerService:
    def __init__(
        self,
        category_repository: CategoryRepository,
        expense_repository: ExpenseRepository,
    ) -> None:
        self.category_repository = category_repository
        self.expense_repository = expense_repository

    def create_category(self, name: str, description: str | None = None) -> Category:
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("Category name cannot be empty.")
        if self.category_repository.get_by_name(clean_name):
            raise ValueError(f"Category '{clean_name}' already exists.")
        return self.category_repository.create(clean_name, description)

    def list_categories(self) -> list[Category]:
        return self.category_repository.list_all()

    def register_expense(
        self,
        user_id: int | None,
        category_name: str,
        title: str,
        amount_text: str,
        expense_date_text: str,
        notes: str | None = None,
    ) -> Expense:
        category = self.category_repository.get_by_name(category_name)
        if category is None or category.id is None:
            raise ValueError(
                f"Category '{category_name}' was not found. Create it before adding expenses."
            )

        clean_title = title.strip()
        if not clean_title:
            raise ValueError("Expense title cannot be empty.")

        amount = self._parse_amount(amount_text)
        expense_date = self._parse_date(expense_date_text)

        return self.expense_repository.create(
            user_id=user_id,
            category_id=category.id,
            title=clean_title,
            amount=amount,
            expense_date=expense_date,
            notes=notes,
        )

    def list_expenses(self, month: str | None = None, user_id: int | None = None) -> list[Expense]:
        if month is None:
            return self.expense_repository.list_all(user_id=user_id)
        self._validate_month(month)
        return self.expense_repository.list_by_month(month, user_id=user_id)

    def get_monthly_summary(
        self,
        month: str,
        user_id: int | None = None,
    ) -> tuple[MonthlySummary, list[CategorySummary]]:
        self._validate_month(month)
        return (
            self.expense_repository.monthly_summary(month, user_id=user_id),
            self.expense_repository.summary_by_category(month, user_id=user_id),
        )

    @staticmethod
    def _parse_amount(amount_text: str) -> Decimal:
        normalized = amount_text.strip().replace(",", ".")
        try:
            amount = Decimal(normalized).quantize(Decimal("0.01"))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("Amount must be a valid number.") from exc
        if amount <= Decimal("0.00"):
            raise ValueError("Amount must be greater than zero.")
        return amount

    @staticmethod
    def _parse_date(value: str) -> date:
        try:
            return date.fromisoformat(value.strip())
        except ValueError as exc:
            raise ValueError("Date must use the YYYY-MM-DD format.") from exc

    @staticmethod
    def _validate_month(month: str) -> None:
        try:
            date.fromisoformat(f"{month}-01")
        except ValueError as exc:
            raise ValueError("Month must use the YYYY-MM format.") from exc
