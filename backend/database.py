from os import mkdir
import json
import os
from pathlib import Path
from typing import List
from .attendance import Attendance

class DatabaseInterface:
    """
    Interface requirements for creating and updating 
    """

    def createAttendance(self, attendanceObject: Attendance, file_opener = open):
        pass
    
    def updateAttendance(self, attendanceObject: Attendance) -> None:
        pass

    def getAttendanceIDs(self) -> List[str]:
        pass

    def getAttendance(self, id: str) -> Attendance:
        pass


# We implement interfaces here. Avoid having direct implementations in classes marked ...Interfcace
# (though we can implement them as stubs if needed)
class Database(DatabaseInterface):
    ATTENDANCE_DATABASE_PATH = Path("./backend_data/")

    # We can mock dependencies easily in python by adding extra parameters for dependencies
    # Note that we supply the function itself, not the result of a function (e.g., a function call)
    def __init__(self, mkdir=mkdir):
        if not self.ATTENDANCE_DATABASE_PATH.is_dir():
            mkdir(self.ATTENDANCE_DATABASE_PATH)

    def createAttendance(self, attendanceObject: Attendance, open = open):
        full_path_name = str(self.ATTENDANCE_DATABASE_PATH) + attendanceObject.id + ".dat"

        # When opening files, use this approach [with open(...)]
        # This will automatically close the file at the end of the scope
        if (os.path.isfile(full_path_name)):
            return # in future we should send response code that shows that we could not process this request. 


        with open(full_path_name, "w") as f:
            f.write(attendanceObject.json())

    def updateAttendance(self, attendanceObject: Attendance) -> None:
        full_path_name = str(self.ATTENDANCE_DATABASE_PATH) + attendanceObject.id + ".dat"

        if not (os.path.isfile(full_path_name)):
            return # in future we should send response code that shows that we could not process this request. 
        
        # if it doesn't exist I can create the file and store it
        with open(full_path_name, "w") as f:
            f.write(attendanceObject.json())

    def getAttendance(self, id: str) -> Attendance:

        full_path_name = str(self.ATTENDANCE_DATABASE_PATH) + id + ".dat"
        if not (os.path.isfile(full_path_name)):
            return # in future we should send response code that shows that we could not process this request. 
        
        # if it doesn't exist I can create the file and store it
         # if it doesn't exist I can create the file and store it
        with open(full_path_name, "r") as f:
            myDataString = f.read()
            data = json.loads(myDataString)
            attendance = Attendance (id = data["id"], records = data["records"])
            return attendance
