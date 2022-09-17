# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import boto3
from moto.dynamodb2 import (
    mock_dynamodb2,
)
from mypy_boto3_dynamodb import (
    DynamoDBServiceResource as ServiceResource,
)
import os
import pytest


@pytest.fixture(scope="function", autouse=True)
def aws_credentials() -> None:
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="module")
def dynamodb() -> ServiceResource:  # type: ignore
    """Mocked DynamoDB Fixture."""
    with mock_dynamodb2():
        yield boto3.resource("dynamodb")
