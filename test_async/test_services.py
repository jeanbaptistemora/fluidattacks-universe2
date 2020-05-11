import pytest

from django.test import TestCase

from backend.exceptions import (
    FindingNotFound
)
from backend.services import (
    is_registered,
    has_access_to_finding,
    has_access_to_event,
    has_valid_access_token
)

class ServicesTests(TestCase):

    @pytest.mark.no_changes_db
    def test_is_registered(self):
        wrong_user = ['unregistered', 'user0000', '1111000','user>**']
        right_user = 'unittest'
        for user in wrong_user:
            assert not is_registered(user)
        assert is_registered(right_user)

    @pytest.mark.no_changes_db
    def test_has_access_to_finding(self):
        wrong_data = ['unittest@fluidattacks.com', '000000000']
        right_data = ['unittest@fluidattacks.com', '560175507']
        with self.assertRaises(FindingNotFound):
            has_access_to_finding(wrong_data[0], wrong_data[1])
        assert has_access_to_finding(right_data[0], right_data[1])

    @pytest.mark.no_changes_db
    def test_has_access_to_event(self):
        assert has_access_to_event('unittest@fluidattacks.com', '418900971')

    @pytest.mark.no_changes_db
    def test_has_valid_access_token(self):
        jti = 'ff6273146a0e4ed82715cdb4db7f5915b30dfa4bccc54c0d2cda17a61a44a5f6'
        assert has_valid_access_token(
            'unittest@fluidattacks.com', {'test_context': 'test_context_value'}, jti)
