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
    """Tests constructor"""

    # Arrange
    mock_database_directory = Path()

    # This mocks the mock_database_directory
    with (
        patch.object(Path, "mkdir") as mkdir_mock,
        patch.object(Path, "is_dir") as is_dir_mock,
    ):
        is_dir_mock.return_value = False
        mkdir_mock.return_value = None

        # Act
        database = Database(mock_database_directory)

        # Assert
        is_dir_mock.assert_called_once()
        mkdir_mock.assert_called_once()


def test_database_create_attendance():
    """
    Tests create_attendance

    Constructor mocks: no issue

    database file: does not exist
    """

    # Arrange
    mock_database_directory = Path()
    attendance_mock = AttendanceMock()

    # This mocks the mock_database_directory
    with (
        patch.object(Path, "mkdir") as mkdir_mock,
        patch.object(Path, "is_dir") as is_dir_mock,
        # Used by create_attendance to derive new paths
        patch.object(Path, "__truediv__") as divide_mock,
    ):
        is_dir_mock.return_value = False
        mkdir_mock.return_value = None

        # Mock the database file itself
        database_file_mock = Path()
        open_mock = mock_open()

        # attendance_database_folder / "ID.json" = database_file_mock
        divide_mock.return_value = database_file_mock

        with (
            patch.object(Path, "is_file") as is_file_mock,
            patch.object(Path, "open", open_mock),
        ):
            is_file_mock.return_value = False

            # Act
            database = Database(mock_database_directory)
            database.create_attendance(attendance_mock)

            # Assert
            is_dir_mock.assert_called_once()
            mkdir_mock.assert_called_once()
            open_mock.assert_called_once_with("w")
