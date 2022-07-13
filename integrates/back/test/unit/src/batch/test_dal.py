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

scan_actions_result = {
    "Items": [
        {
            "additional_info": json.dumps(
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
            "subject": "unittesting@fluidattacks.com",
            "action_name": "report",
            "pk": (
                "1bc77999477bfcc84cd111ac745407f2b9ff21e930f59b097b414bbe34f2"
                "9b46"
            ),
            "time": "1616116348",
            "entity": "unittesting",
            "queue": "small",
        },
        {
            "additional_info": json.dumps(
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
            "subject": "unittesting@fluidattacks.com",
            "action_name": "report",
            "pk": (
                "7eda9da492308050bee1bb70b386ffcb3fc9bcabe5b41185113706fe6a2d"
                "490c"
            ),
            "time": "1615834776",
            "entity": "unittesting",
            "queue": "small",
        },
        {
            "additional_info": json.dumps(
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
            "subject": "unittesting@fluidattacks.com",
            "action_name": "report",
            "pk": (
                "71992ff157b46d63fe5bb9dd37176cdb0e27854009b0529d648375d9bfb3"
                "8977"
            ),
            "time": "1616116348",
            "entity": "unittesting",
            "queue": "small",
        },
        {
            "additional_info": json.dumps(
                {
                    "report_type": "XLS",
                    "treatments": ["ACCEPTED", "NEW"],
                    "states": ["OPEN"],
                    "verifications": ["REQUESTED"],
                    "closing_date": None,
                }
            ),
            "subject": "unittesting@fluidattacks.com",
            "action_name": "report",
            "pk": (
                "0b60f7743b70ef85c0bc62d49483cef23a883ef03aac17d8921021214f08"
                "2ad6"
            ),
            "time": "1615834776",
            "entity": "unittesting",
            "queue": "small",
        },
        {
            "additional_info": json.dumps(
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
            "subject": "unittesting@fluidattacks.com",
            "action_name": "report",
            "pk": (
                "5ae92b4b4437e3e004fb668bed37472fe4615d92767e3a31d81a7d9ea7c7"
                "d999"
            ),
            "time": "1656429212",
            "entity": "unittesting",
            "queue": "small",
        },
    ],
}


async def test_get_actions() -> None:
    with mock.patch("batch.dal.dynamodb_ops.scan") as mock_scan:
        mock_scan.result = scan_actions_result
    all_actions = await batch_dal.get_actions()
    assert isinstance(all_actions, list)
    assert len(all_actions) == 5


async def test_get_action() -> None:
    def side_effect(table_name: str, key_condition: dict) -> list:
        for item in scan_actions_result["Items"]:
            if item["pk"] in key_condition.values() and bool(table_name):
                return [item]
        return []

    with mock.patch(
        "batch.dal.boto3.dynamodb.conditions.Equals"
    ) as mock_key_condition:
        with mock.patch("batch.dal.dynamodb_ops.query") as mock_query:
            mock_query.side_effect = side_effect
            item_1 = dict(
                action="report",
                additional_info=json.dumps(
                    {
                        "report_type": "XLS",
                        "treatments": list(sorted(["ACCEPTED", "NEW"])),
                        "states": ["OPEN"],
                        "verifications": ["REQUESTED"],
                        "closing_date": None,
                    }
                ),
                entity="unittesting",
                subject="integratesmanager@gmail.com",
                time="1615834776",
            )
            key = batch_dal.mapping_to_key(
                [
                    item_1["action"],
                    item_1["additional_info"],
                    item_1["entity"],
                    item_1["subject"],
                    item_1["time"],
                ]
            )
            mock_key_condition.return_value = key
            action = await batch_dal.get_action(action_dynamo_pk=key)
            assert bool(action)

            item_2 = dict(
                action="report",
                additional_info="PDF",
                entity="continuoustesting",
                subject="integratesmanager@gmail.com",
                time="1615834776",
            )
            key_2 = batch_dal.mapping_to_key(
                [
                    item_2["action"],
                    item_2["additional_info"],
                    item_2["entity"],
                    item_2["subject"],
                    item_2["time"],
                ]
            )
            mock_key_condition.return_value = key_2
            optional_action = await batch_dal.get_action(
                action_dynamo_pk=key_2
            )
            assert not bool(optional_action)


async def test_requeue_actions() -> None:
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


@pytest.mark.changes_db
async def test_put_action_to_dynamodb() -> None:
    time = str(get_as_epoch(get_now()))
    item_1 = dict(
        action_name="report",
        entity="oneshottest",
        subject="integratesmanager@gmail.com",
        time=time,
        additional_info="XLS",
    )
    key_1 = await batch_dal.put_action_to_dynamodb(**item_1)
    action_1 = await batch_dal.get_action(action_dynamo_pk=key_1)
    assert action_1.queue == "small"
    assert await batch_dal.is_action_by_key(key=action_1.key)
    assert await batch_dal.delete_action(
        action_name="report",
        additional_info="XLS",
        entity="oneshottest",
        subject="integratesmanager@gmail.com",
        time=time,
    )
    assert not await batch_dal.is_action_by_key(key=action_1.key)
