import boto3
from moto.dynamodb2 import (
    mock_dynamodb2,
)
import os
import pytest
from typing import (
    Generator,
)


@pytest.fixture(scope="function", autouse=True)
def aws_credentials() -> None:
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="module")
def dynamodb() -> Generator:
    """Mocked DynamoDB Fixture."""
    with mock_dynamodb2():
        yield boto3.resource("dynamodb")
