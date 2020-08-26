# -*- coding: utf-8 -*-

"""Modulo para pruebas de cadenas.

Este modulo contiene las funciones necesarias para probar si el modulo de
strings se encuentra adecuadamente implementado.
"""

# standard imports
# None

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('format')

# local imports
from fluidasserts.format import string


# Constants

WEAK_USER_PASS = 'P@ssw0rd1.'
WEAKER_PASS = 'passwordpassword'
DICT_PASS = 'winniethepooh'
STRONG_USER_PASS = 'P@ssw0rd1. P@ssw0rd1.'
WEAK_SYSTEM_PASS = 'system_password'
STRONG_SYSTEM_PASS = 'P@ssw0rd1. P@ssw0rd1. P@ssw0rd1. P@ssw0rd1.'
WEAK_OTP = '123a'
STRONG_OTP = '123abc'
WEAK_SSID = 'network'
STRONG_SSID = 'S3cur3SSID'

#
# Open tests
#


def test_user_password_open():
    """Weak user password?."""
    assert string.is_user_password_insecure(WEAK_USER_PASS)
    assert string.is_user_password_insecure(DICT_PASS)
    assert string.is_user_password_insecure(WEAKER_PASS)
    assert string.is_user_password_insecure(WEAK_USER_PASS+'3')


def test_system_password_open():
    """Weak system password?."""
    assert string.is_system_password_insecure(WEAK_SYSTEM_PASS)


def test_otp_token_open():
    """Weak OTP token?."""
    assert string.is_otp_token_insecure(WEAK_OTP)


def test_ssid_insecure_open():
    """Weak SSID string?."""
    assert string.is_ssid_insecure(WEAK_SSID)


#
# Closing tests
#


def test_user_password_close():
    """Strong user password?."""
    assert not string.is_user_password_insecure(STRONG_USER_PASS)


def test_system_password_close():
    """Strong system password?."""
    assert not string.is_system_password_insecure(STRONG_SYSTEM_PASS)


def test_otp_token_close():
    """Strong OTP token?."""
    assert not string.is_otp_token_insecure(STRONG_OTP)


def test_ssid_insecure_close():
    """Strong SSID string?."""
    assert not string.is_ssid_insecure(STRONG_SSID)
