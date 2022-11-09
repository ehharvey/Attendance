from dataclasses import dataclass
from pathlib import Path
from backend.database import Database
from unittest.mock import MagicMock, mock_open, patch


# Mock for Attendance
@dataclass
class AttendanceMock:
    id = "ID"
    _payload = "Hello World"

    def json(self):
        return self._payload


########################


def test_database_init():
    # Arrange
    mock_path = Path()

    with (
        patch.object(Path, 'mkdir') as mkdir_mock,
        patch.object(Path, "is_dir") as is_dir_mock
    ):
        is_dir_mock.return_value = False
        mkdir_mock.return_value = None

        # Act
        database = Database(mock_path)

        # Assert
        is_dir_mock.assert_called_once()
        mkdir_mock.assert_called_once()


def test_database_createAttendance():
    assert True  # TODO
    # m_mkdir = MagicMock(return_value=None)
    # m_open: MagicMock = mock_open()

    # attendance = AttendanceMock()

    # # Arrange
    # database = Database(mkdirFunc=m_mkdir, openFunc=m_open)

    # # Act
    # database.createAttendance(attendanceObject=attendance, open=m_open)

    # # Assert
    # m_open.assert_called_once_with(Path("./backend_data/") / "ID.json", "w")
    # m_open().write.assert_called_once_with("Hello World")
