import boto3
from moto import (
    mock_s3,
)
from mypy_boto3_s3 import (
    S3Client,
)
import os
import pytest

BUCKET_NAME = "test_bucket"


@pytest.fixture(scope="function", autouse=True)
def aws_credentials() -> None:
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture(scope="module", autouse=True)
def s3_mock() -> S3Client:
    """Mocked S3 Fixture."""
    with mock_s3():
        s3_client = boto3.client("s3", region_name="us-east-1")
        s3_client.create_bucket(Bucket=BUCKET_NAME)
        yield s3_client
