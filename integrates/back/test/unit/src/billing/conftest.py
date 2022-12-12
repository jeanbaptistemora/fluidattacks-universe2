import boto3
from context import (
    FI_AWS_S3_MAIN_BUCKET,
)
from moto import (
    mock_s3,
)
from mypy_boto3_s3 import (
    S3Client,
)
import pytest
from typing import (
    AsyncGenerator,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.fixture(name="s3_client", scope="module")
async def s_3() -> AsyncGenerator[S3Client, None]:
    """Mocked S3 Fixture."""
    with mock_s3():
        yield boto3.client("s3")


@pytest.fixture(scope="module", autouse=True)
def create_bucket(s3_client: S3Client) -> None:
    s3_client.create_bucket(Bucket=FI_AWS_S3_MAIN_BUCKET)
