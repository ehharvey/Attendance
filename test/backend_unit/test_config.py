"""Tests Attendance.config.Config"""

from pathlib import Path
from Attendance.config import Config

from pydantic.error_wrappers import ValidationError

import pytest


class TestConfig:
    def test_debug(self):
        # Act
        actual = Config(SERVICE_REPO="DEBUG")

        # Assert
        assert actual.S3_REGION is None
        assert actual.S3_URL is None
        assert actual.S3_KEY_ID is None
        assert actual.S3_KEY_SECRET is None
        assert actual.S3_BUCKET is None
        assert actual.SERVICE_FILE is None
        assert actual.SERVICE_REPO == "DEBUG"

    def test_no_service_file(self):
        # Act
        with pytest.raises(ValidationError):
            actual = Config(
                SERVICE_REPO="https://github.com/CSCN73030-projectv-group9/ServiceJsonStudent"
            )

    def test_no_service_repo(self):
        with pytest.raises(ValidationError):
            actual = Config(
                SERVICE_FILE="https://github.com/CSCN73030-projectv-group9/ServiceJsonStudent"
            )

    def test_partial_s3(self):
        with pytest.raises(ValidationError):
            actual = Config(S3_KEY_ID="Foo", SERVICE_REPO="DEBUG")

    def test_full_s3_debug(self):
        # Act
        actual = Config(
            S3_REGION="region",
            S3_URL="url",
            S3_KEY_ID="key_id",
            S3_KEY_SECRET="key_secret",
            S3_BUCKET="bucket",
            SERVICE_REPO="DEBUG",
        )

        # Assert
        assert actual.S3_REGION == "region"
        assert actual.S3_URL == "url"
        assert actual.S3_KEY_ID == "key_id"
        assert actual.S3_KEY_SECRET == "key_secret"
        assert actual.S3_BUCKET == "bucket"
        assert actual.SERVICE_FILE is None
        assert actual.SERVICE_REPO == "DEBUG"

    def test_full_config(self):
        # Act
        actual = Config(
            S3_REGION="region",
            S3_URL="url",
            S3_KEY_ID="key_id",
            S3_KEY_SECRET="key_secret",
            S3_BUCKET="bucket",
            SERVICE_REPO="https://github.com/CSCN73030-projectv-group9/ServiceJsonStudent",
            SERVICE_FILE="serviceips.json",
        )

        # Assert
        assert actual.S3_REGION == "region"
        assert actual.S3_URL == "url"
        assert actual.S3_KEY_ID == "key_id"
        assert actual.S3_KEY_SECRET == "key_secret"
        assert actual.S3_BUCKET == "bucket"
        assert actual.SERVICE_FILE == Path("serviceips.json")
        assert (
            actual.SERVICE_REPO
            == "https://github.com/CSCN73030-projectv-group9/ServiceJsonStudent"
        )
