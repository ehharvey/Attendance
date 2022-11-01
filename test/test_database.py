from dataclasses import dataclass
from pathlib import Path
from backend.database import Database
from unittest.mock import MagicMock, mock_open


# Mock for Attendance
@dataclass
class AttendanceMock:
    id = "ID"
    _payload = "Hello World"

    def json(self):
        return self._payload
########################


def test_database_init():
    m_mkdir = MagicMock(return_value = None)

    # Arrange
    database = Database(mkdir = m_mkdir)

    # Assert
    m_mkdir.assert_called_once_with(Path("./backend_data/"))


def test_database_createAttendance():
    m_mkdir = MagicMock(return_value = None)
    m_open: MagicMock = mock_open()


    attendance = AttendanceMock()

    # Arrange
    database = Database(mkdir=m_mkdir)

    # Act
    database.createAttendance(attendanceObject=attendance, open = m_open)

    # Assert
    m_open.assert_called_once_with(Path("./backend_data/") / "ID.json", "w")
    m_open().write.assert_called_once_with("Hello World")
