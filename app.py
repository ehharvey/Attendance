from pathlib import Path
from flask import Flask  # For web server
from flask import request, send_from_directory, send_file
from flask_cors import CORS, cross_origin
from backend.database import Database
import json

from backend.database import AttendanceAlreadyExists
from backend.attendance import Attendance
import requests

app = Flask(__name__)
cors = CORS(app)
CORS(app)

db = Database()

SERVICES_JSON = Path("./services.json")


def get_services() -> dict:
    with SERVICES_JSON.open("r") as f:
        return json.load(f)


SERVICES = get_services()


def get_services_url(theService: str, theRoute: str) -> str:
    return str(
        SERVICES[theService]["ip"]
        + ":"
        + str(SERVICES[theService]["port"])
        + "/"
        + theRoute
    )


@app.route("/")
def hello_world():
    return send_file("./frontend/index.html")


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


@app.route("/api/attendance/getClasslist", methods=["GET"])
def getClasslist():
    myClasslistURL = get_services_url("classlist", "api/attendance/returnClasslist")
    
    response = requests.get(myClasslistURL)
    response.encoding = "utf-8"  # Optional: requests infers this internally

    return {
        "response_status_code": response.status_code,
        "response": response.json(),
        "myClasslistURL": myClasslistURL,
    }, response.status_code


@app.route("/api/attendance/getCalendar", methods=["GET"])
def getCalendar():
    myCalendarURL = get_services_url("calendar", "event")

    response = requests.get(myCalendarURL)
    response.encoding = "utf-8"  # Optional: requests infers this internally

    # if response.status_code == 200:
    # return "Successfully found the classlist", 200

    return {
        "response_status_code": response.status_code,
        "response": response.json(),
        "myClasslistURL": myCalendarURL,
    }, response.status_code
