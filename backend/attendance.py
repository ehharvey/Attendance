from dataclasses import dataclass
from typing import List


@dataclass
class StudentAttendanceItem:
    studentID: str # Retrieved from classlist module
    isPresent: bool

@dataclass
class Attendance:
    id: str # Retrieve calendar
    records: List[StudentAttendanceItem]