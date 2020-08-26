# -*- coding: utf-8 -*-
"""This module allows to check Password and other text vulnerabilities."""

# standard imports
import pkg_resources

# 3rd party imports
# None

# local imports
from fluidasserts import SAST, LOW, MEDIUM, HIGH, _get_result_as_tuple_sast
from fluidasserts.utils.decorators import unknown_if, api


@unknown_if(FileNotFoundError)
def _check_password_strength(password: str, length: int) -> tuple:
    """
    Check if a user password is secure.

    A user password is considered secured if following criteria are met:

    - Password length must be at least the given parameter ``length``.
    - Password must contain at least one uppercase character,
      one lowercase character, one number and one special character.
    - Password must not be a typical dictionary word.

    :param password: String to be tested.
    :param length: Minimum accepted password length.
    :returns: False if all conditions are met (secure),
    True otherwise (insecure).
    """
    static_path = pkg_resources.resource_filename('fluidasserts', 'static/')
    dictionary = static_path + 'wordlists/password.lst'

    caps = sum(1 for c in password if c.isupper())
    lower = sum(1 for c in password if c.islower())
    nums = sum(1 for c in password if c.isdigit())
    special = sum(1 for c in password if not c.isalnum())
    spaces = sum(1 for c in password if c.isspace())

    with open(dictionary) as dict_fd:
        words = (x.rstrip() for x in dict_fd.readlines())

    msg_open: str = 'Password is insecure'
    is_password_secure: bool = False

    if len(password) < length:
        msg_open = 'Password is too short'
    elif password in words:
        msg_open = 'Password is a dictionary password'
    elif caps < 1 or lower < 1 or nums < 1 or special < 1 or spaces < 1:
        msg_open = 'Password is too weak'
    else:
        is_password_secure = True

    return _get_result_as_tuple_sast(
        path=f'Password/{password}',
        msg_open=msg_open,
        msg_closed='Password is secure',
        open_if=not is_password_secure)


@api(risk=HIGH, kind=SAST)
def is_user_password_insecure(password: str) -> tuple:
    """
    Check if a user password is insecure.

    A user password is considered secure if it is at least
    8 characters long and satisfies all other password criteria.

    :param password: Password to be tested.
    :returns: True if password insecure, False if secure.
    """
    min_password_len = 12

    return _check_password_strength(password, min_password_len)


@api(risk=HIGH, kind=SAST)
def is_system_password_insecure(password: str) -> tuple:
    """
    Check if a system password is insecure.

    A system password is considered secure if it is at least
    20 characters long and satisfies all other password criteria.

    :param password: Password to be tested.
    :returns: True if password insecure, False if secure.
    """
    min_password_len = 24

    return _check_password_strength(password, min_password_len)


@api(risk=MEDIUM, kind=SAST)
def is_otp_token_insecure(password: str) -> tuple:
    """
    Check if a one-time password token is insecure.

    A one-time password token is considered secure if it is at least
    6 characters long.

    :param password: Password to be tested.
    :returns: True if insecure, False if secure.
    """
    min_password_len: int = 6

    return _get_result_as_tuple_sast(
        path=f'OTP/{password}',
        msg_open='OTP Token is too short',
        msg_closed='OTP Token length is enough',
        open_if=len(password) < min_password_len)


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def is_ssid_insecure(ssid: str) -> tuple:
    """
    Check if a given SSID is insecure.

    An SSID is considered secure if it is not a typical dictionary
    word such as "home" or "network".

    :param ssid: SSID to be tested.
    :returns: True if insecure, False if secure.
    """
    static_path = pkg_resources.resource_filename('fluidasserts', 'static/')
    dictionary = static_path + 'wordlists/password.lst'

    with open(dictionary) as dict_fd:
        words = (x.rstrip() for x in dict_fd.readlines())

    return _get_result_as_tuple_sast(
        path=f'SSID/{ssid}',
        msg_open='OTP Token is too short',
        msg_closed='OTP Token length is enough',
        open_if=ssid in words)
