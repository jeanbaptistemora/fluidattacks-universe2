from time import time
import pytest
from aniso8601 import parse_datetime

from backend.domain import event as event_domain
from backend.exceptions import EventAlreadyClosed, InvalidCommentParent


def test_get_event():
    event_id = '418900971'
    test_data = event_domain.get_event(event_id)
    expected_output = 'unittesting'
    assert test_data.get('project_name') == expected_output


def test_create_event():
    attrs = {
        'action_after_blocking': 'TRAINING',
        'action_before_blocking': 'DOCUMENT_PROJECT',
        'accessibility': 'REPOSITORY',
        'analyst_email': 'unittesting@fluidattacks.com',
        'context': 'OTHER',
        'detail': 'Something happened.',
        'event_date': parse_datetime('2019-12-09T05:00:00.000Z'),
        'event_type': 'CLIENT_DETECTS_ATTACK',
        'project_name': 'unittesting'
    }
    assert event_domain.create_event(**attrs)


def test_solve_event():
    assert event_domain.solve_event(
        event_id='538745942',
        affectation=1,
        analyst_email='unittesting@fluidattacks.com',
        date=parse_datetime('2019-12-09T05:00:00.000Z'))
    event = event_domain.get_event('538745942')
    assert event['historic_state'][-1]['state'] == 'SOLVED'
    with pytest.raises(EventAlreadyClosed):
        assert event_domain.solve_event(
            event_id='538745942',
            affectation=1,
            analyst_email='unittesting@fluidattacks.com',
            date=parse_datetime('2019-12-09T05:00:00.000Z'))


def test_add_comment():
    comment_id = int(round(time() * 1000))
    comment_id, success = event_domain.add_comment(
        comment_id=comment_id,
        content='comment test',
        event_id='538745942',
        parent='0',
        user_info={
            'user_email': 'unittesting@fluidattacks.com',
            'first_name': 'Unit',
            'last_name': 'test'
        })
    assert success
    assert comment_id

    comment_id, success = event_domain.add_comment(
        comment_id=int(round(time() * 1000)),
        content='comment test 2',
        event_id='538745942',
        parent=str(comment_id),
        user_info={
            'user_email': 'unittesting@fluidattacks.com',
            'first_name': 'Unit',
            'last_name': 'test'
        })
    assert success
    assert comment_id

    with pytest.raises(InvalidCommentParent):
        assert event_domain.add_comment(
            comment_id=int(round(time() * 1000)),
            content='comment test 2',
            event_id='538745942',
            parent=str(comment_id + 1),
            user_info={
                'user_email': 'unittesting@fluidattacks.com',
                'first_name': 'Unit',
                'last_name': 'test'
            })
