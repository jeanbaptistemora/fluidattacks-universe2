from datetime import datetime, timedelta
import pytz

import pytest

from back import settings
from backend.exceptions import InvalidPushToken
from users import domain as users_domain


@pytest.mark.changes_db
async def test_add_push_token():
    user_email = 'test@mail.com'
    with pytest.raises(InvalidPushToken):
        assert await users_domain.add_push_token(
            user_email, 'not-a-push-token')

    valid_token = 'ExponentPushToken[something123]'
    assert await users_domain.add_push_token(
        user_email, valid_token)

    user_attrs = await users_domain.get_attributes(
        user_email, ['push_tokens'])
    assert 'push_tokens' in user_attrs
    assert valid_token in user_attrs['push_tokens']

@pytest.mark.changes_db
async def test_remove_push_token():
    user_email = 'unittest@fluidattacks.com'
    token = 'ExponentPushToken[dummy]'

    attrs_before = await users_domain.get_attributes(
        user_email, ['push_tokens'])
    assert 'push_tokens' in attrs_before
    assert token in attrs_before['push_tokens']

    assert await users_domain.remove_push_token(user_email, token)

    attrs_after = await users_domain.get_attributes(
        user_email, ['push_tokens'])
    assert token not in attrs_after['push_tokens']
