from flask import Flask # For web server

app = Flask(__name__)

@app.route("/")
def hello_world():
    """Basic Hello World"""

    return "<p>Hello, World!</p>"