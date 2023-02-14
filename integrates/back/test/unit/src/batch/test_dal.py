from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_mock_response,
    get_mocked_path,
    get_module_at_test,
    set_mocks_return_values,
)
from batch.dal import (
    delete_action,
    get_action,
    get_actions,
    IntegratesBatchQueue,
    mapping_to_key,
    put_action_to_batch,
    put_action_to_dynamodb,
    SkimsBatchQueue,
    to_queue,
)
from batch.enums import (
    Product,
)
from batch.types import (
    BatchProcessing,
)
import json
import pytest
from typing import (
    Union,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["key"],
    [
        ["44aa89bddf5e0a5b1aca2551799b71ff593c95a89f4402b84697e9b29f652110"],
    ],
)
@patch(MODULE_AT_TEST + "dynamodb_ops.delete_item", new_callable=AsyncMock)
async def test_delete_action(
    mock_dynamodb_ops_delete_item: AsyncMock, key: str
) -> None:

    assert set_mocks_return_values(
        mocks_args=[[key]],
        mocked_objects=[mock_dynamodb_ops_delete_item],
        module_at_test=MODULE_AT_TEST,
        paths_list=["dynamodb_ops.delete_item"],
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
@patch(MODULE_AT_TEST + "dynamodb_ops.query", new_callable=AsyncMock)
async def test_get_action(
    mock_dynamodb_ops_query: AsyncMock, key: str, expected_bool: bool
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[key]],
        mocked_objects=[mock_dynamodb_ops_query],
        module_at_test=MODULE_AT_TEST,
        paths_list=["dynamodb_ops.query"],
    )
    action = await get_action(action_dynamo_pk=key)
    assert bool(action) is expected_bool
    assert mock_dynamodb_ops_query.called is True


@patch(MODULE_AT_TEST + "dynamodb_ops.scan", new_callable=AsyncMock)
async def test_get_actions(
    mock_dynamodb_ops_scan: AsyncMock,
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[]],
        mocked_objects=[mock_dynamodb_ops_scan],
        module_at_test=MODULE_AT_TEST,
        paths_list=["dynamodb_ops.scan"],
    )
    all_actions = await get_actions()
    assert all_actions
    assert len(all_actions) == 2
    assert mock_dynamodb_ops_scan.called is True


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
                    "treatments": ["ACCEPTED", "UNTREATED"],
                    "states": ["VULNERABLE"],
                    "verifications": [],
                    "closing_date": None,
                    "finding_title": "038",
                    "age": 1100,
                    "min_severity": "2.4",
                    "max_severity": "6.4",
                }
            ),
            "7790c855b860e6a0365c5755c362f4f579ba958edea3fce14146f4270541a6a4",
        ],
        [
            "report",
            "unittesting",
            "unittesting@fluidattacks.com",
            json.dumps(
                {
                    "report_type": "XLS",
                    "treatments": [
                        "ACCEPTED",
                        "ACCEPTED_UNDEFINED",
                        "IN_PROGRESS",
                        "UNTREATED",
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
            "ecfa753fb705d90f4636906dcd2fb8db7ddb06cb356e14fe0fb57c23e92fafb5",
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
                            "UNTREATED",
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
                key="ecfa753fb705d90f4636906dcd2fb8db7ddb06cb356e14fe0fb57c23e92fafb5",  # noqa: E501 pylint: disable=line-too-long
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
                            "UNTREATED",
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


@pytest.mark.parametrize(
    [
        "action_name",
        "entity",
        "subject",
        "time",
        "additional_info",
        "queue",
    ],
    [
        [
            "report",
            "unittesting",
            "unittesting@fluidattacks.com",
            "1673453501",
            json.dumps(
                {
                    "report_type": "XLS",
                    "treatments": [
                        "ACCEPTED",
                        "ACCEPTED_UNDEFINED",
                        "IN_PROGRESS",
                        "UNTREATED",
                    ],
                    "states": ["SAFE"],
                    "verifications": ["VERIFIED"],
                    "closing_date": "2020-06-01T05:00:00+00:00",
                    "finding_title": "039",
                    "age": 1200,
                    "min_severity": "2.7",
                    "max_severity": None,
                }
            ),
            IntegratesBatchQueue.SMALL,
        ],
    ],
)
@patch(get_mocked_path("dynamodb_ops.put_item"), new_callable=AsyncMock)
async def test_put_action_to_dynamodb(  # pylint: disable=too-many-arguments
    mock_dynamodb_ops_put_item: AsyncMock,
    action_name: str,
    entity: str,
    subject: str,
    time: str,
    additional_info: str,
    queue: Union[IntegratesBatchQueue, SkimsBatchQueue],
) -> None:

    key = mapping_to_key(
        [
            action_name,
            entity,
            subject,
            additional_info,
        ]
    )
    mock_dynamodb_ops_put_item.return_value = get_mock_response(
        get_mocked_path("dynamodb_ops.put_item"),
        json.dumps(
            [
                key,
                time,
                queue,
            ],
            default=str,
        ),
    )
    result = await put_action_to_dynamodb(
        action_name=action_name,
        entity=entity,
        subject=subject,
        time=time,
        additional_info=additional_info,
        queue=queue,
        key=key,
    )
    assert mock_dynamodb_ops_put_item.called is True
    assert result == key
