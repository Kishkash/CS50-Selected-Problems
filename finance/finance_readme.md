# Finance — Stock Trading Simulator (CS50 Problem Set – Python & Flask)

This project is a full stack stock trading simulator built with Flask and SQLite. It was originally completed as part of Harvard’s CS50 Introduction to Computer Science course and later refined into a more maintainable, production style Flask application.

The app allows users to register, log in, look up real time stock prices, buy and sell shares, track their portfolio value, and review their full transaction history — all using a clean backend architecture and the Yahoo Finance API.

## Features

- User authentication (register, login, logout)
- Real time stock price lookup via `yfinance`
- Buy and sell shares with full validation
- Track cash balance and portfolio value
- View complete transaction history
- Persistent storage using SQLite
- Clean Flask routing and session management
- Jinja2 templates with Bootstrap 5 UI
- Safe database access via a per request connection stored on `g`

## How It Works

### 1. User Accounts

Users can create an account with a unique username and password. Passwords are securely hashed using Werkzeug.

### 2. Stock Lookup

The app uses the Yahoo Finance API (`yfinance`) to fetch live stock prices:

- Validates symbol
- Returns price rounded to two decimals
- Displays results in a dedicated quote page

### 3. Buying Shares

When a user buys shares:

- The symbol and share count are validated
- The user’s cash balance is checked
- A transaction is recorded
- The user’s portfolio is updated

### 4. Selling Shares

When selling:

- The app verifies the user owns enough shares
- Cash balance is increased
- Shares are deducted or removed
- A transaction is logged

### 5. Portfolio Dashboard

The homepage displays:

- All owned stocks
- Current live prices
- Total value per holding
- Cash balance
- Grand total portfolio value

### 6. Transaction History

A complete log of all buys and sells, including:

- Stock symbol
- Action (bought/sold)
- Number of shares
- Price at time of transaction
- Timestamp

## Database Schema

The app uses three tables:

### users

| Column | Type | Description |
|---------|------|-------------|
| id | INTEGER | Primary key |
| username | TEXT | Unique username |
| hash | TEXT | Password hash |
| cash | REAL | User’s cash balance |

### stocks

| Column | Type | Description |
|---------|------|-------------|
| id | INTEGER | Primary key |
| user_id | INTEGER | Foreign key → users.id |
| stock_id | TEXT | Stock symbol |
| shares | INTEGER | Number of shares owned |

### transactions

| Column | Type | Description |
|---------|------|-------------|
| id | INTEGER | Primary key |
| user_id | INTEGER | Foreign key → users.id |
| action | TEXT | "bought" or "sold" |
| stock | TEXT | Stock symbol |
| amount | INTEGER | Number of shares |
| price | REAL | Price at transaction time |
| time | TEXT | Timestamp |

## Usage

Run `init_db.py` to initiate database (only on first use).

Run `app.py` and then navigate in your browser to:

```text
http://127.0.0.1:5000/
```

You can now register, log in, look up stocks, buy and sell shares, and view your portfolio.

## File Overview

```text
finance/
├── app.py
├── helpers.py
├── init_db.py
├── templates/
│   ├── index.html
│   ├── buy.html
│   ├── sell.html
│   ├── quote.html
│   ├── quoted.html
│   ├── history.html
│   ├── login.html
│   ├── register.html
│   └── apology.html
└── static/
    └── styles.css
```

- `app.py` — main Flask application and route logic
- `helpers.py` — utility functions (`lookup`, `usd`, `login_required`, `apology`)
- `init_db.py` — initializes the SQLite database
- `templates/` — Jinja2 HTML templates
- `static/` — CSS and static assets

## About CS50

This project is based on Problem Set 9 – Finance from Harvard’s CS50 course.

The original assignment uses a simplified API and procedural structure; this version includes architectural improvements, real time data via Yahoo Finance, and cleaner Flask patterns as part of my learning journey.
