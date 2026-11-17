import os

from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from database import query_one, execute

from helpers import apology, login_required, lookup, usd
from models.stock import buy_stock
from models.users import find_user

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method != "POST":
        return render_template("buy.html")
        
    user_id = session["user_id"]

    data = request.get_json()
    symbol = data.get("symbol", "").strip().upper()

    if not symbol:
        return jsonify({"message": "Symbol is required!!"}), 400
    
    try:
        stock = lookup(symbol)
    except Exception:
        return jsonify({"message": "Failed to fetch stock data"}), 502

    if stock is None:
        return jsonify({"message": "Stock not found!!"}), 404

    user = find_user(user_id)

    if user is None:
        return redirect("/login")

    if user["cash"] < stock["price"]:
        return jsonify({"message": "Not enough cash"}), 400

    cash = user["cash"] - stock["price"]

    buy_stock(stock["name"], stock["price"], symbol, user_id, cash)

    return jsonify(stock), 201


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        row = query_one("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))

        # Ensure username exists and password is correct
        if not row or not check_password_hash(
            row["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = row["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method != "POST":
        return render_template("quote.html")

    data = request.get_json()

    symbol = data.get("symbol", "")

    #validation
    if not symbol:
        return jsonify({"message": "Symbol is required."}), 400

    stock = lookup(symbol)
    print(stock)

    if stock is None:
        return jsonify({"message": "stock not found!!"}), 404

    return jsonify(stock), 200


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method != "POST":
        return render_template("register.html")

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    confirmation = data.get("confirmation")

    # Validation
    if not all([username, password, confirmation]):
        return jsonify({"message": "All fields should be entered"}), 400

    if password != confirmation:
        return jsonify({"message": "The passwords do not match!!"}), 400
    
    if query_one("SELECT * FROM users WHERE username=?", (username,)):
        return jsonify({"message": "User already exists!!"}), 409
    
    execute("INSERT INTO users (username, hash) VALUES (?,?)", (username, generate_password_hash(password)))
    return jsonify({"message": None}), 200


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")
