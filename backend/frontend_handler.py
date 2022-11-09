from typing import List
from .attendance import Attendance


class FrontendHandlerInterface:
    def getAllAttendanceIDs(self) -> List[str]:
        pass

    def getAttendanceInfo(self, id: str) -> Attendance:
        pass

    def createAttendance(self, attendanceObject: Attendance) -> None:
        pass

    def updateAttendance(self, attendanceObject: Attendance) -> None:
        pass


class FrontendHandler(FrontendHandlerInterface):
    pass
