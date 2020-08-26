# -*- coding: utf-8 -*-

"""This module allows to check FTP-specific vulnerabilities."""

# standard imports
import ftplib
from contextlib import suppress

# local imports
from fluidasserts import DAST, OPEN, CLOSED, Unit, HIGH
from fluidasserts.utils.decorators import unknown_if, api

# Constants
PORT: int = 21
NULL_PASSWORD: str = str()
ADMIN_USERNAME: str = 'root'
ANONYMOUS_USERNAME: str = 'anonymous'
ANONYMOUS_PASS: str = 'anonymous'


@unknown_if(OSError)
def _ftp_do_auth(*,
                 ip_address: str, port: int,
                 username: str, password: str,
                 msg_open: str, msg_closed: str) -> tuple:
    """
    Perform FTP auth.

    :param ip_address: IP address to connect to.
    :param username: Username to check.
    :param password: Password to check.
    :param port: If necessary, specify port to connect to.
    """
    could_connect: bool = False

    with ftplib.FTP() as ftp:
        with suppress(ftplib.error_perm):
            ftp.connect(ip_address, port)
            ftp.login(username, password)
            ftp.makepasv()

            could_connect = True

    unit: Unit = Unit(where=f'FTP://{username}:{password}@{ip_address}:{port}',
                      specific=[msg_open if could_connect else msg_closed])

    if could_connect:
        return OPEN, msg_open, [unit], []
    return CLOSED, msg_closed, [], [unit]


@api(risk=HIGH, kind=DAST)
def is_a_valid_user(ip_address: str, username: str,
                    password: str, port: int = PORT) -> tuple:
    """
    Check if given credentials are valid in FTP service.

    :param ip_address: IP address to connect to.
    :param username: Username to check.
    """
    return _ftp_do_auth(
        ip_address=ip_address, port=port,
        username=username, password=password,
        msg_open='Credentials are valid', msg_closed='Credentials are invalid')


@api(risk=HIGH, kind=DAST)
def user_without_password(ip_address: str, username: str,
                          port: int = PORT) -> tuple:
    """
    Check if a user can login without password.

    :param ip_address: IP address to connect to.
    :param username: Username to check.
    """
    return _ftp_do_auth(
        ip_address=ip_address, port=port,
        username=username, password=NULL_PASSWORD,
        msg_open='Password is not required', msg_closed='Password is required')


@api(risk=HIGH, kind=DAST)
def is_anonymous_enabled(ip_address: str, port: int = PORT) -> tuple:
    """
    Check if FTP service allows anonymous login.

    :param ip_address: IP address to connect to.
    """
    return _ftp_do_auth(
        ip_address=ip_address, port=port,
        username=ANONYMOUS_USERNAME, password=ANONYMOUS_PASS,
        msg_open='Anonymous user is enabled',
        msg_closed='Anonymous user is disabled')


@api(risk=HIGH, kind=DAST)
def is_admin_enabled(ip_address: str,
                     password: str,
                     username: str = ADMIN_USERNAME,
                     port: int = PORT) -> tuple:
    """
    Check if FTP service allows admin login.

    :param ip_address: IP address to connect to.
    :param username: Username to check.
    :param password: Password to check.
    """
    return _ftp_do_auth(
        ip_address=ip_address, port=port,
        username=username, password=password,
        msg_open='Admin credentials are valid',
        msg_closed='Admin credentials are invalid')
