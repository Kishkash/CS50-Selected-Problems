import sqlite3

conn = sqlite3.connect("finance.db")
db = conn.cursor()

db.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT    NOT NULL UNIQUE,
        hash     TEXT    NOT NULL,
        cash     REAL    NOT NULL DEFAULT 10000.00
    );

    CREATE TABLE IF NOT EXISTS stocks (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id  INTEGER NOT NULL,
        stock_id TEXT    NOT NULL,
        shares   INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id),
        UNIQUE (user_id, stock_id)
    );

    CREATE TABLE IF NOT EXISTS transactions (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        action  TEXT    NOT NULL CHECK (action IN ('bought', 'sold')),
        stock   TEXT    NOT NULL,
        amount  INTEGER NOT NULL,
        price   REAL    NOT NULL,
        time    TEXT    NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
""")

conn.commit()
conn.close()
print("finance.db created successfully.")
