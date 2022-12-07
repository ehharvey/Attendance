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

    SERVICE_FILE: Optional[Path]
    SERVICE_REPO: Union[AnyHttpUrl, str]

    @validator("S3_BUCKET", always=True)
    def validate_s3(cls, value, values: dict):
        if any(values.values()):
            assert all(values.values()), "Not all S3 Environmental Variables set"
            assert value, "NOt all S3 Environmental Variables set"

        return value

    @validator("SERVICE_REPO", always=True)
    def validate_service_repo(cls, value, values: dict):
        if isinstance(value, AnyHttpUrl):
            pass
        elif isinstance(value, str):
            assert value == "DEBUG", "SERVICE_REPO must be a URL or 'DEBUG'"

        if value != "DEBUG":
            assert values[
                "SERVICE_FILE"
            ], "SERVICE_FILE must be set if SERVICE_REPO is not 'DEBUG'"
        else:
            assert not values[
                "SERVICE_FILE"
            ], "SERVICE_FILE must not be set if SERVICE_REPO is 'DEBUG'"
        return value
