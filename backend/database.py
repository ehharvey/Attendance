import json
from pathlib import Path
from pydantic import ValidationError

from .attendance import Attendance


class AttendanceAlreadyExists(Exception):
    """Exception when Attendance item already exists"""


class AttendanceDoesNotExist(Exception):
    """Exception when Attendance item does not exist (but it should)"""


class AttendanceIsMalformed(Exception):
    """Exception when read Attendance data is malformed"""


class Database:
    """A Database to store Attendances"""

    attendance_database_folder: Path

    def __init__(
        self,
        database_folder: Path = Path("./backend_data/"),
    ):
        # Set dependencies here
        self.attendance_database_folder = database_folder

        # If attendance path is not a dir, make it one
        if not self.attendance_database_folder.is_dir():
            self.attendance_database_folder.mkdir()

    def create_attendance(self, attendance: Attendance):
        """
        Creates a new attendance item. Raises AttendanceAlreadyExists if the item already exists

        To update an already existing attendance item, use update_attendance
        """

        full_path_name = self.attendance_database_folder / \
            (attendance.id + ".json")

        if (full_path_name.is_file()):
            raise AttendanceAlreadyExists

        with full_path_name.open("w") as f:
            f.write(attendance.json())

    def update_attendance(self, attendance: Attendance) -> None:
        """
        Updates an *existing* Attendance item with a new one
        """

        full_path_name = self.attendance_database_folder / \
            (attendance.id + ".json")

        if not (full_path_name.is_file()):
            raise AttendanceDoesNotExist

        # if it doesn't exist I can create the file and store it
        with full_path_name.open("w") as f:
            f.write(attendance.json())

    def get_attendance(self, id: str) -> Attendance:
        """
        Retrieves an existing Attendance item

        Raises AttendanceDoesNotExist if supplied id does not match any stored attendances

        Raises AttendanceIsMalformed is read Attendance is malformed
        """

        full_path_name = self.attendance_database_folder / (id + ".json")
        if not (full_path_name.is_file()):
            raise AttendanceDoesNotExist

        with full_path_name.open("r") as f:
            file_text = f.read()
            parsed_json = json.loads(file_text)

            if not isinstance(parsed_json, dict):
                raise AttendanceIsMalformed

            try:
                attendance = Attendance(
                    id=parsed_json["id"], records=parsed_json["records"])
            except ValidationError as exc:
                raise AttendanceIsMalformed from exc

            return attendance
