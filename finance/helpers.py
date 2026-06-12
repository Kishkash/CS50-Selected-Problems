import yfinance as yf
from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    return render_template("apology.html", message=message, code=code), code


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def lookup(symbol):
    try:
        ticker = yf.Ticker(symbol)
        price = ticker.fast_info["last_price"]
        if not price:
            return None
        return {
            "symbol": symbol.upper(),
            "price": round(price, 2)
        }
    except Exception:
        return None


def usd(value):
    return f"${value:,.2f}"
