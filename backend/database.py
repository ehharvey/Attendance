import json
import os
from os import mkdir
from pathlib import Path
from typing import List

from .attendance import Attendance


class AttendanceAlreadyExists(Exception):
    """Exception when Attendance item already exists"""
    pass


class AttendanceDoesNotExist(Exception):
    """Exception when Attendance item does not exist (but it should)"""

# We implement interfaces here. Avoid having direct implementations in classes marked ...Interfcace
# (though we can implement them as stubs if needed)


class Database(DatabaseInterface):
    ATTENDANCE_DATABASE_PATH: Path


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

        # When opening files, use this approach [with open(...)]
        # This will automatically close the file at the end of the scope
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
        """Retrieves an existing Attendance item"""

        full_path_name = self.attendance_database_folder / (id + ".json")
        if not (full_path_name.is_file()):
            raise AttendanceDoesNotExist

        # if it doesn't exist I can create the file and store it
        # if it doesn't exist I can create the file and store it
        with full_path_name.open("r") as f:
            myDataString = f.read()
            data = json.loads(myDataString)
            attendance = Attendance(id=data["id"], records=data["records"])
            return attendance
