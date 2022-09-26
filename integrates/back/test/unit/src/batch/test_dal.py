# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    collect,
)
from batch.dal import (
    delete_action,
    get_action,
    get_actions,
    mapping_to_key,
    put_action_to_batch,
    put_action_to_dynamodb,
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


def test_create_table(dynamodb: ServiceResource, populate_db: bool) -> None:
    assert populate_db
    assert TABLE_NAME in dynamodb_backend2.tables
    assert len(dynamodb.Table(TABLE_NAME).scan()["Items"]) == 5


async def test_delete_action(dynamodb: ServiceResource) -> None:
    key = "44aa89bddf5e0a5b1aca2551799b71ff593c95a89f4402b84697e9b29f652110"
    with mock.patch("batch.dal.dynamodb_ops.delete_item") as mock_delete_item:
        mock_delete_item.return_value = dynamodb.Table(TABLE_NAME).delete_item(
            Key={"pk": key}
        )
        assert await delete_action(dynamodb_pk=key)
    assert len(dynamodb.Table(TABLE_NAME).scan()["Items"]) == 4
    with pytest.raises(Exception) as delete_exception:
        await delete_action()
    assert "you must supply the dynamodb pk" in str(delete_exception.value)


async def test_get_action(dynamodb: ServiceResource) -> None:
    item_1 = dict(
        action_name="report",
        entity="unittesting",
        subject="unittesting@fluidattacks.com",
        additional_info=json.dumps(
            {
                "report_type": "XLS",
                "treatments": ["ACCEPTED", "NEW"],
                "states": ["OPEN"],
                "verifications": [],
                "closing_date": None,
                "finding_title": "038",
                "age": 1100,
                "min_severity": "2.4",
                "max_severity": "6.4",
            }
        ),
    )
    key = mapping_to_key(
        [
            item_1["action_name"],
            item_1["entity"],
            item_1["subject"],
            item_1["additional_info"],
        ]
    )
    with mock.patch("batch.dal.dynamodb_ops.query") as mock_query:
        mock_query.return_value = [
            dynamodb.Table(TABLE_NAME).get_item(Key={"pk": key})["Item"]
        ]
        action_in_db = await get_action(action_dynamo_pk=key)
    assert bool(action_in_db)

    item_2 = dict(
        action_name="report",
        entity="continuoustesting",
        subject="integratesmanager@gmail.com",
        additional_info="PDF",
    )
    key_2 = mapping_to_key(
        [
            item_2["action_name"],
            item_2["entity"],
            item_2["subject"],
            item_2["additional_info"],
        ]
    )
    with mock.patch("batch.dal.dynamodb_ops.query") as mock_query:
        try:
            mock_query.return_value = [
                dynamodb.Table(TABLE_NAME).get_item(Key={"pk": key_2})["Item"]
            ]
        except KeyError:
            mock_query.return_value = []
        action_not_in_db = await get_action(action_dynamo_pk=key_2)
    assert not bool(action_not_in_db)


async def test_get_actions(dynamodb: ServiceResource) -> None:
    with mock.patch("batch.dal.dynamodb_ops.scan") as mock_scan:
        mock_scan.return_value = dynamodb.Table(TABLE_NAME).scan()["Items"]
        all_actions = await get_actions()
    assert isinstance(all_actions, list)
    assert len(all_actions) == 4


def test_mapping_to_key(dynamodb: ServiceResource) -> None:
    item_1 = dict(
        action_name="report",
        entity="unittesting",
        subject="unittesting@fluidattacks.com",
        additional_info=json.dumps(
            {
                "report_type": "XLS",
                "treatments": ["ACCEPTED", "NEW"],
                "states": ["OPEN"],
                "verifications": [],
                "closing_date": None,
                "finding_title": "038",
                "age": 1100,
                "min_severity": "2.4",
                "max_severity": "6.4",
            }
        ),
    )
    key = mapping_to_key(
        [
            item_1["action_name"],
            item_1["entity"],
            item_1["subject"],
            item_1["additional_info"],
        ]
    )

    assert dynamodb.Table(TABLE_NAME).get_item(Key={"pk": key})["Item"]


async def test_put_action_to_batch(dynamodb: ServiceResource) -> None:
    with mock.patch("batch.dal.dynamodb_ops.scan") as mock_scan:
        mock_scan.return_value = dynamodb.Table(TABLE_NAME).scan()["Items"]
        pending_actions: List[BatchProcessing] = await get_actions()

    assert all(
        result is None
        for result in await collect(
            [
                put_action_to_batch(
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


async def test_put_action_to_dynamodb(dynamodb: ServiceResource) -> None:
    def side_effect(item: dict, table: str) -> bool:
        if bool(table and item):
            return dynamodb.Table(TABLE_NAME).put_item(  # type: ignore
                Item=item
            )
        return False

    time = str(get_as_epoch(get_now()))
    item = dict(
        action_name="report",
        entity="unittesting",
        subject="unittesting@fluidattacks.com",
        time=time,
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
    )
    key = mapping_to_key(
        [
            item["action_name"],
            item["entity"],
            item["subject"],
            item["additional_info"],
        ]
    )
    assert len(dynamodb.Table(TABLE_NAME).scan()["Items"]) == 4
    with mock.patch("batch.dal.dynamodb_ops.put_item") as mock_put_item:
        mock_put_item.side_effect = side_effect
        await put_action_to_dynamodb(**item)
    assert len(dynamodb.Table(TABLE_NAME).scan()["Items"]) == 5
    assert (
        key
        in dynamodb.Table(TABLE_NAME)
        .get_item(Key={"pk": key})["Item"]
        .values()
    )
