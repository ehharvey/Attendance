import io
from Attendance.database_s3 import DatabaseS3
from Attendance.database import (
    AttendanceAlreadyExists,
    AttendanceDoesNotExist,
    AttendanceIsMalformed,
)
from Attendance.attendance import Attendance, StudentAttendanceItem

from botocore.response import StreamingBody
from boto3 import session
from botocore.client import Config
from botocore.stub import Stubber

from unittest.mock import MagicMock, patch

import pytest

STUB_INIT_PARAMETERS = {
    "s3_region": "",
    "s3_url": "",
    "s3_key_id": "",
    "s3_key_secret": "",
}

STUB_INIT_PARAMETERS_BUCKET_FOO = {**STUB_INIT_PARAMETERS, "s3_bucket": "foo"}


@pytest.fixture()
def client_stubber_tuple():
    client = session.Session().client("s3")
    stubber = Stubber(client)

    client_generator = lambda *args, **kwargs: client

    return client, stubber, client_generator


@pytest.fixture()
def client_stubber_initialized_tuple():
    client = session.Session().client("s3")
    stubber = Stubber(client)

    client_generator = lambda *args, **kwargs: client

    list_buckets_response = {
        "Owner": {"DisplayName": "name", "ID": "EXAMPLE123"},
        "Buckets": [
            {
                "CreationDate": "2016-05-25T16:55:48.000Z",
                "Name": "projectvattendance",
            }
        ],
    }

    stubber.add_response("list_buckets", list_buckets_response, {})

    return client, stubber, client_generator


class TestConfig:
    def test_init_not_present(self, client_stubber_tuple):
        client, stubber, client_generator = client_stubber_tuple

        list_buckets_response = {
            "Owner": {"DisplayName": "name", "ID": "EXAMPLE123"},
            "Buckets": [{"CreationDate": "2016-05-25T16:55:48.000Z", "Name": "foo"}],
        }

        stubber.add_response("list_buckets", list_buckets_response, {})
        stubber.add_response("create_bucket", {}, {"Bucket": "projectvattendance"})

        with stubber:
            with patch.object(session.Session, "client", client_generator):
                db = DatabaseS3(**STUB_INIT_PARAMETERS)

    def test_init_already_exists(self, client_stubber_tuple):
        client, stubber, client_generator = client_stubber_tuple

        list_buckets_response = {
            "Owner": {"DisplayName": "name", "ID": "EXAMPLE123"},
            "Buckets": [
                {
                    "CreationDate": "2016-05-25T16:55:48.000Z",
                    "Name": "projectvattendance",
                }
            ],
        }

        stubber.add_response("list_buckets", list_buckets_response, {})

        with stubber:
            with patch.object(session.Session, "client", client_generator):
                db = DatabaseS3(**STUB_INIT_PARAMETERS)

    def test_list_files_empty(self, client_stubber_initialized_tuple):
        client, stubber, client_generator = client_stubber_initialized_tuple

        list_objects_response = {}
        list_objects_parameters = {"Bucket": "projectvattendance"}

        stubber.add_response(
            "list_objects", list_objects_response, list_objects_parameters
        )

        with stubber:
            with patch.object(session.Session, "client", client_generator):
                db = DatabaseS3(**STUB_INIT_PARAMETERS)

                files = db.list_files()

                assert files == []

    def test_list_files_one_file(self, client_stubber_initialized_tuple):
        client, stubber, client_generator = client_stubber_initialized_tuple

        list_objects_response = {"Contents": [{"Key": "FooBar"}]}
        list_objects_parameters = {"Bucket": "projectvattendance"}

        stubber.add_response(
            "list_objects", list_objects_response, list_objects_parameters
        )

        with stubber:
            with patch.object(session.Session, "client", client_generator):
                db = DatabaseS3(**STUB_INIT_PARAMETERS)

                files = db.list_files()

                assert files == ["FooBar"]

    def test_create_attendance_already_exists(self, client_stubber_initialized_tuple):
        client, stubber, client_generator = client_stubber_initialized_tuple

        list_objects_response = {"Contents": [{"Key": "FooBar"}]}
        list_objects_parameters = {"Bucket": "projectvattendance"}

        stubber.add_response(
            "list_objects", list_objects_response, list_objects_parameters
        )

        with stubber:
            with patch.object(session.Session, "client", client_generator):
                should_not_create = Attendance(id="FooBar", records=[])
                db = DatabaseS3(**STUB_INIT_PARAMETERS)

                with pytest.raises(AttendanceAlreadyExists):
                    db.create_attendance(should_not_create)

    def test_create_attendance_does_not_exist(self, client_stubber_initialized_tuple):
        client, stubber, client_generator = client_stubber_initialized_tuple

        list_objects_response = {"Contents": [{"Key": "FooBar1"}]}
        list_objects_parameters = {"Bucket": "projectvattendance"}

        should_be_created = Attendance(
            id="FooBar",
            records=[StudentAttendanceItem(studentID="student0", isPresent=True)],
        )

        stubber.add_response(
            "list_objects", list_objects_response, list_objects_parameters
        )

        stubber.add_response(
            "put_object",
            {},
            {
                "Bucket": "projectvattendance",
                "Key": should_be_created.id,
                "Body": should_be_created.json(),
                "ACL": "private",
            },
        )

        with stubber:
            with patch.object(session.Session, "client", client_generator):
                db = DatabaseS3(**STUB_INIT_PARAMETERS)

                db.create_attendance(should_be_created)

    def test_update_attendance_does_not_exist(self, client_stubber_initialized_tuple):
        client, stubber, client_generator = client_stubber_initialized_tuple

        list_objects_response = {"Contents": [{"Key": "FooBar1"}]}
        list_objects_parameters = {"Bucket": "projectvattendance"}

        cant_be_updated = Attendance(
            id="FooBar",
            records=[StudentAttendanceItem(studentID="student0", isPresent=True)],
        )

        stubber.add_response(
            "list_objects", list_objects_response, list_objects_parameters
        )

        with stubber:
            with patch.object(session.Session, "client", client_generator):
                db = DatabaseS3(**STUB_INIT_PARAMETERS)

                with pytest.raises(AttendanceDoesNotExist):
                    db.update_attendance(cant_be_updated)

    def test_update_attendance_does_exist(self, client_stubber_initialized_tuple):
        client, stubber, client_generator = client_stubber_initialized_tuple

        list_objects_response = {"Contents": [{"Key": "FooBar"}]}
        list_objects_parameters = {"Bucket": "projectvattendance"}

        can_be_updated = Attendance(
            id="FooBar",
            records=[StudentAttendanceItem(studentID="student0", isPresent=True)],
        )

        stubber.add_response(
            "list_objects", list_objects_response, list_objects_parameters
        )

        stubber.add_response(
            "put_object",
            {},
            {
                "Bucket": "projectvattendance",
                "Key": can_be_updated.id,
                "Body": can_be_updated.json(),
                "ACL": "private",
            },
        )

        with stubber:
            with patch.object(session.Session, "client", client_generator):
                db = DatabaseS3(**STUB_INIT_PARAMETERS)

                db.update_attendance(can_be_updated)

    def test_get_attendance_does_not_exist(self, client_stubber_initialized_tuple):
        client, stubber, client_generator = client_stubber_initialized_tuple

        list_objects_response = {"Contents": [{"Key": "FooBar1"}]}
        list_objects_parameters = {"Bucket": "projectvattendance"}

        should_not_be_retrieved = Attendance(
            id="FooBar",
            records=[StudentAttendanceItem(studentID="student0", isPresent=True)],
        )

        stubber.add_response(
            "list_objects", list_objects_response, list_objects_parameters
        )

        with stubber:
            with patch.object(session.Session, "client", client_generator):
                db = DatabaseS3(**STUB_INIT_PARAMETERS)

                with pytest.raises(AttendanceDoesNotExist):
                    db.get_attendance(should_not_be_retrieved.id)

    def test_get_attendance_does_exist(self, client_stubber_initialized_tuple):
        client, stubber, client_generator = client_stubber_initialized_tuple

        list_objects_response = {"Contents": [{"Key": "FooBar"}]}
        list_objects_parameters = {"Bucket": "projectvattendance"}

        EXPECTED = Attendance(
            id="FooBar",
            records=[StudentAttendanceItem(studentID="student0", isPresent=True)],
        )

        stubber.add_response(
            "list_objects", list_objects_response, list_objects_parameters
        )

        get_body_stream = StreamingBody(
            io.StringIO(EXPECTED.json()), len(EXPECTED.json())
        )

        get_object_response = {"Body": get_body_stream}
        get_object_parameters = {
            "Bucket": "projectvattendance",
            "Key": EXPECTED.id,
        }

        stubber.add_response("get_object", get_object_response, get_object_parameters)

        with stubber:
            with patch.object(session.Session, "client", client_generator):
                db = DatabaseS3(**STUB_INIT_PARAMETERS)

                actual = db.get_attendance(EXPECTED.id)

                assert actual == EXPECTED
