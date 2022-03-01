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

pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_actions() -> None:
    all_actions = await batch_dal.get_actions()
    assert isinstance(all_actions, list)
    assert len(all_actions) == 4


async def test_get_action() -> None:
    item_1 = dict(
        action="report",
        additional_info=json.dumps(
            {
                "report_type": "XLS",
                "treatments": list(sorted(["ACCEPTED"])),
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
    optional_action = await batch_dal.get_action(action_dynamo_pk=key_2)
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
    item_2 = dict(
        action_name="handle_virus_scan",
        entity="file_name",
        subject="integratesmanager@gmail.com",
        additional_info="oneshottest",
        time=time,
        queue="dedicated_soon",
    )
    key_2 = await batch_dal.put_action_to_dynamodb(**item_2)

    action_1 = await batch_dal.get_action(action_dynamo_pk=key_1)

    action_2 = await batch_dal.get_action(action_dynamo_pk=key_2)
    assert action_1.queue == "spot_soon"
    assert action_2.queue == "dedicated_soon"
    assert await batch_dal.is_action_by_key(key=action_1.key)
    assert await batch_dal.is_action_by_key(key=action_2.key)
    assert await batch_dal.delete_action(
        action_name="report",
        additional_info="XLS",
        entity="oneshottest",
        subject="integratesmanager@gmail.com",
        time=time,
    )
    assert await batch_dal.delete_action(
        action_name="handle_virus_scan",
        entity="file_name",
        subject="integratesmanager@gmail.com",
        additional_info="oneshottest",
        time=time,
    )
    assert not await batch_dal.is_action_by_key(key=action_1.key)
    assert not await batch_dal.is_action_by_key(key=action_2.key)
