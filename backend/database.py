from typing import List
from .attendance import Attendance

class DatabaseInterface:
    """
    Provides functionality for creating and updating 
    """

    def createAttendance(self, attendanceObject: Attendance) -> None:
        pass
    
    def updateAttendance(self, attendanceObject: Attendance) -> None:
        pass

    def getAttendanceIDs(self) -> List[str]:
        pass

    def getAttendance(self, id: str) -> Attendance:
        pass


class Database(DatabaseInterface):

    def createAttendance(self, attendanceObject: Attendance):
        return super().createAttendance(attendanceObject)
