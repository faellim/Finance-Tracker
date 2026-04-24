# Finance Tracker

Finance Tracker is a Python web application for managing personal expenses, custom categories and monthly summaries. It was designed as a portfolio project that highlights backend structure, authentication, SQLite persistence and a polished frontend experience.

## Why this project is good for a portfolio

- Shows practical backend logic with layered architecture.
- Uses SQLite for persistent storage and relational data modeling.
- Includes authentication with separate login and signup pages.
- Applies input validation for amount, dates and category rules.
- Generates monthly summaries and category breakdowns.
- Combines backend clarity with a product-style interface.

## Features

- Create and list expense categories
- Register expenses with title, amount, date and notes
- Sign up and log in with your own account
- Store data in SQLite
- View all expenses or filter by month
- Generate monthly summary totals
- See spending grouped by category
- Use a web dashboard with modern UI
- Load demo data for screenshots and GitHub presentation

## Project structure

```text
finance-tracker/
|-- README.md
|-- run.py
|-- static/
|   `-- css/
|       `-- styles.css
|-- templates/
|   |-- base.html
|   |-- dashboard.html
|   |-- home.html
|   |-- login.html
|   `-- register.html
|-- tests/
|   `-- test_service.py
|-- pyproject.toml
`-- src/
    `-- finance_tracker/
        |-- __main__.py
        |-- cli.py
        |-- database.py
        |-- demo.py
        |-- models.py
        |-- money.py
        |-- repository.py
        |-- services.py
        `-- web.py
```

## Technologies used

- Python 3.11+
- Flask
- SQLite
- argparse
- dataclasses
- decimal

## How to run the web app

Create a virtual environment, install the project locally and start the Flask app:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
python run.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Deploy on Vercel

This project includes `app.py` and `vercel.json` so the Flask app can be deployed on Vercel using the project root as the deployment directory.

## CLI commands

The original CLI is still available for backend demonstrations:

```bash
finance-tracker init-db
finance-tracker seed-demo
finance-tracker list-categories
finance-tracker list-expenses --month 2026-04
finance-tracker monthly-summary 2026-04
```

## Example web flow

```bash
1. Open the landing page
2. Create an account on the signup page
3. Log in and access the dashboard
4. Add expenses and filter the month
5. Review monthly totals and category breakdowns
```

## Sample summary output

```text
Monthly summary for 2026-04
Total expenses: $537.30
Number of expenses: 5
Breakdown by category:
- Food: $283.90 (2 expense(s))
- Transport: $120.00 (1 expense(s))
- Education: $89.90 (1 expense(s))
- Health: $43.50 (1 expense(s))
```

## Next improvements

- Add income tracking
- Export reports to CSV
- Add edit and delete flows for expenses
- Add recurring expenses
- Add charts and richer filtering in the dashboard

## Running tests

This project includes basic unit tests using the Python standard library:

```bash
python -m unittest discover -s tests
```

## GitHub portfolio tips

- Capture screenshots of the landing page, login page and dashboard.
- Add screenshots of the terminal commands running with demo data.
- Write a short section in your GitHub description explaining that the project focuses on backend architecture, authentication and data organization.
- In interviews, mention that you intentionally separated domain logic from the web layer to keep the codebase maintainable.
