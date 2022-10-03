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

pytestmark = [
    pytest.mark.asyncio,
]

tables_names = ["fi_authz", "integrates_vms"]
key_schemas = {
    "fi_authz": [
        {"AttributeName": "subject", "KeyType": "HASH"},
        {"AttributeName": "object", "KeyType": "RANGE"},
    ],
    "integrates_vms": [
        {"AttributeName": "pk", "KeyType": "HASH"},
        {"AttributeName": "sk", "KeyType": "RANGE"},
    ],
}
attribute_definitions = {
    "fi_authz": [
        {"AttributeName": "subject", "AttributeType": "S"},
        {"AttributeName": "object", "AttributeType": "S"},
    ],
    "integrates_vms": [
        {"AttributeName": "sk", "AttributeType": "S"},
        {"AttributeName": "pk", "AttributeType": "S"},
    ],
}
data = dict(
    fi_authz=[
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
    ],
    integrates_vms=[
        dict(
            is_concurrent_session="False",
            is_registered="True",
            role="hacker",
            last_name="Hacking",
            last_login_date="2020-03-23T15:45:37+00:00",
            legal_remember="True",
            registration_date="2018-02-28T16:54:12+00:00",
            sk="USER#continuoushacking@gmail.com",
            pk_2="USER#all",
            pk="USER#continuoushacking@gmail.com",
            first_name="Continuous",
            email="continuoushacking@gmail.com",
            sk_2="USER#continuoushacking@gmail.com",
        ),
        dict(
            is_concurrent_session="False",
            is_registered="True",
            role="hacker",
            last_name="Hacker",
            last_login_date="2019-10-29T18:40:37+00:00",
            legal_remember="False",
            registration_date="2018-02-28T16:54:12+00:00",
            sk="USER#integrateshacker@fluidattacks.com",
            pk_2="USER#all",
            pk="USER#integrateshacker@fluidattacks.com",
            first_name="Integrates",
            email="integrateshacker@fluidattacks.com",
            sk_2="USER#integrateshacker@fluidattacks.com",
        ),
        dict(
            is_concurrent_session="False",
            is_registered="True",
            role="user",
            last_name="User",
            last_login_date="2019-10-29T18:40:37+00:00",
            legal_remember="True",
            registration_date="2018-02-28T16:54:12+00:00",
            sk="USER#integratesuser@gmail.com",
            pk_2="USER#all",
            pk="USER#integratesuser@gmail.com",
            first_name="Integrates",
            email="integratesuser@gmail.com",
            sk_2="USER#integratesuser@gmail.com",
        ),
        dict(
            is_concurrent_session="False",
            is_registered="True",
            role="admin",
            last_name="de Orellana",
            last_login_date="2019-10-29T18:40:37+00:00",
            legal_remember="True",
            registration_date="2019-02-28T16:54:12+00:00",
            push_token="[ExponentPushToken[dummy]]",
            sk="USER#unittest@fluidattacks.com",
            pk_2="USER#all",
            pk="USER#unittest@fluidattacks.com",
            first_name="Miguel",
            email="unittest@fluidattacks.com",
            sk_2="USER#unittest@fluidattacks.com",
        ),
    ],
)


@pytest.fixture(scope="function", autouse=True)
def aws_credentials() -> None:
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(name="dynamo_resource", scope="module")
async def dynamodb() -> ServiceResource:  # type: ignore
    """Mocked DynamoDB Fixture."""
    with mock_dynamodb2():
        yield boto3.resource("dynamodb")


@pytest.fixture(scope="module", autouse=True)
def create_tables(dynamo_resource: ServiceResource) -> None:
    for table in tables_names:
        dynamo_resource.create_table(
            TableName=table,
            KeySchema=key_schemas[table],  # type: ignore
            AttributeDefinitions=attribute_definitions[table],  # type: ignore
        )
        for item in data[table]:
            dynamo_resource.Table(table).put_item(Item=item)
