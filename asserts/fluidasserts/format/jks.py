# -*- coding: utf-8 -*-

"""This module allows to check ``JKS`` vulnerabilities."""

# standard imports
import os
from typing import List

# 3rd party imports
import jks

# local imports
from fluidasserts import Unit, SAST, HIGH, CLOSED, OPEN, UNKNOWN
from fluidasserts.utils.generic import get_paths, get_sha256
from fluidasserts.utils.decorators import api


@api(risk=HIGH, kind=SAST)
def has_no_password_protection(path: str) -> tuple:
    """
    Check if .jks files are password protected.

    :param path: path to check
    :rtype: :class:`fluidasserts.Result`
    """
    if not os.path.exists(path):
        return UNKNOWN, 'Path does not exist'

    msg_open: str = 'Keystore is not password protected'
    msg_closed: str = 'Keystore is password protected'

    safes: List[Unit] = []
    vulns: List[Unit] = []
    for full_path in get_paths(path, endswith=('.jks', '.bks',)):
        vulnerable: bool = True
        try:
            if full_path.endswith('.jks'):
                jks.KeyStore.load(full_path, '')
            elif full_path.endswith('.bks'):
                jks.BksKeyStore.load(full_path, '')
        except jks.util.KeystoreSignatureException:
            vulnerable = False

        (vulns if vulnerable else safes).append(
            Unit(where=path,
                 source='JKS/Password',
                 specific=[msg_open if vulnerable else msg_closed],
                 fingerprint=get_sha256(path)))

    if vulns:
        return OPEN, msg_open, vulns, safes
    return CLOSED, msg_closed, vulns, safes


def _use_passwords(path: str, passwords: list) -> tuple:
    """
    Check if a JKS file has been protected by any of ``passwords``.

    :param path: path to check
    :param passwords: passwords to test
    """
    if not os.path.exists(path):
        return UNKNOWN, 'Path does not exist'

    msg_open: str = 'Keystore is protected by a weak password'
    msg_closed: str = 'Keystore is protected by a strong password'

    safes: List[Unit] = []
    vulns: List[Unit] = []

    passwords = ['', *(p for p in set(passwords))]

    for full_path in get_paths(path, endswith=('.jks', '.bks',)):
        vulnerable: bool = False
        for password in passwords:
            try:
                if full_path.endswith('.jks'):
                    jks.KeyStore.load(full_path, password)
                elif full_path.endswith('.bks'):
                    jks.BksKeyStore.load(full_path, password)
            except jks.util.KeystoreSignatureException:
                # wrong password
                continue
            else:
                # correct password
                vulnerable = True
                break

        (vulns if vulnerable else safes).append(
            Unit(where=path,
                 source='JKS/Password',
                 specific=[msg_open if vulnerable else msg_closed],
                 fingerprint=get_sha256(path)))

    if vulns:
        return OPEN, msg_open, vulns, safes
    return CLOSED, msg_closed, vulns, safes


@api(risk=HIGH, kind=SAST)
def use_password(path: str, password: str) -> tuple:
    """
    Check if a JKS file has been protected by ``password``.

    :param path: path to check
    :param password: password to test
    :rtype: :class:`fluidasserts.Result`
    """
    return _use_passwords(path, [password])


@api(risk=HIGH, kind=SAST)
def use_passwords(path: str, passwords: list) -> tuple:
    """
    Check if a JKS file has been protected by any of ``passwords``.

    :param path: path to check
    :param passwords: passwords to test
    :rtype: :class:`fluidasserts.Result`
    """
    return _use_passwords(path, passwords)
