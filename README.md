# Finance Tracker
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue)
![Tests](https://img.shields.io/badge/Tests-unittest-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A full-featured personal finance tracker built with Python, designed to manage expenses, organize categories, and generate monthly insights through both a web interface and a CLI tool.

This project was created as a production-inspired finance application to demonstrate backend architecture, data modeling, authentication, and real-world application structure.

---

## Overview

Finance Tracker allows users to:# 💰 Finance Tracker

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python\&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?logo=flask\&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?logo=sqlite\&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-unittest-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A production-inspired personal finance application with both **web and CLI interfaces**, built to manage expenses, organize categories, and generate monthly insights.

This project demonstrates **backend architecture, data modeling, authentication, and scalable application design**.

---

## 🚀 Overview

Finance Tracker allows users to:

* Track personal expenses with structured data
* Organize spending into custom categories
* Analyze monthly summaries and breakdowns
* Interact through both a web dashboard and CLI

It emphasizes **clean architecture, separation of concerns, and maintainable code design**.

---

## ✨ Key Highlights

* 🔐 Authentication system (signup & login)
* 🧠 Layered architecture (services, repository, models)
* 💾 Persistent storage with SQLite
* 📊 Monthly summaries and category breakdowns
* 🌐 Web interface with clean UI
* 🧪 Unit-tested business logic
* 💻 CLI support for backend interaction

---

## 🧩 Features

* Create and manage expense categories
* Add expenses with title, amount, date, and notes
* Filter expenses by month
* Generate monthly summaries
* View spending grouped by category
* Load demo data for presentation
* Access via web dashboard or CLI

---

## 🏗️ Project Structure

```text
finance-tracker/
├── run.py
├── pyproject.toml
├── static/
│   └── css/
│       └── styles.css
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── demo.html
│   ├── docs.html
│   ├── home.html
│   ├── login.html
│   └── register.html
├── tests/
│   └── test_service.py
└── src/finance_tracker/
    ├── __main__.py
    ├── cli.py
    ├── database.py
    ├── demo.py
    ├── models.py
    ├── money.py
    ├── repository.py
    ├── services.py
    ├── translations.py
    └── web.py
```

---

## ⚙️ Tech Stack

### Backend

* Python 3.11+
* Flask (web framework)
* SQLite (relational database)

### Architecture

* Layered architecture (services, repository, models)
* Separation of concerns

### Data Handling

* dataclasses (structured models)
* decimal (financial precision)

### CLI & Testing

* argparse (command-line interface)
* unittest (testing)

---

## ▶️ Running the Web App

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -e .
python run.py
```

Open in your browser:

```text
http://127.0.0.1:5000
```

---

## ☁️ Deployment

The project includes `app.py` and `vercel.json` for deployment on Vercel.

---

## 💻 CLI Usage

```bash
finance-tracker init-db
finance-tracker seed-demo
finance-tracker list-categories
finance-tracker list-expenses --month 2026-04
finance-tracker monthly-summary 2026-04
```

---

## 🔄 Example User Flow

1. Access the landing page
2. Create an account
3. Log in to the dashboard
4. Add and manage expenses
5. Analyze monthly summaries

---

## 📊 Sample Output

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

---

## 🧪 Running Tests

```bash
python -m unittest discover -s tests
```

---

## 🧠 Engineering Focus

* Clean and maintainable backend architecture
* Reusable domain logic shared between CLI and web
* Data validation and integrity
* Financial precision using `decimal` instead of `float`

---

## 🛣️ Roadmap

* [ ] Income tracking
* [ ] CSV export
* [ ] Edit and delete expenses
* [ ] Recurring expenses
* [ ] Dashboard charts and advanced filters

---

## 📸 Suggested Additions

* Add screenshots of dashboard, login, and summaries
* Include a demo GIF
* Show CLI usage in action
* Add a short demo video (optional)

---

## 📄 License

This project is licensed under the MIT License.
See the full license here: [LICENSE](./LICENSE)


* Track personal expenses with structured data
* Organize spending into custom categories
* Analyze monthly summaries and breakdowns
* Interact through both a web dashboard and CLI

It emphasizes clean architecture, separation of concerns, and maintainable code design.

---

## Key Highlights

* Authentication system with signup and login
* Layered backend architecture with services, repository, and models
* Persistent storage with SQLite
* Monthly summaries and category breakdowns
* Web interface with a clean UI
* Unit-tested business logic
* CLI support for backend interaction and demos

---

## Features

* Create and manage expense categories
* Add expenses with title, amount, date, and notes
* Filter expenses by month
* Generate monthly summaries
* View spending grouped by category
* Load demo data for presentation
* Access via web dashboard or CLI

---

## Project Structure

```text
finance-tracker/
|-- run.py
|-- pyproject.toml
|-- static/
|   `-- css/
|       `-- styles.css
|-- templates/
|   |-- base.html
|   |-- dashboard.html
|   |-- demo.html
|   |-- docs.html
|   |-- home.html
|   |-- login.html
|   `-- register.html
|-- tests/
|   `-- test_service.py
`-- src/finance_tracker/
    |-- __main__.py
    |-- cli.py
    |-- database.py
    |-- demo.py
    |-- models.py
    |-- money.py
    |-- repository.py
    |-- services.py
    |-- translations.py
    `-- web.py
```

---

## Tech Stack

* Python 3.11+
* Flask
* SQLite
* argparse
* dataclasses
* decimal

---

## Running the Web App

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
python run.py
```

Open in your browser:

```text
http://127.0.0.1:5000
```

---

## Deployment

The project includes `app.py` and `vercel.json` for deployment on Vercel.

---

## CLI Usage

```bash
finance-tracker init-db
finance-tracker seed-demo
finance-tracker list-categories
finance-tracker list-expenses --month 2026-04
finance-tracker monthly-summary 2026-04
```

---

## Example User Flow

1. Access the landing page
2. Create an account
3. Log in to the dashboard
4. Add and manage expenses
5. Analyze monthly summaries

---

## Sample Output

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

---

## Running Tests

```bash
python -m unittest discover -s tests
```

---

## Roadmap

* [ ] Income tracking
* [ ] CSV export
* [ ] Edit and delete expenses
* [ ] Recurring expenses
* [ ] Dashboard charts and advanced filters

---

## Suggested Additions

* Add screenshots of the dashboard, login, and summary pages
* Include a short demo GIF
* Show CLI usage in action
* Add a short demo video if desired

---

## License

This project is licensed under the MIT License.

See the full license here: [LICENSE](./LICENSE)
