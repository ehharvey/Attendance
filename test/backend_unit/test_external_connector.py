"""
Unit tests ExternalConnector

Test status:
* All functions tested
* Repeated calls not tested
* 
"""

from Attendance.external_connector import *
import requests
import git
from unittest.mock import MagicMock, mock_open, patch
from pathlib import Path
from requests import Response
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


@patch("Attendance.external_connector.git.Repo.clone_from")
@patch.object(Path, "open", mocked_open)
def test_get_service_json(clone_from_mock):
    # Arrange
    EXPECTED = json.loads(SERVICE_JSON)

    # Act
    actual = ExternalConnector().get_service_json()

    # Assert
    assert actual == EXPECTED
    clone_from_mock.assert_called_once()


@patch.object(
    ExternalConnector, "get_service_json", lambda *args: json.loads(SERVICE_JSON)
)
def test_ExternalConnector_fetch():
    # Arrange
    external_connector = ExternalConnector()

    # Act
    external_connector.fetch()

    # Assert
    assert external_connector.fetched == True
    assert external_connector.services == ServiceContainer(**json.loads(SERVICE_JSON))


def fetch_mock_fn(external_connector: ExternalConnector):
    external_connector.fetched = True
    external_connector.services = ServiceContainer(**json.loads(SERVICE_JSON))


@patch(
    "Attendance.external_connector.requests.get",
    lambda url, timeout: type(
        "Response",
        (object,),
        {"content": json.dumps(ExternalConnectorStub().getCalendar())},
    ),  # Creates a mock response
)
def test_ExternalConnector_getCalendar():
    with patch.object(ExternalConnector, "fetch") as fetch_mock:
        # Arrange
        external_connector = ExternalConnector()
        fetch_mock.side_effect = lambda *args: fetch_mock_fn(external_connector)
        EXPECTED = ExternalConnectorStub().getCalendar()

        # Act
        actual = external_connector.getCalendar()

        # Assert
        assert actual == EXPECTED
        fetch_mock.assert_called_once()


@patch(
    "Attendance.external_connector.requests.get",
    lambda url, timeout: type(
        "Response",
        (object,),
        {"content": json.dumps(ExternalConnectorStub().getClasslist())},
    ),  # Creates a mock response
)
def test_ExternalConnector_getClasslist():
    with patch.object(ExternalConnector, "fetch") as fetch_mock:
        # Arrange
        external_connector = ExternalConnector()
        fetch_mock.side_effect = lambda *args: fetch_mock_fn(external_connector)
        EXPECTED = ExternalConnectorStub().getClasslist()

        # Act
        actual = external_connector.getClasslist()

        # Assert
        assert actual == EXPECTED
        fetch_mock.assert_called_once()


@patch(
    "Attendance.external_connector.requests.get",
    lambda url, timeout: type(
        "Response",
        (object,),
        {"content": json.dumps(ExternalConnectorStub().getClasslist())},
    ),  # Creates a mock response
)
def test_ExternalConnector_getCalendarTwice_FetchOnce():
    with patch.object(ExternalConnector, "fetch") as fetch_mock:
        # Arrange
        external_connector = ExternalConnector()
        fetch_mock.side_effect = lambda *args: fetch_mock_fn(external_connector)

        # Act
        external_connector.getCalendar()
        external_connector.getCalendar()

        # Assert
        fetch_mock.assert_called_once()


@patch(
    "Attendance.external_connector.requests.get",
    lambda url, timeout: type(
        "Response",
        (object,),
        {"content": json.dumps(ExternalConnectorStub().getClasslist())},
    ),  # Creates a mock response
)
def test_ExternalConnector_getClasslistTwice_FetchOnce():
    with patch.object(ExternalConnector, "fetch") as fetch_mock:
        # Arrange
        external_connector = ExternalConnector()
        fetch_mock.side_effect = lambda *args: fetch_mock_fn(external_connector)

        # Act
        external_connector.getClasslist()
        external_connector.getClasslist()

        # Assert
        fetch_mock.assert_called_once()
