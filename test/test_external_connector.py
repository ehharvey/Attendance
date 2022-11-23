from backend.external_connector import *
import requests
import git
from unittest.mock import MagicMock, mock_open, patch
from pathlib import Path
import json

SERVICE_JSON = """
{
  "assignments": {
    "ip": "10.192.218.86",
    "port": 8080
  },
  "attendance": {
    "ip": "10.192.218.63",
    "port": 8080
  },
  "calendar": {
    "ip": "10.192.218.137",
    "port": 8080
  },
  "classlist": {
    "ip": "10.192.218.57",
    "port": 8080
  },
  "grades": {
    "ip": "10.192.84.251",
    "port": 8080
  },
  "groups": {
    "ip": "10.192.82.212",
    "port": 8080
  },
  "rubrics": {
    "ip": "10.192.0.0",
    "port": 8080
  },
  "quizzes": {
    "ip": "10.192.229.5",
    "port": 8080
  },
  "surveys": {
    "ip": "10.192.218.242",
    "port": 8080
  },
  "adminactivities": {
    "ip": "10.192.85.105",
    "port": 8080
  }
}
"""

mocked_open = mock_open(read_data=SERVICE_JSON)


@patch("backend.external_connector.git.Repo.clone_from")
@patch.object(Path, "open", mocked_open)
def test_get_service_json(mocked_function):
    actual = get_service_json()
    EXPECTED = json.loads(SERVICE_JSON)

    assert actual == EXPECTED

