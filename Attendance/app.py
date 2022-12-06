import json
import os.path
from pathlib import Path
from typing import Dict
import requests
import yaml
from flask import Flask  # For web server
from flask import request, send_file, send_from_directory
from flask_cors import CORS, cross_origin
from pydantic import BaseModel

from Attendance.attendance import Attendance
from Attendance.database import AttendanceAlreadyExists, Database
from Attendance.external_connector import ExternalConnector, ExternalConnectorStub

# APP Initialization ################
app = Flask(__name__)
cors = CORS(app)
CORS(app)

CONFIG_FILE = Path("attendance_config.yaml")

if CONFIG_FILE.is_file():
    with CONFIG_FILE.open(mode="r", encoding="utf-8") as f:
        app.config.update(**yaml.safe_load(f))
else:
    app.config.update(**{"debug": False})

DB = Database()

if not app.config.get("debug", False):
    app.config["services"]: ExternalConnector = ExternalConnector()
else:
    app.config["services"]: ExternalConnector = ExternalConnectorStub()

STATIC_DIRECTORY = Path(os.path.dirname(__file__)) / "static"
##################################


@app.route("/test")
def test_view():
    return send_file(STATIC_DIRECTORY / "test.html")


@app.route("/")
def teacher_view():
    response = app.config["services"].getModeOfOperation()
    value = response["modeofoperation"]
    if value == True:
        return send_file(STATIC_DIRECTORY / "teacher-view.html")
    else:
        return send_file(STATIC_DIRECTORY / "student-view.html")


@app.route("/images/<path:path>")
def send_image(path: Path):
    return send_from_directory(STATIC_DIRECTORY / "images", path)


@app.route("/scripts/<path:path>")
def send_script(path: Path):
    return send_from_directory(STATIC_DIRECTORY / "scripts", path)


@app.route("/style/<path:path>")
def send_style(path: Path):
    return send_from_directory(STATIC_DIRECTORY / "style", path)


@app.route("/api/attendance", methods=["GET"])
def get_summary_attendance():
    """Get Summary List of Attendances"""

    result = DB.get_summary_attendance()

    return {"ids": result}, 200  # tuple, return code


@app.route("/api/attendance/<string:attendance_id>", methods=["GET", "POST"])
def api_attendance(attendance_id):
    if request.method == "GET":
        val = DB.get_attendance(attendance_id)
        return val.json()
    if request.method == "POST":
        request_json = request.get_json()
        attendance_object = Attendance(
            id=request_json.get("id"), records=request_json.get("records")
        )
        try:
            DB.create_attendance(attendance_object)
        except AttendanceAlreadyExists:
            return "Attendance Item already exists", 400

        return "Successfully added attendance item", 201


@app.route("/api/classlist", methods=["GET"])
def get_classlist():

    try:
        response = app.config["services"].getClasslist()

        return response, 200

    except Exception as e:
        return str(e), 500


@app.route("/api/calendar", methods=["GET"])
def get_calendar():

    try:
        response = app.config["services"].getCalendar()

        return response, 200

    except Exception as e:
        return str(e), 500
