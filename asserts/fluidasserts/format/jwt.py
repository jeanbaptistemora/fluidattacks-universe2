# -*- coding: utf-8 -*-

"""This module allows to check ``JWT`` vulnerabilities."""

# 3rd party imports
from jwt import decode
from jwt.exceptions import InvalidTokenError

# local imports
from fluidasserts import SAST, LOW, _get_result_as_tuple_sast
from fluidasserts.utils.decorators import unknown_if, api


@api(risk=LOW, kind=SAST)
@unknown_if(InvalidTokenError)
def has_insecure_expiration_time(
        jwt_token: str, max_expiration_time: int = 600) -> tuple:
    """
    Check if the given JWT has an insecure expiration time.

    :param jwt_token: JWT to test.
    :param max_expiration_time: According to the bussiness rule, (in seconds).
    """
    claimset = decode(jwt_token, verify=False)

    iat = claimset.get('iat')
    exp = claimset.get('exp')

    msg_open: str = 'Token has an insecure expiration time'
    msg_closed: str = 'Token has a secure expiration time'

    missing_iat_or_exp: bool = False

    if not iat or not exp:
        missing_iat_or_exp = True
        msg_open = 'Token does not include iat or exp claims'
    else:
        expiration_time: float = (exp - iat)

    return _get_result_as_tuple_sast(
        path='JWT/token',
        msg_open=msg_open, msg_closed=msg_closed,
        open_if=missing_iat_or_exp or expiration_time > max_expiration_time,
        fingerprint={'claimset': claimset})
