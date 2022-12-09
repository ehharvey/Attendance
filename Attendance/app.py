import json
import os.path
import os
from pathlib import Path
from typing import Dict
import requests
import yaml
from flask import Flask  # For web server
from flask import request, send_file, send_from_directory
from flask_cors import CORS, cross_origin
from pydantic import BaseModel

from Attendance.attendance import Attendance
from Attendance.config import Config
from Attendance.database import (
    AttendanceAlreadyExists,
    Database,
    AttendanceDoesNotExist,
)
from Attendance.database_s3 import DatabaseS3
from Attendance.external_connector import ExternalConnector, ExternalConnectorStub

# APP Initialization ################
app = Flask(__name__)
cors = CORS(app)
CORS(app)

# This app is configured by environmental variables:
#
# S3 configuration
# S3_REGION: Location of S3 bucket
# S3_URL: URL of S3 Bucket
# S3_KEY_ID: Key ID to access S3 Bucket
# S3_KEY_SECRET: Secret for Key ID
# S3_BUCKET: Bucket name to use for storage. If does not exist, will create
#
# If no S3 environmental variables are set, resorts to file-based DB
# If only some S3 environmental variables are set, raises an error
#
# External Service Config
# SERVICE_REPO: link to repo containing json file
# SERVICE_FILE: name of json file
#
# If not all SERVICE environmental variables are set, raises an error
CONFIG = Config(**os.environ)
DB: Database
CONNECTOR: ExternalConnector

if CONFIG.SERVICE_REPO != "DEBUG":
    CONNECTOR: ExternalConnector = ExternalConnector(
        CONFIG.SERVICE_REPO, CONFIG.SERVICE_FILE
    )
else:
    CONNECTOR: ExternalConnector = ExternalConnectorStub()


if CONFIG.S3_REGION:
    DB = DatabaseS3(
        s3_region=CONFIG.S3_REGION,
        s3_url=CONFIG.S3_URL,
        s3_key_id=CONFIG.S3_KEY_ID,
        s3_key_secret=CONFIG.S3_KEY_SECRET,
        s3_bucket=CONFIG.S3_BUCKET,
    )
else:
    DB = Database()


STATIC_DIRECTORY = Path(os.path.dirname(__file__)) / "static"
##################################


@app.route("/test")
def test_view():
    return send_file(STATIC_DIRECTORY / "test.html")


@app.route("/")
def teacher_view():
    response = CONNECTOR.getModeOfOperation()
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


@app.route("/api/attendance/<string:attendance_id>", methods=["GET", "PUT", "POST"])
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

    if request.method == "PUT":
        request_json = request.get_json()
        attendance_object = Attendance(
            id=request_json.get("id"), records=request_json.get("records")
        )

        try:
            DB.update_attendance(attendance_object)
            return "ok", 201

        except AttendanceDoesNotExist:
            try:
                DB.create_attendance(attendance_object)
                return "ok", 201
            except AttendanceAlreadyExists:
                return "Internal Server Error", 500  # We should never reach here


@app.route("/api/classlist", methods=["GET"])
def get_classlist():

    try:
        response = CONNECTOR.getClasslist()

        return response, 200

    except Exception as e:
        return str(e), 500


@app.route("/api/calendar", methods=["GET"])
def get_calendar():

    try:
        response = CONNECTOR.getCalendar()

        return response, 200

    except Exception as e:
        return str(e), 500


@app.route("/favicon.ico")
def get_favicon():
    return send_file("static/images/favicon.ico")


@app.route("/api/home_url")
def get_home_url():
    return {
        "url": f"{CONNECTOR.services.adminactivities.ip}:{CONNECTOR.services.adminactivities.port}"
    }


@app.route("/healthcheck")
def get_health():
    return "ok", 200


@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response
