import requests
import os
import sqlite3
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

# Configure application
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database connection management
def get_db():
    """Open a new database connection if there is none yet for the current request."""
    if not hasattr(g, 'sqlite_db'):
        db = sqlite3.connect("database.db")
        db.row_factory = sqlite3.Row  # Enable dict-like row access
        g.sqlite_db = db
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Close the database connection at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    """Decorate routes to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.after_request
def after_request(response):
    """Ensure responses aren't cached."""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT articles.id, articles.title, articles.content, articles.created_at, users.username AS author
        FROM articles
        JOIN users ON articles.user_id = users.id
        ORDER BY articles.created_at DESC
        LIMIT 20
    """)
    rows = cursor.fetchall()
    articles = []
    for row in rows:
        article = dict(row)
        if isinstance(article["created_at"], str):
            try:
                article["created_at"] = datetime.strptime(article["created_at"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                try:
                    article["created_at"] = datetime.strptime(article["created_at"], "%Y-%m-%d %H:%M:%S.%f")
                except Exception:
                    pass
        articles.append(article)
    return render_template("index.html", articles=articles)

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return apology("must provide username", 403)
        if not password:
            return apology("must provide password", 403)
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user is None or not check_password_hash(user["hash"], password):
            return apology("invalid username and/or password", 403)
        session["user_id"] = user["id"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    db = get_db()
    cursor = db.cursor()
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        # Fetch user
        cursor.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],))
        user = cursor.fetchone()
        if not user or not check_password_hash(user["hash"], current_password):
            return apology("Current password is incorrect", 400)
        if not new_password or new_password != confirm_password:
            return apology("New passwords do not match", 400)
        hash_pw = generate_password_hash(new_password)
        cursor.execute("UPDATE users SET hash = ? WHERE id = ?", (hash_pw, session["user_id"]))
        db.commit()
        flash("Password updated successfully!")
        return redirect("/account")
    else:
        cursor.execute("SELECT username FROM users WHERE id = ?", (session["user_id"],))
        user = cursor.fetchone()
        return render_template("account.html", user=user)

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username:
            return apology("must provide username", 400)
        if not password:
            return apology("must provide password", 400)
        if password != confirmation:
            return apology("passwords do not match", 400)
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return apology("username already exists", 400)
        hash_pw = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash_pw))
        db.commit()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        session["user_id"] = user["id"]
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if not title or not content:
            return apology("Title and content required", 400)
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO articles (user_id, title, content) VALUES (?, ?, ?)",
                (session["user_id"], title, content)
            )
            db.commit()
        except sqlite3.Error as e:
            db.rollback()
            return apology(f"database error: {str(e)}", 400)
        return redirect("/")
    else:
        return render_template("create.html")

@app.route("/article/<int:article_id>")
@login_required
def article(article_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT articles.id, articles.title, articles.content, articles.created_at, users.username AS author
        FROM articles
        JOIN users ON articles.user_id = users.id
        WHERE articles.id = ?
    """, (article_id,))
    row = cursor.fetchone()
    if not row:
        return apology("Article not found", 404)
    article = dict(row)
    if isinstance(article["created_at"], str):
        try:
            article["created_at"] = datetime.strptime(article["created_at"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                article["created_at"] = datetime.strptime(article["created_at"], "%Y-%m-%d %H:%M:%S.%f")
            except Exception:
                pass
    return render_template("article.html", article=article)

@app.route("/my_articles", methods=["GET", "POST"])
@login_required
def my_articles():
    db = get_db()
    cursor = db.cursor()
    if request.method == "POST":
        article_id = request.form.get("article_id")
        # Ensure the article belongs to the user
        cursor.execute("SELECT * FROM articles WHERE id = ? AND user_id = ?", (article_id, session["user_id"]))
        article = cursor.fetchone()
        if article:
            cursor.execute("DELETE FROM articles WHERE id = ?", (article_id,))
            db.commit()
            flash("Article deleted.")
        else:
            flash("You can only delete your own articles.")
        return redirect("/my_articles")
    else:
        cursor.execute("""
            SELECT id, title, created_at
            FROM articles
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (session["user_id"],))
        articles = [dict(row) for row in cursor.fetchall()]
        return render_template("my_articles.html", articles=articles)

if __name__ == "__main__":
    app.run(debug=True)