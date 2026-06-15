# Birthday Tracker (CS50 Problem Set – Python & Flask)

This project is a lightweight web application for storing and managing birthdays. It was originally completed as part of Harvard’s CS50 Introduction to Computer Science course and later refined into a clean, maintainable Flask application.

The app allows users to add birthdays, view all stored entries, and delete records — all backed by a simple SQLite database and a Flask/Jinja frontend.

## Features

- Add birthdays with server side validation
- Display all stored birthdays in a table
- Delete entries with a single click
- Persistent storage using SQLite
- Simple, readable Flask routing
- Jinja2 templating for dynamic HTML
- Custom CSS styling
- Safe database access via a per request connection stored on `g`

## How It Works

### 1. Adding Birthdays

Users submit a name and date. The server validates the input and inserts it into the `birthdays` table.

### 2. Displaying Birthdays

All entries are fetched from the database and rendered in a table using a Jinja template.

### 3. Deleting Birthdays

Each row includes a delete button that removes the corresponding entry from the database.

## Database Schema

The app uses a simple SQLite table:

| Column | Type | Description |
|---------|------|-------------|
| id | INTEGER | Primary key |
| name | TEXT | Person’s name |
| month | INTEGER | Month of birthday |
| day | INTEGER | Day of birthday |

## Usage

Run `birthdays_init.py` to intiate the database (Only on first use).

Run `app.py` and then navigate in your browser to:

```text
http://127.0.0.1:5000/
```

You can now add, view, and delete birthdays.

## File Overview

```text
birthday/
├── app.py
├── birthdays_init_db.py
├── templates/
│   └── index.html
└── static/
    └── styles.css
```

- `app.py` — main Flask application
- `birthdays_init_db.py` — initializes the SQLite database
- `templates/index.html` — Jinja template for the UI
- `static/styles.css` — custom styling

## About CS50

This project is based on Problem Set 9 – Birthdays from Harvard’s CS50 course.

The original assignment is minimal and procedural; this version includes structural improvements and cleaner Flask patterns as part of my learning journey.
