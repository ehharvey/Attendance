#! /bin/bash

(python3 -m http.server -d ./frontend/ 27501 > ./deployment/http.server.logs) \
& \
(flask run --host=0.0.0.0 > ./deployment/flask.logs) 