from flask import Flask  # For web server
from flask import request
from flask_cors import CORS, cross_origin
from backend.database import Database

from backend.database import AttendanceAlreadyExists
from backend.attendance import Attendance


app = Flask(__name__)
cors = CORS(app)
CORS(app)

db = Database()


@app.route("/")
def hello_world():
    """Basic Hello World"""

    return "Attendance Backend says Hello World!"


@app.route("/api/attendance", methods=["GET"])
def getSummaryAttendance():
    """Get Summary List of Attendances"""

    result = db.get_summary_attendance()

    return {"records": result}, 200  # tuple, return code


@app.route("/api/attendance/<int:attendance_id>", methods=["GET", "POST"])
def attendance(attendance_id):
    if request.method == "GET":
        val = db.get_attendance(attendance_id)
        return val
    if request.method == "POST":
        request_json = request.get_json()
        attendance_object = Attendance(
            id=request_json.get("id"), records=[request_json.get("records")]
        )
        try:
            db.create_attendance(attendance_object)
        except AttendanceAlreadyExists:
            return "Attendance Item already exists"

        return "Successfully added attendance item"
