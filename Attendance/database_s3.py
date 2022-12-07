import json
from typing import List
from Attendance.database import (
    Database,
    AttendanceAlreadyExists,
    AttendanceDoesNotExist,
    AttendanceIsMalformed,
    Attendance,
)

from boto3 import session
from botocore.client import Config


class DatabaseS3(Database):
    def __init__(
        self,
        s3_region: str,
        s3_url: str,
        s3_key_id: str,
        s3_key_secret: str,
        s3_bucket="projectvattendance",
    ):
        # Initiate session
        self.session = session.Session()
        self.client = self.session.client(
            "s3",
            endpoint_url=s3_url,  # Find your endpoint in the control panel, under Settings. Prepend "https://".
            config=Config(
                s3={"addressing_style": "virtual"}
            ),  # Configures to use subdomain/virtual calling format.
            region_name=s3_region,  # Use the region in your endpoint.
            aws_access_key_id=s3_key_id,  # Access key pair. You can create access key pairs using the control panel or API.
            aws_secret_access_key=s3_key_secret,
        )
        self.s3_bucket = s3_bucket

        buckets = self.client.list_buckets()["Buckets"]
        bucket_names = [b["Name"] for b in buckets]

        if s3_bucket not in bucket_names:
            self.client.create_bucket(Bucket=s3_bucket)

    def list_files(self) -> List[str]:
        query = self.client.list_objects(Bucket=self.s3_bucket)

        if not "Contents" in query:
            return []
        else:
            files = query["Contents"]

            return [f["Key"] for f in files]

    def create_attendance(self, attendance: Attendance) -> None:
        """
        Creates a new attendance item. Raises AttendanceAlreadyExists if the item already exists

        To update an already existing attendance item, use update_attendance
        """

        files = self.list_files()

        if attendance.id in files:
            raise AttendanceAlreadyExists
        else:
            self.client.put_object(
                Bucket=self.s3_bucket,
                Key=attendance.id,
                Body=attendance.json(),
                ACL="private",
            )

    def update_attendance(self, attendance: Attendance) -> None:
        """
        Updates an *existing* Attendance item with a new one
        """

        files = self.list_files()

        if not attendance.id in files:
            raise AttendanceDoesNotExist
        else:
            self.client.put_object(
                Bucket=self.s3_bucket,
                Key=attendance.id,
                Body=attendance.json(),
                ACL="private",
            )

    def get_attendance(self, id: str) -> Attendance:
        """
        Retrieves an existing Attendance item

        Raises AttendanceDoesNotExist if supplied id does not match any stored attendances

        Raises AttendanceIsMalformed is read Attendance is malformed
        """

        files = self.list_files()

        if not id in files:
            raise AttendanceDoesNotExist
        else:
            body = self.client.get_object(Bucket=self.s3_bucket, Key=id)["Body"]

            return Attendance(**json.loads(body.read()))

    def get_summary_attendance(self) -> List[str]:
        return self.list_files()
