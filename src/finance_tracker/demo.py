from __future__ import annotations

from finance_tracker.services import FinanceTrackerService


def seed_demo_data(service: FinanceTrackerService) -> None:
    sample_categories = [
        ("Food", "Meals, delivery and groceries"),
        ("Transport", "App rides, fuel and public transit"),
        ("Education", "Courses, books and subscriptions"),
        ("Health", "Medicine and medical appointments"),
    ]

    for name, description in sample_categories:
        try:
            service.create_category(name, description)
        except ValueError:
            pass

    sample_expenses = [
        ("Food", "Supermarket", "245.90", "2026-04-02", "Monthly groceries"),
        ("Transport", "Bus card", "120.00", "2026-04-05", "Recharge"),
        ("Education", "Python backend course", "89.90", "2026-04-08", "Career investment"),
        ("Health", "Pharmacy", "43.50", "2026-04-10", "Cold medicine"),
        ("Food", "Lunch with team", "38.00", "2026-04-15", "Office day"),
    ]

    existing_april = service.list_expenses("2026-04")
    if existing_april:
        return

    for category_name, title, amount, expense_date, notes in sample_expenses:
        service.register_expense(None, category_name, title, amount, expense_date, notes)
