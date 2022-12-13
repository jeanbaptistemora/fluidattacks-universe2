from batch import (
    dal as batch_dal,
)
import boto3
import json
from moto.dynamodb2 import (
    mock_dynamodb2,
)
from mypy_boto3_dynamodb import (
    DynamoDBServiceResource as ServiceResource,
)
from newutils.datetime import (
    get_as_epoch,
    get_now,
)
import pytest
from unittest import (
    mock,
)

TABLE_NAME = "fi_async_processing"
key_schema = [{"AttributeName": "pk", "KeyType": "HASH"}]
attribute_definitions = [{"AttributeName": "pk", "AttributeType": "S"}]
TIME = str(get_as_epoch(get_now()))

data = [
    dict(
        action_name="report",
        entity="oneshottest",
        subject="unittesting@fluidattacks.com",
        time=TIME,
        additional_info=json.dumps(
            {
                "report_type": "PDF",
                "treatments": [
                    "ACCEPTED",
                    "ACCEPTED_UNDEFINED",
                    "IN_PROGRESS",
                    "NEW",
                ],
                "states": ["CLOSED", "OPEN"],
                "verifications": [],
                "closing_date": None,
                "finding_title": "",
                "age": None,
                "min_severity": None,
                "max_severity": None,
            }
        ),
    ),
    dict(
        action_name="report",
        entity="unittesting",
        subject="unittesting@fluidattacks.com",
        time=TIME,
        additional_info=json.dumps(
            {
                "report_type": "XLS",
                "treatments": [
                    "ACCEPTED",
                    "ACCEPTED_UNDEFINED",
                    "IN_PROGRESS",
                    "NEW",
                ],
                "states": ["CLOSED", "OPEN"],
                "verifications": [],
                "closing_date": None,
                "finding_title": "",
                "age": None,
                "min_severity": None,
                "max_severity": None,
            }
        ),
    ),
    dict(
        action_name="report",
        entity="unittesting",
        subject="unittesting@fluidattacks.com",
        time=TIME,
        additional_info=json.dumps(
            {
                "report_type": "DATA",
                "treatments": [
                    "ACCEPTED",
                    "ACCEPTED_UNDEFINED",
                    "IN_PROGRESS",
                    "NEW",
                ],
                "states": ["CLOSED", "OPEN"],
                "verifications": [],
                "closing_date": None,
                "finding_title": "",
                "age": None,
                "min_severity": None,
                "max_severity": None,
            }
        ),
    ),
    dict(
        action_name="report",
        entity="unittesting",
        subject="unittesting@fluidattacks.com",
        time=TIME,
        additional_info=json.dumps(
            {
                "report_type": "XLS",
                "treatments": [
                    "ACCEPTED",
                    "NEW",
                ],
                "states": ["OPEN"],
                "verifications": [],
                "closing_date": None,
                "finding_title": "038",
                "age": 1100,
                "min_severity": "2.4",
                "max_severity": "6.4",
            }
        ),
    ),
    dict(
        action_name="report",
        entity="unittesting",
        subject="unittesting@fluidattacks.com",
        time=TIME,
        additional_info=json.dumps(
            {
                "report_type": "XLS",
                "treatments": [
                    "ACCEPTED",
                    "ACCEPTED_UNDEFINED",
                    "IN_PROGRESS",
                    "NEW",
                ],
                "states": ["CLOSED"],
                "verifications": ["VERIFIED"],
                "closing_date": "2020-06-01T05:00:00+00:00",
                "age": 1200,
                "finding_title": "",
                "min_severity": "2.7",
                "max_severity": None,
            }
        ),
    ),
]


@pytest.fixture(name="dynamodb", scope="module")
def fixture_dynamodb() -> ServiceResource:  # type: ignore
    # Mocked DynamoDB Fixture.
    with mock_dynamodb2():
        yield boto3.resource("dynamodb")


@pytest.fixture(scope="module")
async def populate_db(dynamodb: ServiceResource) -> bool:
    def side_effect(item: dict, table: str) -> bool:
        if bool(table and item):
            return dynamodb.Table(TABLE_NAME).put_item(  # type: ignore
                Item=item
            )
        return False

    # Create mocked table
    dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=key_schema,  # type: ignore
        AttributeDefinitions=attribute_definitions,  # type: ignore
    )
    # Populate table
    with mock.patch("batch.dal.dynamodb_ops.put_item") as mock_put_item:
        mock_put_item.side_effect = side_effect
        for item in data:
            await batch_dal.put_action_to_dynamodb(
                queue=batch_dal.IntegratesBatchQueue.SMALL, **item
            )
    return True
