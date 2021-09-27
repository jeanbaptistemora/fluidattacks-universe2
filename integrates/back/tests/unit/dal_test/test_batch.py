from aioextensions import (
    collect,
)
from batch import (
    dal as batch_dal,
)
from batch.types import (
    BatchProcessing,
)
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
    assert len(all_actions) == 3


async def test_get_action() -> None:
    action = await batch_dal.get_action(
        action_name="report",
        additional_info="XLS",
        entity="unittesting",
        subject="integratesmanager@gmail.com",
        time="1615834776",
    )
    assert bool(action)

    optional_action = await batch_dal.get_action(
        action_name="report",
        additional_info="PDF",
        entity="continuoustesting",
        subject="integratesmanager@gmail.com",
        time="1615834776",
    )
    assert not bool(optional_action)


async def test_requeue_actions() -> None:
    pending_actions: List[BatchProcessing] = await batch_dal.get_actions()

    assert all(
        await collect(
            [
                batch_dal.put_action_to_batch(
                    action_name=action.action_name,
                    entity=action.entity,
                    subject=action.subject,
                    time=action.time,
                    additional_info=action.additional_info,
                    queue=action.queue,
                )
                for action in pending_actions
            ],
            workers=20,
        )
    )


@pytest.mark.changes_db
async def test_put_action_to_dynamodb() -> None:
    time = str(get_as_epoch(get_now()))
    assert await batch_dal.put_action_to_dynamodb(
        action_name="report",
        entity="oneshottest",
        subject="integratesmanager@gmail.com",
        time=time,
        additional_info="XLS",
    )
    assert await batch_dal.put_action_to_dynamodb(
        action_name="handle_virus_scan",
        entity="file_name",
        subject="integratesmanager@gmail.com",
        additional_info="oneshottest",
        time=time,
        queue="dedicated_soon",
    )

    action = await batch_dal.get_action(
        action_name="report",
        additional_info="XLS",
        entity="oneshottest",
        subject="integratesmanager@gmail.com",
        time=time,
    )

    virus_action = await batch_dal.get_action(
        action_name="handle_virus_scan",
        entity="file_name",
        subject="integratesmanager@gmail.com",
        additional_info="oneshottest",
        time=time,
    )
    assert action.queue == "spot_soon"
    assert virus_action.queue == "dedicated_soon"
    assert await batch_dal.is_action_by_key(key=action.key)
    assert await batch_dal.is_action_by_key(key=virus_action.key)
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
    assert not await batch_dal.is_action_by_key(key=action.key)
    assert not await batch_dal.is_action_by_key(key=virus_action.key)
