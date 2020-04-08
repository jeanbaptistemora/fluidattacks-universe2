from django.test import TestCase
from backend.services import (
    is_registered,
    has_valid_access_token
)

class ServicesTests(TestCase):

    def test_is_registered(self):
        assert is_registered('unittest')

    def test_has_valid_access_token(self):
        jti = 'ff6273146a0e4ed82715cdb4db7f5915b30dfa4bccc54c0d2cda17a61a44a5f6'
        assert has_valid_access_token(
            'unittest@fluidattacks.com', {'test_context': 'test_context_value'}, jti)
