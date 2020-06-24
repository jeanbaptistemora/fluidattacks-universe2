import pytest

from asgiref.sync import async_to_sync
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from operator import itemgetter

from backend.dal.session import (
    get_all_logged_users, get_previous_session,
    invalidate_session
)
from test_async.utils import create_dummy_simple_session


def _test_get_all_logged_users():
    def unpack_sessions(active_users):
        return sorted(
            [tuple(*a_user.items()) for a_user in active_users],
            key = itemgetter(1)
        )

    for session in unpack_sessions(get_all_logged_users()):
        invalidate_session(session[1])
    assert not bool(get_all_logged_users())

    create_dummy_simple_session('unittest', 'unittest')
    create_dummy_simple_session('unittest2', 'unittest2')
    users, _ = zip(*unpack_sessions(get_all_logged_users()))
    assert sorted(users) == ['unittest', 'unittest2']

def _test_get_previous_session():
    def unpack_sessions(active_users):
        return sorted(
            [tuple(*a_user.items()) for a_user in active_users],
            key = itemgetter(1)
        )

    for session in unpack_sessions(get_all_logged_users()):
        invalidate_session(session[1])
    assert not bool(get_all_logged_users())

    test_1 = [
        create_dummy_simple_session(
            f'unittest{i}', f'unittest{i}').session.session_key
        for i in range(5)]
    assert len(get_all_logged_users()) == len(test_1)

    assert not bool(get_previous_session('unittest4', test_1[-1]))

    assert \
        f'fi_session:{test_1[-1]}' == \
        get_previous_session(
            'unittest4',
            create_dummy_simple_session(
                'unittest4', 'unittest4').session.session_key)

def _test_invalidate_session():
    def unpack_sessions(active_users):
        return sorted(
            [tuple(*a_user.items()) for a_user in active_users],
            key = itemgetter(1)
        )

    for session in unpack_sessions(get_all_logged_users()):
        invalidate_session(session[1])
    assert not bool(get_all_logged_users())

    all_active_sessions = sorted(
        [create_dummy_simple_session(
            f'unittest{i}', f'unittest{i}').session.session_key
        for i in range(20)]
    )
    all_active_sessions = [f'fi_session:{s}' for s in all_active_sessions]
    assert len(get_all_logged_users()) == len(all_active_sessions)

    index_for_test = (0, 2, 5, 6, 9, 12, 18)
    expected = [all_active_sessions[index] \
        for index in range(len(all_active_sessions)) \
            if index not in index_for_test]
    test_1 = [all_active_sessions[index] \
        for index in range(len(all_active_sessions)) \
            if index in index_for_test]
    for to_invalidate in test_1:
        invalidate_session(to_invalidate)
    _, result_1 = zip(*unpack_sessions(get_all_logged_users()))
    assert sorted(result_1) == expected

@pytest.mark.changes_sessions
def test_sessions():
    _test_get_all_logged_users()
    _test_get_previous_session()
    _test_invalidate_session()
