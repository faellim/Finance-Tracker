from __future__ import annotations

import os
from datetime import date
from pathlib import Path

from flask import (
    Flask,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from finance_tracker.database import DEFAULT_DB_PATH, get_connection, initialize_database
from finance_tracker.demo import seed_demo_data
from finance_tracker.repository import CategoryRepository, ExpenseRepository, UserRepository
from finance_tracker.services import AuthService, FinanceTrackerService
from finance_tracker.translations import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES, get_language, translate


def create_app(db_path: str | Path = DEFAULT_DB_PATH) -> Flask:
    app = Flask(
        __name__,
        template_folder="../../templates",
        static_folder="../../static",
    )
    app.config["DATABASE_PATH"] = str(db_path)
    app.config["SECRET_KEY"] = os.getenv("FINANCE_TRACKER_SECRET", "dev-secret-change-me")
    app.config["GITHUB_URL"] = os.getenv(
        "FINANCE_TRACKER_GITHUB_URL",
        "https://github.com/your-username/finance-tracker",
    )

    @app.before_request
    def load_language() -> None:
        requested = request.args.get("lang")
        if requested in SUPPORTED_LANGUAGES:
            session["lang"] = requested
        if "lang" not in session:
            session["lang"] = get_language(request.headers.get("Accept-Language"))
        g.lang = session.get("lang", DEFAULT_LANGUAGE)

    def t(key: str, **kwargs: str) -> str:
        return translate(getattr(g, "lang", DEFAULT_LANGUAGE), key, **kwargs)

    def flash_t(key: str, category: str = "success", **kwargs: str) -> None:
        flash(t(key, **kwargs), category)

    def get_services() -> tuple[AuthService, FinanceTrackerService]:
        if "db_connection" not in g:
            g.db_connection = get_connection(app.config["DATABASE_PATH"])
            initialize_database(g.db_connection)

        connection = g.db_connection
        auth_service = AuthService(UserRepository(connection))
        finance_service = FinanceTrackerService(
            category_repository=CategoryRepository(connection),
            expense_repository=ExpenseRepository(connection),
        )
        return auth_service, finance_service

    @app.teardown_appcontext
    def close_connection(_: object | None) -> None:
        connection = g.pop("db_connection", None)
        if connection is not None:
            connection.close()

    @app.context_processor
    def inject_user() -> dict[str, object]:
        return {
            "current_user_name": session.get("user_name"),
            "current_year": date.today().year,
            "current_path": request.path,
            "github_url": app.config["GITHUB_URL"],
            "current_lang": getattr(g, "lang", DEFAULT_LANGUAGE),
            "supported_languages": SUPPORTED_LANGUAGES,
            "t": t,
        }

    @app.get("/set-language/<lang>")
    def set_language(lang: str):
        if lang in SUPPORTED_LANGUAGES:
            session["lang"] = lang
        target = request.args.get("next") or url_for("home")
        return redirect(target)

    @app.get("/")
    def home():
        _, finance_service = get_services()
        seed_demo_data(finance_service)
        summary, category_breakdown = finance_service.get_monthly_summary("2026-04")
        expenses = finance_service.list_expenses("2026-04")[:4]
        return render_template(
            "home.html",
            summary=summary,
            category_breakdown=category_breakdown,
            expenses=expenses,
        )

    @app.get("/demo")
    def demo():
        _, finance_service = get_services()
        seed_demo_data(finance_service)
        selected_month = request.args.get("month", "2026-04")
        try:
            summary, category_breakdown = finance_service.get_monthly_summary(selected_month)
            expenses = finance_service.list_expenses(selected_month)
        except ValueError:
            flash_t("message_month_format", "error")
            return redirect(url_for("demo", month="2026-04"))
        return render_template(
            "demo.html",
            summary=summary,
            category_breakdown=category_breakdown,
            expenses=expenses,
            selected_month=selected_month,
        )

    @app.get("/docs")
    def docs():
        return render_template("docs.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        auth_service, finance_service = get_services()
        if request.method == "POST":
            full_name = request.form.get("full_name", "")
            email = request.form.get("email", "")
            password = request.form.get("password", "")
            confirm_password = request.form.get("confirm_password", "")
            try:
                if password != confirm_password:
                    raise ValueError(t("message_passwords_no_match"))
                user = auth_service.register_user(full_name, email, password)
                ensure_default_categories(finance_service)
                session["user_id"] = user.id
                session["user_name"] = user.full_name
                flash_t("message_account_created", "success")
                return redirect(url_for("dashboard"))
            except ValueError as exc:
                flash(str(exc), "error")
        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        auth_service, _ = get_services()
        if request.method == "POST":
            email = request.form.get("email", "")
            password = request.form.get("password", "")
            try:
                user = auth_service.authenticate(email, password)
                session["user_id"] = user.id
                session["user_name"] = user.full_name
                flash_t("message_welcome_back", "success")
                return redirect(url_for("dashboard"))
            except ValueError as exc:
                flash(str(exc), "error")
        return render_template("login.html")

    @app.get("/logout")
    def logout():
        session.clear()
        session["lang"] = getattr(g, "lang", DEFAULT_LANGUAGE)
        flash_t("message_session_finished", "success")
        return redirect(url_for("home"))

    @app.get("/api/health")
    def api_health():
        return jsonify(
            {
                "status": "ok",
                "service": "finance-tracker",
                "stack": ["Flask", "SQLite", "Python"],
            }
        )

    @app.get("/api/demo/monthly-summary")
    def api_demo_monthly_summary():
        _, finance_service = get_services()
        seed_demo_data(finance_service)
        month = request.args.get("month", "2026-04")
        try:
            summary, category_breakdown = finance_service.get_monthly_summary(month)
        except ValueError:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": t("message_month_format"),
                        "field": "month",
                    }
                ),
                400,
            )
        return jsonify(
            {
                "status": "success",
                "data": {
                    "month": summary.month,
                    "total_expenses": str(summary.total_expenses),
                    "number_of_expenses": summary.number_of_expenses,
                    "categories": [
                        {
                            "category_name": item.category_name,
                            "total_amount": str(item.total_amount),
                            "expense_count": item.expense_count,
                        }
                        for item in category_breakdown
                    ],
                },
            }
        )

    @app.get("/api/demo/expenses")
    def api_demo_expenses():
        _, finance_service = get_services()
        seed_demo_data(finance_service)
        month = request.args.get("month", "2026-04")
        try:
            expenses = finance_service.list_expenses(month)
        except ValueError:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": t("message_month_format"),
                        "field": "month",
                    }
                ),
                400,
            )
        return jsonify(
            {
                "status": "success",
                "data": {
                    "month": month,
                    "items": [
                        {
                            "id": expense.id,
                            "title": expense.title,
                            "category": expense.category_name,
                            "amount": str(expense.amount),
                            "expense_date": expense.expense_date.isoformat(),
                            "notes": expense.notes,
                        }
                        for expense in expenses
                    ],
                },
            }
        )

    @app.route("/dashboard", methods=["GET", "POST"])
    def dashboard():
        _, finance_service = get_services()
        user_id = session.get("user_id")
        if user_id is None:
            flash_t("message_login_required", "error")
            return redirect(url_for("login"))

        ensure_default_categories(finance_service)
        selected_month = request.values.get("month") or date.today().strftime("%Y-%m")

        if request.method == "POST":
            try:
                finance_service.register_expense(
                    user_id=user_id,
                    category_name=request.form.get("category", ""),
                    title=request.form.get("title", ""),
                    amount_text=request.form.get("amount", ""),
                    expense_date_text=request.form.get("expense_date", ""),
                    notes=request.form.get("notes", ""),
                )
                flash_t("message_expense_added", "success")
                return redirect(url_for("dashboard", month=selected_month))
            except ValueError as exc:
                flash(str(exc), "error")

        expenses = finance_service.list_expenses(selected_month, user_id=user_id)
        summary, category_breakdown = finance_service.get_monthly_summary(
            selected_month,
            user_id=user_id,
        )
        categories = finance_service.list_categories()
        top_category = category_breakdown[0] if category_breakdown else None
        return render_template(
            "dashboard.html",
            categories=categories,
            expenses=expenses,
            summary=summary,
            category_breakdown=category_breakdown,
            selected_month=selected_month,
            top_category=top_category,
        )

    return app


def ensure_default_categories(finance_service: FinanceTrackerService) -> None:
    defaults = [
        ("Food", "Meals, groceries and coffee"),
        ("Transport", "Fuel, public transit and rides"),
        ("Education", "Courses, books and subscriptions"),
        ("Health", "Medicine and appointments"),
        ("Bills", "Rent, internet and recurring costs"),
    ]
    existing = {category.name.lower() for category in finance_service.list_categories()}
    for name, description in defaults:
        if name.lower() not in existing:
            finance_service.create_category(name, description)


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
