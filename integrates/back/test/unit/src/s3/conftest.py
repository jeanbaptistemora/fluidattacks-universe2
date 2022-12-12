import boto3
from moto import (
    mock_s3,
)
from mypy_boto3_s3 import (
    S3Client,
)
import pytest

BUCKET_NAME = "test_bucket"


@pytest.fixture(scope="module", autouse=True)
def s3_mock() -> S3Client:  # type: ignore
    """Mocked S3 Fixture."""
    with mock_s3():
        s3_client = boto3.client("s3", region_name="us-east-1")
        s3_client.create_bucket(Bucket=BUCKET_NAME)
        yield s3_client
