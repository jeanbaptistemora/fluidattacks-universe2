from datetime import datetime, timedelta
import pytz
import pytest

from django.conf import settings
from django.test import TestCase
from backend.domain import user as user_domain
from backend.exceptions import InvalidPushToken


class UserTests(TestCase):
    def test_get_current_date(self):
        tzn = pytz.timezone(settings.TIME_ZONE)
        today = datetime.now(tz=tzn).today()
        date = today.strftime('%Y-%m-%d %H:%M')
        test_data = user_domain.get_current_date()[:-3]
        assert isinstance(test_data, str)
        assert test_data == date

    @pytest.mark.changes_db
    async def test_add_push_token(self):
        user_email = 'test@mail.com'
        with pytest.raises(InvalidPushToken):
            assert await user_domain.add_push_token(
                user_email, 'not-a-push-token')

        valid_token = 'ExponentPushToken[something123]'
        assert await user_domain.add_push_token(
            user_email, valid_token)

        user_attrs = await user_domain.get_attributes(
            user_email, ['push_tokens'])
        assert 'push_tokens' in user_attrs
        assert valid_token in user_attrs['push_tokens']

    @pytest.mark.changes_db
    async def test_remove_push_token(self):
        user_email = 'unittest@fluidattacks.com'
        token = 'ExponentPushToken[dummy]'

        attrs_before = await user_domain.get_attributes(
            user_email, ['push_tokens'])
        assert 'push_tokens' in attrs_before
        assert token in attrs_before['push_tokens']

        assert await user_domain.remove_push_token(user_email, token)

        attrs_after = await user_domain.get_attributes(
            user_email, ['push_tokens'])
        assert token not in attrs_after['push_tokens']
