from pathlib import Path
from typing import Dict
from flask import Flask  # For web server
from flask import request, send_from_directory, send_file
from flask_cors import CORS, cross_origin
from backend.database import Database
import json

from pydantic import BaseModel
from backend.database import AttendanceAlreadyExists
from backend.attendance import Attendance
import requests

app = Flask(__name__)
cors = CORS(app)
CORS(app)

db = Database()

SERVICES_JSON = Path("./services.json")


def get_services() -> Dict[str, dict]:
    with SERVICES_JSON.open("r") as f:
        return json.load(f)


class Service(BaseModel):
    ip: str
    port: str


SERVICES = {key: Service(**value) for key, value in get_services().items()}

CALENDAR_SERVICE = SERVICES.get("calendar")
CLASSLIST_SERVICE = SERVICES.get("classlist")

SERVICE_TIMEOUT = 3  # seconds before we quit trying to communicate with others


@app.route("/test")
def hello_world():
    return send_file("./frontend/test.html")


@app.route("/")
def teacher_view():
    return send_file("./frontend/teacher-view.html")


@app.route("/images/<path:path>")
def send_image(path: Path):
    return send_from_directory("./frontend/images", path)


@app.route("/scripts/<path:path>")
def send_script(path: Path):
    return send_from_directory("./frontend/scripts", path)


@app.route("/style/<path:path>")
def send_style(path: Path):
    return send_from_directory("./frontend/style", path)


@app.route("/api/attendance", methods=["GET"])
def getSummaryAttendance():
    """Get Summary List of Attendances"""

    result = db.get_summary_attendance()

    return {"ids": result}, 200  # tuple, return code


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


@app.route("/api/classlist", methods=["GET"])
def getClasslist():

    try:
        response = requests.get(
            f"http://{CLASSLIST_SERVICE.ip}:{CLASSLIST_SERVICE.port}/students",
            timeout=3,
        )

        return response.content, 200

    except Exception as e:
        return str(e), 500


@app.route("/api/calendar", methods=["GET"])
def getCalendar():

    try:
        response = requests.get(
            f"http://{CALENDAR_SERVICE.ip}:{CALENDAR_SERVICE.port}/event", timeout=3
        )
        # if response.status_code == 200:
        # return "Successfully found the classlist", 200
    except Exception as e:
        return str(e), 500
