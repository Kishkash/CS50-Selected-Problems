import sqlite3

conn = sqlite3.connect("birthdays.db")
db = conn.cursor()

db.executescript("""
    CREATE TABLE IF NOT EXISTS birthdays (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        name  TEXT    NOT NULL,
        month INTEGER NOT NULL,
        day   INTEGER NOT NULL
    );
""")

conn.commit()
conn.close()
print("birthdays.db created successfully.")
