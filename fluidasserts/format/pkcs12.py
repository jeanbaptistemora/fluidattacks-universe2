# -*- coding: utf-8 -*-

"""This module allows to check ``PKCS12`` vulnerabilities."""

# standard imports
from contextlib import suppress

# 3rd party imports
from OpenSSL import crypto

# local imports
from fluidasserts import SAST, HIGH, _get_result_as_tuple_sast
from fluidasserts.utils.decorators import unknown_if, api


@api(risk=HIGH, kind=SAST)
@unknown_if(FileNotFoundError)
def has_no_password_protection(p12_file: str) -> tuple:
    """
    Check if a .p12 file is password protected.

    :param p12_file: .p12 file to check
    """
    is_password_protected: bool = True
    with suppress(crypto.Error):
        with open(p12_file, 'rb') as p12_file_handle:
            crypto.load_pkcs12(p12_file_handle.read())
            is_password_protected = False

    return _get_result_as_tuple_sast(
        path=p12_file,
        msg_open='File is not password protected',
        msg_closed='File is password protected',
        open_if=not is_password_protected)
