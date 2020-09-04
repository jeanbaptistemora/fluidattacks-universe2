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

pytestmark = [
    pytest.mark.asyncio,
]

async def _test_get_all_logged_users():
    for session in await get_all_logged_users():
        await invalidate_session(session['key'])
    assert not bool(await get_all_logged_users())

    create_dummy_simple_session('unittest')
    create_dummy_simple_session('unittest2')
    users = [session['username'] for session in await get_all_logged_users()]
    assert sorted(users) == ['unittest', 'unittest2']

async def _test_get_previous_session():
    for session in await get_all_logged_users():
        await invalidate_session(session['key'])
    assert not bool(await get_all_logged_users())

    test_1 = [
        create_dummy_simple_session(
            f'unittest{i}').session.session_key
        for i in range(5)]
    assert len(await get_all_logged_users()) == len(test_1)

    create_dummy_simple_session('unittest4', 'mobile')
    assert len(await get_all_logged_users()) == len(test_1) + 1
    assert not bool(await get_previous_session('unittest4', test_1[-1]))

    assert \
        f'fi_session:{test_1[-1]}' == \
        await get_previous_session(
            'unittest4',
            create_dummy_simple_session(
                'unittest4').session.session_key)

async def _test_invalidate_session():
    for session in await get_all_logged_users():
        await invalidate_session(session['key'])
    assert not bool(await get_all_logged_users())

    all_active_sessions = sorted(
        [create_dummy_simple_session(
            f'unittest{i}').session.session_key
        for i in range(20)]
    )
    all_active_sessions = [f'fi_session:{s}' for s in all_active_sessions]
    assert len(await get_all_logged_users()) == len(all_active_sessions)

    index_for_test = (0, 2, 5, 6, 9, 12, 18)
    expected = [all_active_sessions[index] \
        for index in range(len(all_active_sessions)) \
            if index not in index_for_test]
    test_1 = [all_active_sessions[index] \
        for index in range(len(all_active_sessions)) \
            if index in index_for_test]
    for to_invalidate in test_1:
        await invalidate_session(to_invalidate)
    result_1 = [session['key'] for session in await get_all_logged_users()]
    assert sorted(result_1) == expected


@pytest.mark.changes_sessions
async def test_sessions():
    await _test_get_all_logged_users()
    await _test_get_previous_session()
    await _test_invalidate_session()
