from os import mkdir
from pathlib import Path
from typing import List
from .attendance import Attendance

class DatabaseInterface:
    """
    Interface functionality for creating and updating 
    """
    

    # REMOVE WHEN ABLE: Interfaces should not receive implementations ##################################

    # def createAttendance(self, attendanceObject: Attendance) -> None:

    #     #save the object locally 
    #     file = open('backend/database/data.dat','a+')
    #     if file.tell()!=0:  #this is just to make sure that unless we're starting at 0 we should create a new line to read the json
    #         file.write("\n")
    #     file.write(attendanceObject.json())
    #     pass

    ####################################################################################################

    def createAttendance(self, attendanceObject: Attendance, file_opener = open):
        pass
    
    def updateAttendance(self, attendanceObject: Attendance) -> None:
        pass

    def getAttendanceIDs(self) -> List[str]:
        pass

    def getAttendance(self, id: str) -> Attendance:
        pass


class Database(DatabaseInterface):
    ATTENDANCE_DATABASE_PATH = Path("./backend_data/")

    # We can mock dependencies easily in python by adding extra parameters for dependencies
    # Note that we supply the function itself, not the result of a function (e.g., a function call)
    def __init__(self, mkdir=mkdir):
        if not self.ATTENDANCE_DATABASE_PATH.is_dir():
            mkdir(self.ATTENDANCE_DATABASE_PATH)

    def createAttendance(self, attendanceObject: Attendance, open = open):
        file_name = attendanceObject.id

        # When opening files, use this approach [with open(...)]
        # This will automatically close the file at the end of the scope
        with open(self.ATTENDANCE_DATABASE_PATH / file_name, "w") as f:
            f.write(attendanceObject.json())
