import pytest
from datetime import timedelta
from time import time

from back import settings
from newutils import token as token_utils

AGE_WEEKS = 27  # invalid expiration time


def test_verificate_hash_token():
    token = token_utils.calculate_hash_token()
    access_token = {"salt": token["salt"], "jti": token["jti_hashed"]}
    different_token = token_utils.calculate_hash_token()

    assert token_utils.verificate_hash_token(access_token, token["jti"])
    assert not token_utils.verificate_hash_token(
        access_token, different_token["jti"]
    )


def test_is_valid_expiration_time():
    exp_valid = int(time()) + settings.SESSION_COOKIE_AGE
    exp_invalid = int(time() + timedelta(weeks=AGE_WEEKS).total_seconds())

    assert token_utils.is_valid_expiration_time(exp_valid)
    assert not token_utils.is_valid_expiration_time(exp_invalid)
