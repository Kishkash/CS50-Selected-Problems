import sqlite3
from flask import Flask, g, redirect, render_template, request
from flask_session import Session

# Configure application
app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Database connection — one per request, stored on Flask's g object
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("birthdays.db", check_same_thread=False)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db()

    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            return redirect("/")

        month = request.form.get("month")
        if not month:
            return redirect("/")
        try:
            month = int(month)
        except ValueError:
            return redirect("/")

        day = request.form.get("day")
        if not day:
            return redirect("/")
        try:
            day = int(day)
        except ValueError:
            return redirect("/")

        db.execute(
            "INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)",
            (name, month, day)
        )
        db.commit()
        return redirect("/")

    else:
        birthdays = db.execute("SELECT * FROM birthdays").fetchall()
        return render_template("index.html", birthdays=birthdays)


@app.route("/delete", methods=["POST"])
def delete():
    db = get_db()
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM birthdays WHERE id = ?", (id,))
        db.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
