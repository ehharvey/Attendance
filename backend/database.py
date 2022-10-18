from typing import List
from .attendance import Attendance

class DatabaseInterface:
    """
    Provides functionality for creating and updating 
    """
    

    def createAttendance(self, attendanceObject: Attendance) -> None:
        #save the object locally 
        file = open('backend/database/data.dat','a+')
        if file.tell()!=0:  #this is just to make sure that unless we're starting at 0 we should create a new line to read the json
            file.write("\n")
        file.write(attendanceObject.json())
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
