from flask import Flask, render_template
from board.classes import Board
from database.beginning import init_db, db_session
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

init_db()

board = Board()

def refreshBoard():
    board.update(debug=False)

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(func=refreshBoard, trigger="interval", seconds=1)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

app = Flask(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run()
