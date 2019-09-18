# -*- coding: utf-8 -*-

"""This module allows to check SMB vulnerabilities."""

# standard imports
from typing import Optional
from contextlib import suppress

# 3rd party imports
from smb import SMBConnection
from smb import smb_structs

# local imports
from fluidasserts import DAST, MEDIUM, HIGH, _get_result_as_tuple_host_port
from fluidasserts.utils.decorators import unknown_if, api

# Constants
CLIENT_MACHINE_NAME = 'assertspc'


@api(risk=MEDIUM, kind=DAST)
@unknown_if(AssertionError, OSError)
def has_dirlisting(server: str, share: str,
                   user: Optional[str] = None,
                   password: Optional[str] = None,
                   domain: str = 'WORKGROUP') -> tuple:
    r"""
    Check if an SMB share has dirlisting.

    :param share: The name of the shared folder.
    :param \*args: Optional arguments for SMB connect.
    :param \*\*kwargs: Optional arguments for SMB connection.
    """
    success: bool = False
    with suppress(smb_structs.OperationFailure):
        with SMBConnection.SMBConnection(user, password,
                                         CLIENT_MACHINE_NAME, server,
                                         domain=domain,
                                         use_ntlm_v2=True,
                                         is_direct_tcp=True) as conn:
            if not conn.connect(server, port=445):
                raise AssertionError('There was an error connecting to SMB')

            # Attempt to list directories
            conn.listPath(share, '/')
            success = True

    return _get_result_as_tuple_host_port(
        protocol='SMB', host=server, port=445, extra=share,
        msg_open='Directory listing is possible',
        msg_closed='Directory listing is not possible',
        open_if=success,
        auth=(user, password))


@api(risk=HIGH, kind=DAST)
@unknown_if(OSError)
def is_anonymous_enabled(server: str,
                         domain: str = 'WORKGROUP') -> tuple:
    """
    Check if anonymous login is possible over SMB.

    :param server: The NetBIOS machine name of the remote server.
    :param domain: The network domain/workgroup. Defaults to 'WORKGROUP'
    """
    success: bool
    username: str = 'anonymous'
    password: str = str()

    with SMBConnection.SMBConnection(username, password,
                                     CLIENT_MACHINE_NAME, server,
                                     domain=domain,
                                     use_ntlm_v2=True,
                                     is_direct_tcp=True) as conn:
        success = bool(conn.connect(server, port=445))

    return _get_result_as_tuple_host_port(
        protocol='SMB', host=server, port=445,
        msg_open='Anonymous login is possible',
        msg_closed='Anonymous login is not possible',
        open_if=success,
        auth=(username, password))


@api(risk=MEDIUM, kind=DAST)
@unknown_if(AssertionError, OSError)
def is_signing_disabled(server, user, password, domain='WORKGROUP'):
    """
    Check if SMB connection uses signing.

    :param server: The NetBIOS machine name of the remote server.
    :param user: Username to authenticate SMB connection.
    :param password: Password for given user.
    :param domain: The network domain/workgroup. Defaults to 'WORKGROUP'
    """
    signs: bool
    with SMBConnection.SMBConnection(user, password,
                                     CLIENT_MACHINE_NAME, server,
                                     domain=domain,
                                     use_ntlm_v2=True,
                                     is_direct_tcp=True) as conn:
        if not conn.connect(server, port=445):
            raise AssertionError('There was an error connecting to SMB')

        signs = conn.is_signing_active

    return _get_result_as_tuple_host_port(
        protocol='SMB', host=server, port=445,
        msg_open='Signing is not active',
        msg_closed='Signing is active',
        open_if=not signs,
        auth=(user, password))
