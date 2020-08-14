import pytest

from django.test import TestCase

from backend.exceptions import (
    FindingNotFound
)
from backend.services import (
    has_access_to_finding,
    has_access_to_event,
    has_valid_access_token
)

pytestmark = [
    pytest.mark.asyncio,
]


class ServicesTests(TestCase):

    async def test_has_access_to_finding(self):
        wrong_data = ['unittest@fluidattacks.com', '000000000']
        right_data = ['unittest@fluidattacks.com', '560175507']
        with self.assertRaises(FindingNotFound):
            await has_access_to_finding(wrong_data[0], wrong_data[1])
        assert await has_access_to_finding(right_data[0], right_data[1])

    async def test_has_access_to_event(self):
        assert await has_access_to_event('unittest@fluidattacks.com', '418900971')

    async def test_has_valid_access_token(self):
        jti = 'ff6273146a0e4ed82715cdb4db7f5915b30dfa4bccc54c0d2cda17a61a44a5f6'
        assert await has_valid_access_token(
            'unittest@fluidattacks.com', {'test_context': 'test_context_value'}, jti)
