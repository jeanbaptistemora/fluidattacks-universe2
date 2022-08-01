from aioextensions import (
    collect,
)
from batch import (
    dal as batch_dal,
)
from batch.enums import (
    Product,
)
from batch.types import (
    BatchProcessing,
)
import json
from moto.dynamodb2 import (
    dynamodb_backend2,
)
from mypy_boto3_dynamodb import (
    DynamoDBServiceResource as ServiceResource,
)
from newutils.datetime import (
    get_as_epoch,
    get_now,
)
import pytest
from typing import (
    List,
)
from unittest import (
    mock,
)

pytestmark = [
    pytest.mark.asyncio,
]

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
            }
        ),
    ),
]


async def test_put_action_to_dynamodb(dynamodb: ServiceResource) -> None:
    def side_effect(item: dict, table: str) -> bool:
        if bool(table and item):
            return dynamodb.Table(TABLE_NAME).put_item(Item=item)
        return False

    dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
    )
    assert TABLE_NAME in dynamodb_backend2.tables
    assert len(dynamodb.Table(TABLE_NAME).scan()["Items"]) == 0
    with mock.patch("batch.dal.dynamodb_ops.put_item") as mock_put_item:
        mock_put_item.side_effect = side_effect
        for item in data:
            await batch_dal.put_action_to_dynamodb(**item)
    assert len(dynamodb.Table(TABLE_NAME).scan()["Items"]) == 5
    assert (
        dynamodb.Table(TABLE_NAME).scan()["Items"][0]["entity"]
        == "oneshottest"
    )


async def test_get_actions(dynamodb: ServiceResource) -> None:
    with mock.patch("batch.dal.dynamodb_ops.scan") as mock_scan:
        mock_scan.return_value = dynamodb.Table(TABLE_NAME).scan()["Items"]
        all_actions = await batch_dal.get_actions()
    assert isinstance(all_actions, list)
    assert len(all_actions) == 5


async def test_get_action(dynamodb: ServiceResource) -> None:
    with mock.patch("batch.dal.dynamodb_ops.query") as mock_query:
        item_1 = dict(
            action="report",
            entity="unittesting",
            subject="unittesting@fluidattacks.com",
            additional_info=json.dumps(
                {
                    "report_type": "XLS",
                    "treatments": ["ACCEPTED", "NEW"],
                    "states": ["OPEN"],
                    "verifications": [],
                    "closing_date": None,
                }
            ),
        )
        key = batch_dal.mapping_to_key(
            [
                item_1["action"],
                item_1["entity"],
                item_1["subject"],
                item_1["additional_info"],
            ]
        )
        mock_query.return_value = [
            dynamodb.Table(TABLE_NAME).get_item(Key={"pk": key})["Item"]
        ]
        action_in_db = await batch_dal.get_action(action_dynamo_pk=key)
        assert bool(action_in_db)

        item_2 = dict(
            action="report",
            entity="continuoustesting",
            subject="integratesmanager@gmail.com",
            additional_info="PDF",
        )
        key_2 = batch_dal.mapping_to_key(
            [
                item_2["action"],
                item_2["entity"],
                item_2["subject"],
                item_2["additional_info"],
            ]
        )
        try:
            mock_query.return_value = [
                dynamodb.Table(TABLE_NAME).get_item(Key={"pk": key_2})["Item"]
            ]
        except KeyError:
            mock_query.return_value = []
        action_not_in_db = await batch_dal.get_action(action_dynamo_pk=key_2)
        assert not bool(action_not_in_db)


async def test_requeue_actions(dynamodb: ServiceResource) -> None:
    with mock.patch("batch.dal.dynamodb_ops.scan") as mock_scan:
        mock_scan.return_value = dynamodb.Table(TABLE_NAME).scan()["Items"]
        pending_actions: List[BatchProcessing] = await batch_dal.get_actions()

    assert all(
        result is None
        for result in await collect(
            [
                batch_dal.put_action_to_batch(
                    entity=action.entity,
                    action_name=action.action_name,
                    action_dynamo_pk=action.key,
                    queue=action.queue,
                    product_name=(
                        Product.SKIMS
                        if action.action_name == "execute-machine"
                        else Product.INTEGRATES
                    ).value,
                )
                for action in pending_actions
            ],
            workers=20,
        )
    )


async def test_delete_action(dynamodb: ServiceResource) -> None:
    key = "6da32eec4b0f7dba634335a67386983e090cc6c25f58c12244c2d6685a8f5126"
    with mock.patch("batch.dal.dynamodb_ops.delete_item") as mock_delete_item:
        mock_delete_item.return_value = dynamodb.Table(TABLE_NAME).delete_item(
            Key={"pk": key}
        )
        assert await batch_dal.delete_action(dynamodb_pk=key)
    assert len(dynamodb.Table(TABLE_NAME).scan()["Items"]) == 4
    with pytest.raises(Exception) as delete_exception:
        await batch_dal.delete_action()
    assert "you must supply the dynamodb pk" in str(delete_exception.value)
