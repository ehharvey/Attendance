from dataclasses import dataclass
from typing import List
from pydantic import BaseModel


class StudentAttendanceItem(BaseModel):
    studentID: str # Retrieved from classlist module
    isPresent: bool


class Attendance(BaseModel):
    id: str # Retrieve calendar
    records: List[StudentAttendanceItem]