import pytest

from backend.dal.event import (
    update, get_event
)


@pytest.mark.changes_db
def test_update():
    assert get_event('418900979').get('action_before_blocking', '') == \
        'TEST_OTHER_PART_TOE'

    update('418900979', {'action_before_blocking': None})
    assert get_event('418900979').get('action_before_blocking', '') == ''

    update('418900979', {'action_before_blocking': 'TEST_OTHER_PART_TOE'})
    assert get_event('418900979').get('action_before_blocking', '') == \
        'TEST_OTHER_PART_TOE'
