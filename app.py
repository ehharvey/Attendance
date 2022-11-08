from flask import Flask, request # For web server
from backend.attendance import Attendance
from backend.database import Database
from pydantic import ValidationError
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app)
CORS(app)

database: Database = Database()


@app.route("/")
def hello_world():
    """Basic Hello World"""

    return "Attendance Backend says Hello World!"


@app.route("/api/attendance", methods=["POST"])
def postAttendance():
    try:
        attendance = Attendance(**request.json) # request.json raises 400 if no json body

        database.createAttendance(attendance)

        return {
            "id": attendance.id
        }, 201 # Return a tuple of body, return code

    except ValidationError as e:
        return e.json(), 400 # Return a tuple of body, return code
