from flask import Flask # For web server
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
CORS(app)


@app.route("/")
def hello_world():
    """Basic Hello World"""

    return "Attendance Backend says Hello World!"