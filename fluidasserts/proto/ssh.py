# -*- coding: utf-8 -*-

"""This module allows to check SSH vulnerabilities."""

# standard imports
import socket
from contextlib import suppress

# 3rd party imports
import paramiko

# local imports
from fluidasserts import DAST, LOW, MEDIUM, _get_result_as_tuple_host_port
from fluidasserts.helper import banner, ssh
from fluidasserts.utils.decorators import unknown_if, api

PORT: int = 22


@api(risk=MEDIUM, kind=DAST)
@unknown_if(socket.timeout, paramiko.ssh_exception.NoValidConnectionsError)
def is_cbc_used(host: str, port: int = PORT, username: str = None,
                password: str = None) -> tuple:
    """
    Check if SSH has CBC algorithms enabled.

    :param host: Address to test.
    :param port: If necessary, specify port to connect to.
    :param username: Username.
    :param password: Password.
    """
    result: bool = False
    with suppress(paramiko.ssh_exception.AuthenticationException):
        service = banner.SSHService(port)
        fingerprint = service.get_fingerprint(host)
        with ssh.build_ssh_object() as ssh_obj:
            ssh_obj.connect(host, port, username=username, password=password)
            transport = ssh_obj.get_transport()

        if '-cbc' in transport.remote_cipher:
            result = True

    return _get_result_as_tuple_host_port(
        protocol='SSH', host=host, port=port,
        msg_open='Uses insecure CBC encryption algorithms',
        msg_closed='Does not use insecure CBC encryption algorithms',
        open_if=result,
        auth=(username, password),
        fingerprint=fingerprint)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(socket.timeout, paramiko.ssh_exception.NoValidConnectionsError)
def is_hmac_used(host: str, port: int = PORT, username: str = None,
                 password: str = None) -> tuple:
    """
    Check if SSH has weak HMAC algorithms enabled.

    :param host: Address to test.
    :param port: If necessary, specify port to connect to.
    :param username: Username.
    :param password: Password.
    """
    result: bool = False
    with suppress(paramiko.ssh_exception.AuthenticationException):
        service = banner.SSHService(port)
        fingerprint = service.get_fingerprint(host)
        with ssh.build_ssh_object() as ssh_obj:
            ssh_obj.connect(host, port, username=username, password=password)
            transport = ssh_obj.get_transport()

        if "hmac-md5" in transport.remote_cipher:
            result = True

    return _get_result_as_tuple_host_port(
        protocol='SSH', host=host, port=port,
        msg_open='Uses insecure HMAC encryption algorithms',
        msg_closed='Does not use insecure HMAC encryption algorithms',
        open_if=result,
        auth=(username, password),
        fingerprint=fingerprint)


@api(risk=LOW, kind=DAST)
def is_version_visible(ip_address: str, port: int = PORT) -> tuple:
    """
    Check if banner is visible.

    :param ip_address: IP address to test.
    :param port: If necessary, specify port to connect to (default: 22).
    """
    service = banner.SSHService(port)
    version = service.get_version(ip_address)
    fingerprint = service.get_fingerprint(ip_address)

    result: bool = bool(version)

    return _get_result_as_tuple_host_port(
        protocol='SSH', host=ip_address, port=port,
        msg_open='Version is visible',
        msg_closed='Version is not visible',
        open_if=result,
        fingerprint=fingerprint)
