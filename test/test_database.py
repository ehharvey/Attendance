from backend.attendance import Attendance, StudentAttendanceItem
import json

def test_attendance_json():
    """This is to test if the .json() functionality of Attendance object works as expected"""

    #ARRANGE
    student_id1 = StudentAttendanceItem(studentID = "123", isPresent = False)
    student_id2 = StudentAttendanceItem(studentID = "456", isPresent = True)
    my_attendance = Attendance(id="1", records = [student_id1, student_id2])

    _expected = json.dumps({
        "id": "1",
        "records": [
            {
                "studentID": "123",
                "isPresent": False
            },
            {
                "studentID": "456",
                "isPresent": True
            }
        ]
    })

    #ACT
    _actual = my_attendance.json()
    
    #ASSERT
    assert _expected == _actual