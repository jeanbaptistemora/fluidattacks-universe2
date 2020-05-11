import pytest
from time import time

from datetime import timedelta
from django.conf import settings
from django.test import TestCase

from backend.util import (
    calculate_hash_token, is_valid_expiration_time, verificate_hash_token)

AGE_WEEKS = 27  # invalid expiration time


class AcessTokenTest(TestCase):

    @pytest.mark.no_changes_db
    def test_verificate_hash_token(self):
        token = calculate_hash_token()
        access_token = {
            'salt': token['salt'],
            'jti': token['jti_hashed']
        }
        different_token = calculate_hash_token()

        assert verificate_hash_token(access_token, token['jti'])
        assert not verificate_hash_token(
            access_token, different_token['jti'])

    @pytest.mark.no_changes_db
    def test_is_valid_expiration_time(self):
        exp_valid = int(time()) + settings.SESSION_COOKIE_AGE
        exp_invalid = int(time() + timedelta(weeks=AGE_WEEKS).total_seconds())

        assert is_valid_expiration_time(exp_valid)
        assert not is_valid_expiration_time(exp_invalid)
