from back.tests.unit import (
    MIGRATION,
)
from batch import (
    dal as batch_dal,
)
from newutils.datetime import (
    get_as_epoch,
    get_now,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.skipif(MIGRATION, reason="Finding migration")
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

    action = await batch_dal.get_action(
        action_name="report",
        additional_info="XLS",
        entity="oneshottest",
        subject="integratesmanager@gmail.com",
        time=time,
    )
    assert await batch_dal.is_action_by_key(key=action.key)
    assert await batch_dal.delete_action(
        action_name="report",
        additional_info="XLS",
        entity="oneshottest",
        subject="integratesmanager@gmail.com",
        time=time,
    )
    assert not await batch_dal.is_action_by_key(key=action.key)
