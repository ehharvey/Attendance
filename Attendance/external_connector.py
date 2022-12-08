"""Module that handles retrieving and serving IPs for other services"""
from pydantic import BaseModel, validator
from typing import Dict
import git
import tempfile
from pathlib import Path
import json
import requests
from datetime import date
from datetime import datetime


REPO_URL = (
    "https://Ecoleshill@dev.azure.com/Ecoleshill/CSCN73030-F22/_git/CSCN73030-F22"
)

SERVICE_JSON_FILE = Path("serviceips.json")


class Service(BaseModel):
    ip: str
    port: int

    @validator("ip")
    def fix_ip(cls, value: str):
        value = value.strip("/")

        if value.startswith("https://") or value.startswith("http://"):
            return value
        else:
            return f"http://{value}"


class ServiceContainer(BaseModel):
    assignments: Service
    attendance: Service
    calendar: Service
    classlist: Service
    grades: Service
    groups: Service
    rubrics: Service
    quizzes: Service
    surveys: Service
    adminactivities: Service


class ExternalConnector:
    def __init__(self, url: Path = REPO_URL, file: Path = SERVICE_JSON_FILE, timeout=3):
        self.timeout = timeout
        self.fetched = False
        self.services = None
        self.url = url
        self.file = file

    def get_service_json(self) -> Dict[str, dict]:
        with tempfile.TemporaryDirectory() as t:
            git.Repo.clone_from(self.url, t, branch="main", depth=1)

            result_file = t / self.file

            with result_file.open(encoding="utf-8", mode="r") as f:
                return json.load(f)

    def fetch(self):
        repo_data = self.get_service_json()
        self.services: ServiceContainer = ServiceContainer(**repo_data)
        self.fetched = True

    def getCalendar(self):
        if not self.fetched:
            self.fetch()

        response = requests.get(
            f"{self.services.calendar.ip}:{self.services.calendar.port}/events",
            timeout=self.timeout,
        )

        return json.loads(response.content)

    def getClasslist(self):
        if not self.fetched:
            self.fetch()

        response = requests.get(
            f"{self.services.classlist.ip}:{self.services.classlist.port}/students",
            timeout=self.timeout,
        )

        return json.loads(response.content)

    def getModeOfOperation(self):
        if not self.fetched:
            self.fetch()

        response = requests.get(
            f"{self.services.adminactivities.ip}:{self.services.adminactivities.port}/modeofoperation",
            timeout=self.timeout,
        )

        return json.loads(response.content)


class Student(BaseModel):
    firstname: str
    lastname: str
    email: str
    studentNumber: int


class Event(BaseModel):
    enterpriseID: str
    title: str
    startDate: str
    dueDate: str
    type: str


class ModeOfOperation(BaseModel):
    modeofoperation: bool


class ExternalConnectorStub(ExternalConnector):
    def __init__(self):
        pass

    def fetch(self):
        pass

    def getClasslist(self):
        return [
            Student(
                firstname="Hello",
                lastname="World",
                email="Hello@World.com",
                studentNumber=123456,
            ).dict(),
            Student(
                firstname="Hello1",
                lastname="World1",
                email="Hello1@World.com",
                studentNumber=123456,
            ).dict(),
            Student(
                firstname="Hello2",
                lastname="World2",
                email="Hello2@World.com",
                studentNumber=123456,
            ).dict(),
            Student(
                firstname="Hello3",
                lastname="World3",
                email="Hello3@World.com",
                studentNumber=123456,
            ).dict(),
            Student(
                firstname="Hello4",
                lastname="World4",
                email="Hello4@World.com",
                studentNumber=123456,
            ).dict(),
        ]

    def getCalendar(self):
        return [
            Event(
                enterpriseID="id0",
                title="Course A Class",
                startDate="2022-11-20T12:00:00",
                dueDate="2022-11-25T12:00:00",
                type="Test",
            ).dict(),
            Event(
                enterpriseID="id1",
                title="Test 3",
                startDate="2022-12-7T12:00:00",
                dueDate="2022-12-7T12:00:00",
                type="Survey",
            ).dict(),
            Event(
                enterpriseID="id2",
                title="Survey Due",
                startDate="2022-12-14T12:00:00",
                dueDate="2022-12-14T12:00:00",
                type="Test",
            ).dict(),
            Event(
                enterpriseID="id3",
                title="Quiz",
                startDate="2022-12-21T12:00:00",
                dueDate="2022-12-21T12:00:00",
                type="Assignment",
            ).dict(),
            Event(
                enterpriseID="id4",
                title="Misc",
                startDate="2022-12-28T12:00:00",
                dueDate="2022-12-28T12:00:00",
                type="Test",
            ).dict(),
        ]

    def getModeOfOperation(self):
        return ModeOfOperation(modeofoperation=True).dict()
