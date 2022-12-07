import os

from Attendance.config import Config
from Attendance.database import (
    AttendanceAlreadyExists,
    AttendanceDoesNotExist,
    AttendanceIsMalformed,
)
from Attendance.database_s3 import DatabaseS3
from Attendance.attendance import Attendance, StudentAttendanceItem

import pytest

CONFIG = Config(**os.environ)


@pytest.fixture()
def database_s3() -> DatabaseS3:
    result = DatabaseS3(
        s3_region=CONFIG.S3_REGION,
        s3_url=CONFIG.S3_URL,
        s3_key_id=CONFIG.S3_KEY_ID,
        s3_key_secret=CONFIG.S3_KEY_SECRET,
        s3_bucket=CONFIG.S3_BUCKET,
    )

    for key in result.get_summary_attendance():
        result.client.delete_object(Bucket=result.s3_bucket, Key=key)

    return result


class TestDatabaseS3:
    def test_list_files_empty(self, database_s3: DatabaseS3):
        # Arrange
        EXPECTED = []

        # Act
        actual = database_s3.list_files()

        # Arrange
        assert EXPECTED == actual

    def test_create_get_empty_attendance(self, database_s3: DatabaseS3):
        # Arrange
        EXPECTED = Attendance(id="test", records=[])

        # Act
        database_s3.create_attendance(EXPECTED)

        # Assert
        actual = database_s3.get_attendance(EXPECTED.id)

        assert actual == EXPECTED

    def test_create_twice(self, database_s3: DatabaseS3):
        # Arrange
        attendance = Attendance(id="test", records=[])

        # Act
        database_s3.create_attendance(attendance)

        with pytest.raises(AttendanceAlreadyExists):
            database_s3.create_attendance(attendance)

    def test_create_update(self, database_s3: DatabaseS3):
        # Arrange
        a_1 = Attendance(
            id="Foo", records=[StudentAttendanceItem(studentID="s1", isPresent=True)]
        )
        a_2 = Attendance(
            id=a_1.id, records=[StudentAttendanceItem(studentID="s2", isPresent=False)]
        )

        # Act/Assert
        database_s3.create_attendance(a_1)
        assert database_s3.get_attendance(a_1.id) == a_1

        database_s3.update_attendance(a_2)
        assert database_s3.get_attendance(a_2.id) == a_2
