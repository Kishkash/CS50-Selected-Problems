# CS50 Python & Flask Projects

A collection of selected problem set solutions from Harvard’s CS50.

This repository showcases several CS50 assignments rebuilt with clean code and modern Python practices. Each project demonstrates a different backend skill: database design, form handling, OOP, API integration, authentication, and session management.

## Projects Included

### 1. Birthday — Flask CRUD App with SQLite

A lightweight web application for storing and managing birthdays.

#### Highlights

- CRUD (Create + Read + Delete) using SQLite
- Clean Flask routing and session configuration
- HTML templating with Jinja
- Custom CSS styling
- Safe database access via a per-request connection stored on `g`

#### Tech Stack

- Python, Flask
- SQLite
- HTML/CSS (custom)
- Jinja2

#### Key Features

- Add birthdays with validation
- Display all birthdays in a table
- Delete entries
- Persistent storage via `birthdays.db`

---

### 2. Credit — Object Oriented Luhn Validator

A Python OOP implementation of the CS50 credit card validation problem.

#### Highlights

- Object oriented design
- Clean separation of concerns (`_detect_type`, `_check_luhn`)
- Supports AMEX, Mastercard, Visa
- Robust input validation

#### Tech Stack

- Python (OOP)

#### Key Features

- Detects card type based on number patterns
- Validates using Luhn’s algorithm
- Returns `"INVALID"` for any failing case

---

### 3. Finance — Full Stack Stock Trading Simulator

A complete Flask application that simulates buying and selling stocks using real time market data.

#### Highlights

- User authentication (register/login/logout)
- Session management
- Real time stock lookup via Yahoo Finance (`yfinance`)
- Transaction history
- Portfolio dashboard with live pricing
- Relational database with foreign keys
- Bootstrap 5 UI

#### Tech Stack

- Python, Flask
- SQLite
- Bootstrap 5
- Jinja2
- Yahoo Finance API (`yfinance`)

#### Key Features

- Buy and sell shares with validation
- Track cash balance and portfolio value
- View full transaction history
- Dynamic price lookup

---

## Project Structure

```text
/
├── birthday/
│   ├── app.py
│   ├── birthdays_init_db.py
│   ├── templates/
│   └── static/
│
├── credit/
│   └── credit.py
│
├── finance/
│   ├── app.py
│   ├── helpers.py
│   ├── init_db.py
│   ├── templates/
│   └── static/
│
└── README.md  ← you are here
```

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the databases

```bash
python birthdays/birthdays_init_db.py
python finance/init_db.py
```

### 5. Run any project

```bash
flask run
```

## Skills Demonstrated

### Backend Development

- Flask routing & blueprints
- Session handling
- Authentication & authorization
- Form validation
- Database schema design
- SQL queries & transactions

### Python

- OOP design
- Error handling
- Modular architecture
- Clean, readable code

### Frontend

- Bootstrap 5
- Custom CSS
- Jinja templating
- Responsive layouts

### APIs & External Libraries

- Yahoo Finance API (`yfinance`)
- Werkzeug password hashing
- Flask Session

## What I Learned

- How to structure Flask apps cleanly for maintainability
- How to design relational schemas for real world workflows
- How to integrate external APIs safely
- How to build user authentication from scratch
- How to write Python code that is both readable and robust

## Future Improvements

- Add unit tests for the Credit OOP module
- Add pagination and filtering to Finance transaction history
- Add edit functionality to Birthdays
- Containerize each project with Docker
