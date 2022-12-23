# pylint: disable=import-error
from aioextensions import (
    collect,
)
from back.test.unit.src.utils import (
    get_mock_response,
    get_mocked_path,
)
from batch.dal import (
    delete_action,
    get_action,
    get_actions,
    IntegratesBatchQueue,
    mapping_to_key,
    put_action_to_batch,
    put_action_to_dynamodb,
    to_queue,
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
    Optional,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

pytestmark = [
    pytest.mark.asyncio,
]

TABLE_NAME = "fi_async_processing"


def test_create_table(dynamodb: ServiceResource, populate_db: bool) -> None:
    assert populate_db
    assert TABLE_NAME in dynamodb_backend2.tables
    assert len(dynamodb.Table(TABLE_NAME).scan()["Items"]) == 5


@pytest.mark.parametrize(
    ["key"],
    [
        ["44aa89bddf5e0a5b1aca2551799b71ff593c95a89f4402b84697e9b29f652110"],
    ],
)
@patch(get_mocked_path("dynamodb_ops.delete_item"), new_callable=AsyncMock)
async def test_delete_action(
    mock_dynamodb_ops_delete_item: AsyncMock, key: str
) -> None:
    mock_dynamodb_ops_delete_item.return_value = get_mock_response(
        get_mocked_path("dynamodb_ops.delete_item"),
        json.dumps([key]),
    )
    assert await delete_action(dynamodb_pk=key)
    assert mock_dynamodb_ops_delete_item.called is True
    with pytest.raises(Exception) as delete_exception:
        await delete_action()
    assert "you must supply the dynamodb pk" in str(delete_exception.value)


@pytest.mark.parametrize(
    ["key", "expected_bool"],
    [
        [
            "ac25d6d18e368c34a41103a9f6dbf0a787cf2551d6ef5884c844085d26013e0a",
            True,
        ],
        [
            "049ee0097a137f2961578929a800a5f23f93f59806b901ee3324abf6eb5a4828",
            False,
        ],
    ],
)
@patch(get_mocked_path("dynamodb_ops.query"), new_callable=AsyncMock)
async def test_get_action(
    mock_dynamodb_ops_query: AsyncMock, key: str, expected_bool: bool
) -> None:
    mock_dynamodb_ops_query.return_value = get_mock_response(
        get_mocked_path("dynamodb_ops.query"),
        json.dumps([key]),
    )
    action = await get_action(action_dynamo_pk=key)
    assert bool(action) is expected_bool


async def test_get_actions(dynamodb: ServiceResource) -> None:
    with patch("batch.dal.dynamodb_ops.scan") as mock_scan:
        mock_scan.return_value = dynamodb.Table(TABLE_NAME).scan()["Items"]
        all_actions = await get_actions()
    assert mock_scan.called is True
    assert isinstance(all_actions, list)
    assert len(all_actions) == 5


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
    with patch("batch.dal.dynamodb_ops.scan") as mock_scan:
        mock_scan.return_value = dynamodb.Table(TABLE_NAME).scan()["Items"]
        pending_actions: List[BatchProcessing] = await get_actions()
    assert mock_scan.called is True

    async def _put(action: BatchProcessing) -> Optional[str]:
        product = (
            Product.SKIMS
            if action.action_name == "execute-machine"
            else Product.INTEGRATES
        )
        return await put_action_to_batch(
            entity=action.entity,
            action_name=action.action_name,
            action_dynamo_pk=action.key,
            queue=to_queue(action.queue, product),
            product_name=product.value,
        )

    assert all(
        result is None
        for result in await collect(
            [_put(action) for action in pending_actions],
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
    assert len(dynamodb.Table(TABLE_NAME).scan()["Items"]) == 5
    with patch("batch.dal.dynamodb_ops.put_item") as mock_put_item:
        mock_put_item.side_effect = side_effect
        await put_action_to_dynamodb(queue=IntegratesBatchQueue.SMALL, **item)
    assert mock_put_item.called is True
    assert len(dynamodb.Table(TABLE_NAME).scan()["Items"]) == 5
    assert (
        key
        in dynamodb.Table(TABLE_NAME)
        .get_item(Key={"pk": key})["Item"]
        .values()
    )
