import time
import atexit
from flask import Flask, render_template
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

# Shutdown DB on app shutdown
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# Flask route bindings
@app.route('/')
def home():
    return render_template('home.html')

# Running Flask
app.run()