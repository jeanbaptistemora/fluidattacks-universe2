# -*- coding: utf-8 -*-

"""This module allows to check SMB vulnerabilites."""

# standard imports
from __future__ import absolute_import
from typing import Optional

# 3rd party imports
from smb import SMBConnection
from smb import smb_structs

# local imports
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.utils.decorators import track, level, notify


CLIENT_MACHINE_NAME = 'assertspc'


@notify
@level('medium')
@track
def has_dirlisting(server: str, share: str,
                   user: Optional[str] = None,
                   password: Optional[str] = None,
                   domain: str = 'WORKGROUP') -> bool:
    r"""
    Check if an SMB share has dirlisting.

    :param share: The name of the shared folder.
    :param \*args: Optional arguments for SMB connect.
    :param \*\*kwargs: Optional arguments for SMB connection.
    """
    try:
        with SMBConnection.SMBConnection(user, password,
                                         CLIENT_MACHINE_NAME, server,
                                         domain=domain, use_ntlm_v2=True,
                                         is_direct_tcp=True) as conn:

            ret = conn.connect(server, port=445)
            if not ret:
                show_unknown('There was an error connecting to SMB',
                             details=dict(server=server, domain=domain))
                return False
            conn.listPath(share, '/')
            show_open('Directory listing is possible',
                      details=dict(domain=domain,
                                   user=user,
                                   server=server,
                                   share=share))
            return True
    except OSError as exc:
        show_unknown('There was an error connecting to SMB',
                     details=dict(server=server, domain=domain,
                                  error=str(exc)))
        return False
    except smb_structs.OperationFailure:
        show_close('Directory listing not possible',
                   details=dict(domain=domain,
                                user=user,
                                server=server,
                                share=share))
        return False


@notify
@level('high')
@track
def is_anonymous_enabled(server: str,
                         domain: str = 'WORKGROUP') -> bool:
    """
    Check if anonymous login is possible over SMB.

    :param server: The NetBIOS machine name of the remote server.
    :param domain: The network domain/workgroup. Defaults to 'WORKGROUP'
    """
    user = 'anonymous'
    password = ''
    try:
        with SMBConnection.SMBConnection(user, password,
                                         CLIENT_MACHINE_NAME, server,
                                         domain=domain, use_ntlm_v2=True,
                                         is_direct_tcp=True) as conn:
            ret = conn.connect(server, port=445)
            if not ret:
                show_close('Anonymous login not possible',
                           details=dict(domain=domain, user=user,
                                        server=server))
                return False
            show_open('Anonymous login enabled',
                      details=dict(domain=domain, user=user, server=server))
            return True
    except OSError as exc:
        show_unknown('There was an error connecting to SMB',
                     details=dict(server=server, domain=domain,
                                  error=str(exc)))
        return False


@notify
@level('low')
@track
def is_signing_disabled(server, user, password, domain='WORKGROUP'):
    """
    Check if SMB connection uses signing.

    :param server: The NetBIOS machine name of the remote server.
    :param user: Username to authenticate SMB connection.
    :param password: Password for given user.
    :param domain: The network domain/workgroup. Defaults to 'WORKGROUP'
    """
    try:
        with SMBConnection.SMBConnection(user, password,
                                         CLIENT_MACHINE_NAME, server,
                                         domain=domain, use_ntlm_v2=True,
                                         is_direct_tcp=True) as conn:
            ret = conn.connect(server, port=445)
            if not ret:
                show_unknown('There was an error connecting to SMB',
                             details=dict(server=server, domain=domain))
                return False
            if conn.is_signing_active:
                show_close('SMB has signing active',
                           details=dict(domain=domain, server=server,
                                        user=user))
                return False
            show_open('SMB has signing disabled',
                      details=dict(domain=domain, server=server, user=user))
            return True
    except OSError as exc:
        show_unknown('There was an error connecting to SMB',
                     details=dict(server=server, domain=domain,
                                  error=str(exc)))
        return False
