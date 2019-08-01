# -*- coding: utf-8 -*-

"""This module allows to check ``JKS`` vulnerabilities."""


# standard imports
import os

# 3rd party imports
import jks

# local imports
from fluidasserts import show_open
from fluidasserts import show_close
from fluidasserts import show_unknown
from fluidasserts.utils.generic import get_sha256
from fluidasserts.utils.generic import get_paths
from fluidasserts.utils.decorators import track, level, notify


@notify
@level('high')
@track
def has_no_password_protection(path: str) -> bool:
    """
    Check if .jks files are password protected.

    :param path: path to check
    """
    if not os.path.exists(path):
        show_unknown('Path does not exist',
                     details=dict(path=path))
        return False
    jks_with_password: list = []
    jks_without_password: list = []
    for full_path in get_paths(path, endswith=('.jks',)):
        try:
            jks.KeyStore.load(full_path, '')
        except jks.util.KeystoreSignatureException:
            # has password
            jks_with_password.append(dict(path=full_path,
                                          sha256=get_sha256(full_path)))
        else:
            # has not password
            jks_without_password.append(dict(path=full_path,
                                             sha256=get_sha256(full_path)))
    if jks_without_password:
        show_open('JKS is/are not password protected',
                  details=dict(jks_without_password=jks_without_password))
        return True
    show_close('JKS is/are password protected',
               details=dict(jks_with_password=jks_with_password))
    return False


def _use_passwords(path: str, passwords: list) -> bool:
    """
    Check if a JKS file has been protected by any of ``passwords``.

    :param path: path to check
    :param passwords: passwords to test
    """
    if not os.path.exists(path):
        show_unknown('Path does not exist',
                     details=dict(path=path))
        return False

    opened_jks: list = []
    closed_jks: list = []
    passwords = ['', *(p for p in set(passwords))]

    for full_path in get_paths(path, endswith=('.jks',)):
        success: bool = False
        for password in passwords:
            try:
                jks.KeyStore.load(full_path, password)
            except jks.util.KeystoreSignatureException:
                # wrong password
                continue
            else:
                # correct password
                success = True
                break
        if success:
            opened_jks.append(dict(path=full_path,
                                   password=password,
                                   sha256=get_sha256(full_path)))
        else:
            closed_jks.append(dict(path=full_path,
                                   sha256=get_sha256(full_path)))
    if opened_jks:
        show_open('JKS is/are protected by a password from the list',
                  details=dict(opened_jks=opened_jks,
                               tested_passwords=passwords))
        return True
    show_close('JKS is/are protected by a password from the list',
               details=dict(closed_jks=closed_jks,
                            tested_passwords=passwords))
    return False


@notify
@level('high')
@track
def use_password(path: str, password: str) -> bool:
    """
    Check if a JKS file has been protected by ``password``.

    :param path: path to check
    :param password: password to test
    """
    return _use_passwords(path, [password])


@notify
@level('high')
@track
def use_passwords(path: str, passwords: list) -> bool:
    """
    Check if a JKS file has been protected by any of ``passwords``.

    :param path: path to check
    :param passwords: passwords to test
    """
    return _use_passwords(path, passwords)
