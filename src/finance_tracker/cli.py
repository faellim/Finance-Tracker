from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from finance_tracker.database import DEFAULT_DB_PATH, get_connection, initialize_database
from finance_tracker.demo import seed_demo_data
from finance_tracker.repository import CategoryRepository, ExpenseRepository
from finance_tracker.services import FinanceTrackerService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="finance-tracker",
        description="Manage expenses, categories and monthly summaries.",
    )
    parser.add_argument(
        "--db",
        default=str(DEFAULT_DB_PATH),
        help="Path to the SQLite database file.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init-db", help="Create the database structure.")

    add_category = subparsers.add_parser("add-category", help="Create a new category.")
    add_category.add_argument("name")
    add_category.add_argument("--description")

    subparsers.add_parser("list-categories", help="List all categories.")

    add_expense = subparsers.add_parser("add-expense", help="Register a new expense.")
    add_expense.add_argument("category")
    add_expense.add_argument("title")
    add_expense.add_argument("amount")
    add_expense.add_argument("date")
    add_expense.add_argument("--notes")

    list_expenses = subparsers.add_parser("list-expenses", help="List expenses.")
    list_expenses.add_argument("--month", help="Filter by month using YYYY-MM.")

    monthly_summary = subparsers.add_parser(
        "monthly-summary",
        help="Show an aggregated summary for a given month.",
    )
    monthly_summary.add_argument("month", help="Month in YYYY-MM format.")

    subparsers.add_parser(
        "seed-demo",
        help="Populate the database with portfolio-friendly demo data.",
    )

    return parser


def get_service(db_path: str) -> FinanceTrackerService:
    connection = get_connection(Path(db_path))
    initialize_database(connection)
    return FinanceTrackerService(
        category_repository=CategoryRepository(connection),
        expense_repository=ExpenseRepository(connection),
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        service = get_service(args.db)

        if args.command == "init-db":
            print(f"Database ready at {args.db}")
            return 0

        if args.command == "add-category":
            category = service.create_category(args.name, args.description)
            print(f"Category created: {category.name}")
            return 0

        if args.command == "list-categories":
            categories = service.list_categories()
            if not categories:
                print("No categories found.")
                return 0
            for category in categories:
                description = f" - {category.description}" if category.description else ""
                print(f"[{category.id}] {category.name}{description}")
            return 0

        if args.command == "add-expense":
            expense = service.register_expense(
                user_id=None,
                category_name=args.category,
                title=args.title,
                amount_text=args.amount,
                expense_date_text=args.date,
                notes=args.notes,
            )
            print(f"Expense added: {expense.title} - ${expense.amount}")
            return 0

        if args.command == "list-expenses":
            expenses = service.list_expenses(args.month)
            if not expenses:
                print("No expenses found.")
                return 0
            for expense in expenses:
                notes = f" | notes: {expense.notes}" if expense.notes else ""
                print(
                    f"[{expense.id}] {expense.expense_date} | {expense.category_name} | "
                    f"{expense.title} | ${expense.amount}{notes}"
                )
            return 0

        if args.command == "monthly-summary":
            summary, category_summaries = service.get_monthly_summary(args.month)
            print(f"Monthly summary for {summary.month}")
            print(f"Total expenses: ${summary.total_expenses}")
            print(f"Number of expenses: {summary.number_of_expenses}")
            if not category_summaries:
                print("No category data for this month.")
                return 0
            print("Breakdown by category:")
            for item in category_summaries:
                print(
                    f"- {item.category_name}: ${item.total_amount} "
                    f"({item.expense_count} expense(s))"
                )
            return 0

        if args.command == "seed-demo":
            seed_demo_data(service)
            print("Demo data loaded.")
            return 0

    except ValueError as exc:
        print(f"Error: {exc}")
        return 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
