# -*- coding: utf-8 -*-
"""This module allows to check ``PKCS12`` vulnerabilities."""

# standard imports
from typing import List

# 3rd party imports
from OpenSSL import crypto

# local imports
from fluidasserts import SAST, HIGH, OPEN, CLOSED, Unit
from fluidasserts.utils.decorators import unknown_if, api
from fluidasserts.utils.generic import get_paths, get_sha256


@api(risk=HIGH, kind=SAST)
@unknown_if(FileNotFoundError)
def has_no_password_protection(path: str) -> tuple:
    """
    Check if a PKCS 12 file is password protected.

    :param path: path to check.
    """
    msg_open: str = 'File is not password protected'
    msg_closed: str = 'File is password protected'

    safes: List[Unit] = []
    vulns: List[Unit] = []

    for full_path in get_paths(
            path, endswith=(
                '.p12',
                '.pfx',
            )):
        vulnerable = True
        try:
            with open(full_path, 'rb') as p12_file_handle:
                crypto.load_pkcs12(p12_file_handle.read())
        except crypto.Error:
            vulnerable = False

        (vulns if vulnerable else safes).append(
            Unit(
                where=full_path,
                source='PKCS 12/Password',
                specific=[msg_open if vulnerable else msg_closed],
                fingerprint=get_sha256(path)))
    if vulns:
        return OPEN, msg_open, vulns, safes
    return CLOSED, msg_closed, vulns, safes


@api(risk=HIGH, kind=SAST)
@unknown_if(FileNotFoundError)
def use_passwords(path: str, passwords: List):
    """
    Check if a PKCS 12 file has been protected by any of ``passwords``.

    :param path: path to check
    :param passwords: passwords to test
    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'PKCS is protected by a weak password'
    msg_closed: str = 'PKCS is protected by a strong password'

    safes: List[Unit] = []
    vulns: List[Unit] = []

    passwords = ['', *(p for p in set(passwords))]

    for full_path in get_paths(
            path, endswith=(
                '.p12',
                '.pfx',
            )):
        vulnerable = False
        for password in passwords:
            try:
                with open(full_path, 'rb') as p12_file_handle:
                    crypto.load_pkcs12(p12_file_handle.read(), password)
            except crypto.Error:
                continue
            else:
                vulnerable = True
                break

        (vulns if vulnerable else safes).append(
            Unit(
                where=full_path,
                source='PKCS 12/Password',
                specific=[msg_open if vulnerable else msg_closed],
                fingerprint=get_sha256(path)))
    if vulns:
        return OPEN, msg_open, vulns, safes
    return CLOSED, msg_closed, vulns, safes
