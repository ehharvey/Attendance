from flask import Flask # For web server
from flask_cors import CORS
from backend.database import Database
app = Flask(__name__)
cors = CORS(app)
CORS(app)


database: Database = Database()


@app.route("/")
def hello_world():
    """Basic Hello World"""

    return "Attendance Backend says Hello World!"


@app.route("/api/attendance", methods=["GET"])
def getSummaryAttendance():
    """Get Summary List of Attendances"""

    result = database.getSummaryAttendance()

    return {
        "records": result
    }, 200 # tuple, return code