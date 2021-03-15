# Standard libraries
import pytest

# Local libraries
from batch import dal as batch_dal


pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_actions() -> None:
    all_actions = await batch_dal.get_actions()
    assert isinstance(all_actions, list)
    assert len(all_actions) == 1


async def test_get_action() -> None:
    action = await batch_dal.get_action(
        action_name='report',
        additional_info='XLS',
        entity='unittesting',
        subject='integratesmanager@gmail.com',
        time='1615834776'
    )
    assert bool(action)

    optional_action = await batch_dal.get_action(
        action_name='report',
        additional_info='PDF',
        entity='continuoustesting',
        subject='integratesmanager@gmail.com',
        time='1615834776'
    )
    assert not bool(optional_action)
