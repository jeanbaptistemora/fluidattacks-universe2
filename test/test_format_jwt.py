# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.code.java."""

# standard imports
import secrets
import datetime

# 3rd party imports
from jwt import encode
import pytest
pytestmark = pytest.mark.format

# local imports
from fluidasserts.format import jwt


# Constants

KEY_WEAK = 'secret'
KEY_STRONG = secrets.token_hex(32)

SECONDS_IN_10_MIN = 600
SECONDS_IN_24_HOURS = 86400

UTCNOW = datetime.datetime.utcnow()
DELTA_10_MIN = datetime.timedelta(seconds=SECONDS_IN_10_MIN)
DELTA_24_HOURS = datetime.timedelta(seconds=SECONDS_IN_24_HOURS)

NOT_A_TOKEN = 'this will Raise Errors'

#
# Open tests
#


def test_has_insecure_expiration_time_open():
    """token has an insecure expiration time."""
    tests = [
        {},
        {'iat': UTCNOW},
        {'exp': UTCNOW + DELTA_24_HOURS},
        {'iat': UTCNOW, 'exp': UTCNOW + DELTA_24_HOURS},
    ]
    for claimset in tests:
        token = encode(claimset, KEY_STRONG, algorithm='HS256').decode()
        assert jwt.has_insecure_expiration_time(token, SECONDS_IN_10_MIN)


#
# Closing tests
#


def test_has_insecure_expiration_time_close():
    """Search DES encryption algorithm."""
    tests = [
        {'iat': UTCNOW, 'exp': UTCNOW + DELTA_10_MIN},
    ]
    for claimset in tests:
        token = encode(claimset, KEY_STRONG, algorithm='HS256').decode()
        assert not jwt.has_insecure_expiration_time(token, SECONDS_IN_10_MIN)

    assert not jwt.has_insecure_expiration_time(NOT_A_TOKEN, SECONDS_IN_10_MIN)
