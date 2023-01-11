# pylint: disable=import-error
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


@pytest.mark.parametrize(
    ["action_name", "entity", "subject", "additional_info", "expected_result"],
    [
        [
            "report",
            "unittesting",
            "unittesting@fluidattacks.com",
            json.dumps(
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
            "69bda99b6a486a86b64e6e3188c3d4c82ccf195ad0baa14fca63656e7666aad4",
        ],
    ],
)
def test_mapping_to_key(
    action_name: str,
    entity: str,
    subject: str,
    additional_info: str,
    expected_result: str,
) -> None:
    key = mapping_to_key(
        [
            action_name,
            entity,
            subject,
            additional_info,
        ]
    )

    assert key == expected_result


@pytest.mark.parametrize(
    ["action"],
    [
        [
            BatchProcessing(
                key="78ebd9f895b8efcd4e6d4cf40d3dbcf3f6fc2ac655537edc0b0465bd3a80871c",  # noqa: E501 pylint: disable=line-too-long
                action_name="report",
                entity="unittesting",
                subject="unittesting@fluidattacks.com",
                time="1672248409",
                additional_info=json.dumps(
                    {
                        "report_type": "XLS",
                        "treatments": [
                            "ACCEPTED",
                            "ACCEPTED_UNDEFINED",
                            "IN_PROGRESS",
                            "NEW",
                        ],
                        "states": ["SAFE"],
                        "verifications": ["VERIFIED"],
                        "closing_date": "2020-06-01T00:00:00",
                        "finding_title": "065",
                        "age": None,
                        "min_severity": None,
                        "max_severity": None,
                        "last_report": None,
                        "min_release_date": None,
                        "max_release_date": None,
                        "location": "",
                    }
                ),
                queue="integrates_medium",
                batch_job_id=None,
                retries=0,
                running=False,
            ),
        ],
        [
            BatchProcessing(
                key="78ebd9f895b8efcd4e6d4cf40d3dbcf3f6fc2ac655537edc0b0465bd3a80871c",  # noqa: E501 pylint: disable=line-too-long
                action_name="report",
                entity="unittesting",
                subject="unittesting@fluidattacks.com",
                time="1672248409",
                additional_info=json.dumps(
                    {
                        "report_type": "XLS",
                        "treatments": [
                            "ACCEPTED",
                            "ACCEPTED_UNDEFINED",
                            "IN_PROGRESS",
                            "NEW",
                        ],
                        "states": ["SAFE", "VULNERABLE"],
                        "verifications": [],
                        "closing_date": None,
                        "finding_title": "068",
                        "age": 1300,
                        "min_severity": "2.9",
                        "max_severity": "4.3",
                        "last_report": None,
                        "min_release_date": None,
                        "max_release_date": None,
                        "location": "",
                    }
                ),
                queue="integrates_medium",
                batch_job_id=None,
                retries=0,
                running=False,
            ),
        ],
    ],
)
async def test_put_action_to_batch(action: BatchProcessing) -> None:
    product = (
        Product.SKIMS
        if action.action_name == "execute-machine"
        else Product.INTEGRATES
    )
    assert (
        await put_action_to_batch(
            entity=action.entity,
            action_name=action.action_name,
            action_dynamo_pk=action.key,
            queue=to_queue(action.queue, product),
            product_name=product.value,
        )
        is None
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
