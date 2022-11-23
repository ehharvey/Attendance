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
from backend.external_connector import ExternalConnector, ExternalConnectorStub
import requests
import yaml


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
##################################


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

    result = DB.get_summary_attendance()

    return {"ids": result}, 200  # tuple, return code


@app.route("/api/attendance/<int:attendance_id>", methods=["GET", "POST"])
def attendance(attendance_id):
    if request.method == "GET":
        val = DB.get_attendance(attendance_id)
        return val
    if request.method == "POST":
        request_json = request.get_json()
        attendance_object = Attendance(
            id=request_json.get("id"), records=[request_json.get("records")]
        )
        try:
            DB.create_attendance(attendance_object)
        except AttendanceAlreadyExists:
            return "Attendance Item already exists"

        return "Successfully added attendance item"


@app.route("/api/classlist", methods=["GET"])
def getClasslist():

    try:
        response = app.config["services"].getClasslist()

        return response, 200

    except Exception as e:
        return str(e), 500


@app.route("/api/calendar", methods=["GET"])
def getCalendar():

    try:
        response = app.config["services"].getCalendar()

        return response, 200

    except Exception as e:
        return str(e), 500
