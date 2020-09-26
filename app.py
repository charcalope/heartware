import time
import atexit
import os
from flask import Flask, render_template, session, url_for, request, redirect
from markupsafe import escape
from board.classes import Board
from database.beginning import init_db, db_session
from database.utils import customer_login as db_customer_login
from apscheduler.schedulers.background import BackgroundScheduler

# Initialize database and board
init_db()
board = Board()

# Initialize scheduler and register job(s)
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(func=(lambda: board.update(debug=False)), trigger="interval", seconds=1)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

# Initialize Flask
app = Flask(__name__)
## CHANGE IN PROD
app.secret_key = os.urandom(24)

# Shutdown DB on app shutdown
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# Flask route bindings
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/customer/login', methods=["GET", "POST"])
def customer_login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        username = request.form["username"]
        password = request.form["password"]
        if db_customer_login(username, password):
            session["username"] = username
            session["password"] = password
            return redirect(url_for('customer_cart'))
        else:
            return render_template('customer_login.html', error=True)
    return render_template('customer_login.html')

@app.route('/customer/cart')
def customer_cart():
    return render_template('cart.html')

## DEBUG
@app.route('/logged/in')
def logged_in():
    if 'username' in session and 'password' in session:
        return "Logged in as %s" % escape(session['username'])
    return "Not logged in!"

# Running Flask
if __name__ == "__main__":
    app.run()