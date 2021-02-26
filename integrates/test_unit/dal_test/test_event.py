import pytest

from backend.events.dal import (
    get_event,
    update
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_update():
    event = await get_event('418900979')
    assert event.get('action_before_blocking', '') == 'TEST_OTHER_PART_TOE'

    await update('418900979', {'action_before_blocking': None})
    event = await get_event('418900979')
    assert event.get('action_before_blocking', '') == ''

    await update(
        '418900979',
        {'action_before_blocking': 'TEST_OTHER_PART_TOE'}
    )
    event = await get_event('418900979')
    assert event.get('action_before_blocking', '') == 'TEST_OTHER_PART_TOE'
