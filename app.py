from flask import Flask  # For web server
from flask_cors import CORS, cross_origin
from backend.database import Database

app = Flask(__name__)
cors = CORS(app)
CORS(app)

db = Database()


@app.route("/")
def hello_world():
    """Basic Hello World"""

    return "Attendance Backend says Hello World!"


@app.route("/api/attendance/<int:attendance_id>")
def attendance(attendance_id):

    try:
        val = db.get_attendance(attendance_id)
    except:
        return "<h2>404 Not Found<h2>"

    return val
