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


@pytest.fixture(name="dynamo_resource", scope="module")
def dynamodb() -> ServiceResource:
    """Mocked DynamoDB Fixture."""
    with mock_dynamodb2():
        yield boto3.resource("dynamodb")


@pytest.fixture(scope="module", autouse=True)
def create_table(dynamo_resource: ServiceResource) -> None:
    table_name = "fi_authz"
    key_schema = [
        {"AttributeName": "subject", "KeyType": "HASH"},
        {"AttributeName": "object", "KeyType": "RANGE"},
    ]
    attribute_definitions = [
        {"AttributeName": "subject", "AttributeType": "S"},
        {"AttributeName": "object", "AttributeType": "S"},
    ]
    data = [
        dict(
            level="user",
            object="unittesting",
            role="admin",
            subject="unittest@fluidattacks.com",
        ),
        dict(
            level="group",
            object="oneshottest",
            role="reattacker",
            subject="integrateshacker@fluidattacks.com",
        ),
        dict(
            level="group",
            object="unittesting",
            role="hacker",
            subject="integrateshacker@fluidattacks.com",
        ),
        dict(
            level="group",
            object="unittesting",
            role="user_manager",
            subject="integratesuser@gmail.com",
        ),
        dict(
            level="user",
            object="unittesting",
            role="user",
            subject="integratesuser2@gmail.com",
        ),
        dict(
            level="organization",
            object="org#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            role="customer_manager",
            subject="unittest2@fluidattacks.com",
        ),
        dict(
            level="group",
            object="unittesting",
            role="hacker",
            subject="continuoushacking@gmail.com",
        ),
    ]

    dynamo_resource.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
    )
    for item in data:
        dynamo_resource.Table(table_name).put_item(Item=item)
