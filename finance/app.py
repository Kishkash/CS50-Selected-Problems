import sqlite3
from flask import Flask, flash, g, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Database connection — one per request, stored on Flask's g object
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("finance.db", check_same_thread=False)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON;")
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
@login_required
def index():
    # The index page has a "buy more shares" form that POSTs here
    if request.method == "POST":
        return buy()

    db = get_db()
    user_id = session["user_id"]

    stocks = db.execute(
        "SELECT * FROM stocks WHERE user_id = ? ORDER BY stock_id",
        (user_id,)
    ).fetchall()

    prices = []
    total_values = []
    stocks_sum = 0

    for stock in stocks:
        current = lookup(stock["stock_id"])
        current_price = current["price"]
        current_total = current_price * stock["shares"]

        prices.append(usd(current_price))
        total_values.append(usd(current_total))
        stocks_sum += current_total

    cash = db.execute(
        "SELECT cash FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()["cash"]

    return render_template(
        "index.html",
        stocks=stocks,
        prices=prices,
        total_values=total_values,
        cash_usd=usd(cash),
        grand_total=usd(cash + stocks_sum)
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    db = get_db()
    user_id = session["user_id"]

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol or not shares:
            return apology("Empty field")

        if not shares.isdigit() or int(shares) < 1:
            return apology("Shares must be a positive integer")

        data = lookup(symbol)
        if not data:
            return apology("Invalid symbol")

        price = data["price"]
        cost = price * int(shares)

        cash = db.execute(
            "SELECT cash FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()["cash"]

        if cash < cost:
            return apology("Not enough cash")

        # Deduct cash
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            (cash - cost, user_id)
        )

        # Record transaction
        db.execute(
            "INSERT INTO transactions (user_id, action, stock, amount, price, time) "
            "VALUES (?, 'bought', ?, ?, ?, datetime('now','localtime'))",
            (user_id, symbol.upper(), shares, price)
        )

        # Update stocks
        existing = db.execute(
            "SELECT shares FROM stocks WHERE user_id = ? AND stock_id = ?",
            (user_id, symbol.upper())
        ).fetchone()

        if existing:
            new_total = existing["shares"] + int(shares)
            db.execute(
                "UPDATE stocks SET shares = ? WHERE user_id = ? AND stock_id = ?",
                (new_total, user_id, symbol.upper())
            )
        else:
            db.execute(
                "INSERT INTO stocks (user_id, stock_id, shares) VALUES (?, ?, ?)",
                (user_id, symbol.upper(), int(shares))
            )

        db.commit()
        return redirect("/")

    return render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    db = get_db()
    user_id = session["user_id"]

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol or not shares:
            return apology("Empty field")

        if not shares.isdigit() or int(shares) < 1:
            return apology("Shares must be a positive integer")

        owned = db.execute(
            "SELECT shares FROM stocks WHERE user_id = ? AND stock_id = ?",
            (user_id, symbol)
        ).fetchone()

        if not owned:
            return apology("You don't own this stock")

        if owned["shares"] < int(shares):
            return apology("Not enough shares")

        data = lookup(symbol)
        price = data["price"]
        revenue = price * int(shares)

        cash = db.execute(
            "SELECT cash FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()["cash"]

        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            (cash + revenue, user_id)
        )

        # Record transaction
        db.execute(
            "INSERT INTO transactions (user_id, action, stock, amount, price, time) "
            "VALUES (?, 'sold', ?, ?, ?, datetime('now','localtime'))",
            (user_id, symbol, shares, price)
        )

        # Update or delete stock
        new_total = owned["shares"] - int(shares)
        if new_total == 0:
            db.execute(
                "DELETE FROM stocks WHERE user_id = ? AND stock_id = ?",
                (user_id, symbol)
            )
        else:
            db.execute(
                "UPDATE stocks SET shares = ? WHERE user_id = ? AND stock_id = ?",
                (new_total, user_id, symbol)
            )

        db.commit()
        return redirect("/")

    stocks = db.execute(
        "SELECT stock_id FROM stocks WHERE user_id = ?",
        (user_id,)
    ).fetchall()

    return render_template("sell.html", stocks=stocks)


@app.route("/history")
@login_required
def history():
    db = get_db()
    user_id = session["user_id"]

    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = ?",
        (user_id,)
    ).fetchall()

    if not transactions:
        return apology("No transactions in database", 400)

    prices = []
    for transaction in transactions:
        prices.append(usd(transaction["price"]))

    return render_template("history.html", transactions=transactions, prices=prices)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        db = get_db()
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (request.form.get("username"),)
        ).fetchall()

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Empty field", 400)

        data = lookup(symbol)
        if not data:
            return apology("Couldn't find company symbol", 400)

        return render_template("qouted.html", symbol=data["symbol"], price=usd(data["price"]))

    return render_template("qoute.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("Empty field", 400)

        if password != confirmation:
            return apology("Passwords do not match", 400)

        db = get_db()
        existing = db.execute(
            "SELECT username FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if existing:
            return apology("Username already in use", 400)

        hash = generate_password_hash(password, method="pbkdf2", salt_length=16)

        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            (username, hash)
        )
        db.commit()

        return redirect("/")

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
