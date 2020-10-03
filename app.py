import time
import atexit
import os
import database.utils as db
from flask import Flask, render_template, session, url_for, request, redirect
from markupsafe import escape
from board.classes import Board
from database.beginning import init_db, db_session
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
    db.invalidate_all_customer_tokens()
    db_session.remove()

# Flask route bindings
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/customer/login', methods=["GET", "POST"])
def customer_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if db.customer_login(username, password):
            token = db.generate_customer_token(username)
            session["username"] = username
            session["token"] = token
            session["logged_in"] = True
            return redirect(url_for('customer_cart'))
        else:
            return render_template('customer_login.html', error=True)
    return render_template('customer_login.html')

@app.route('/customer/logout', methods=["POST"])
def customer_logout():
    username = escape(session["username"])
    db.invalidate_customer_token(username)
    del session["username"]
    del session["token"]
    session["logged_in"] = False 

@app.route('/customer/cart')
def customer_cart():
    return render_template('cart.html')

## DEBUG
@app.route('/logged/in')
def logged_in():
    if 'username' in session and 'token' in session:
        return '''<p><strong>Logged in as: </strong>{}</p>
        <p><strong>Session Token:</strong> {}</p>'''.format(escape(session["username"]), escape(session["token"]))
    return "Not logged in!"

# Running Flask
if __name__ == "__main__":
    app.run()