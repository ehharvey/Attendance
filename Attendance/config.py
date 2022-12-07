"""Config for app"""

from typing import Optional, Union
from pydantic import BaseModel, validator, AnyHttpUrl
from pathlib import Path


class Config(BaseModel):
    S3_REGION: Optional[str]
    S3_URL: Optional[str]
    S3_KEY_ID: Optional[str]
    S3_KEY_SECRET: Optional[str]
    S3_BUCKET: Optional[str]

    SERVICE_REPO: Union[AnyHttpUrl, str]
    SERVICE_FILE: Optional[Path]

    @validator("S3_BUCKET", always=True)
    def validate_s3(cls, value, values: dict):
        if any(values.values()):
            assert all(values.values()), "Not all S3 Environmental Variables set"
            assert value, "NOt all S3 Environmental Variables set"

        return value

    @validator("SERVICE_REPO")
    def validate_service_repo(cls, value):
        if isinstance(value, str):
            assert value == "DEBUG", "SERVICE_REPO must be a URL or 'DEBUG'"

        return value

    @validator("SERVICE_FILE")
    def validate_service_file(cls, value, values: dict):
        assert "SERVICE_REPO" in values, "SERVICE_REPO must be set if SERVICE_FILE is"

        return value
