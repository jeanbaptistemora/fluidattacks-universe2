import pytest

from boto3.dynamodb.conditions import Attr, Key, Not
from asgiref.sync import async_to_sync
from backend.dal.user import (
    delete, get, create, update
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_delete():
    test_1 = 'unittest3'
    assert {
            'company' : 'unittest', 'date_joined': '2017-12-28 23:54:55',
            'last_login': '2019-10-29 13:40:37', 'email' : 'unittest3',
            'legal_remember' : True,
            'organization': 'ORG#6ee4c12b-7881-4490-a851-07357fff1d64',
            'registered' : False
        } == await get(test_1)
    assert await delete(test_1)
    assert {} == await get(test_1)

@pytest.mark.changes_db
async def test_create():
    assert await get('unittest4') == {}

    await create('unittest4', {'phone_number': '11111111'})
    assert await get('unittest4') == \
        {'email': 'unittest4', 'phone_number': '11111111'}

@pytest.mark.changes_db
async def test_update():
    assert await get('unittest5') == {}

    await create('unittest5', {'phone_number': '22222222'})
    await update('unittest5', {})
    assert await get('unittest5') == \
        {'email': 'unittest5', 'phone_number': '22222222'}

    await update('unittest5', {'last_name':'testing'})
    assert await get('unittest5') == \
        {'last_name':'testing', 'email': 'unittest5', 'phone_number': '22222222'}
