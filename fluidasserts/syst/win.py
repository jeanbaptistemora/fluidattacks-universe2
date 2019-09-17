# -*- coding: utf-8 -*-

"""This module allows to check Windows Server vulnerabilities."""

# standard imports
import re

# local imports
from fluidasserts import DAST, LOW, MEDIUM, HIGH
from fluidasserts.syst import _get_result_as_tuple
from fluidasserts.helper.winrm import winrm_exec_command, ConnError
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ConnError)
def are_compilers_installed(server: str, username: str,
                            password: str) -> tuple:
    """
    Check if there is any compiler installed in Windows Server.

    :param server: URL or IP of host to test.
    :param username: User to connect to WinRM.
    :param password: Password for given user.
    """
    common_compilers = ('Visual', 'Python', 'Mingw', 'CygWin')

    query: str = ('reg query "HKLM\\Software\\Microsoft\\Windows\\'
                  'CurrentVersion\\Uninstall" /s')

    installed_software = winrm_exec_command(server, username, password, query)

    return _get_result_as_tuple(
        system='Windows', host=server,
        msg_open='Server has compilers installed',
        msg_closed='Server does not have compilers installed',
        open_if=any(
            re.search(compiler, installed_software, re.IGNORECASE)
            for compiler in common_compilers))


@api(risk=HIGH, kind=DAST)
@unknown_if(ConnError)
def is_antimalware_not_installed(server: str, username: str,
                                 password: str) -> tuple:
    """
    Check if there is any antimalware installed in Windows Server.

    :param server: URL or IP of host to test.
    :param username: User to connect to WinRM.
    :param password: Password for given user.
    """
    common_av = ('Symantec', 'Norton', 'AVG', 'Kaspersky', 'TrendMicro',
                 'Panda', 'Sophos', 'McAfee', 'Eset')

    query: str = ('reg query "HKLM\\Software\\Microsoft\\Windows\\'
                  'CurrentVersion\\Uninstall" /s')

    installed_software = winrm_exec_command(server, username, password, query)

    return _get_result_as_tuple(
        system='Windows', host=server,
        msg_open='Server has an antivirus installed',
        msg_closed='Server does not have an antivirus installed',
        open_if=any(
            re.search(antivirus, installed_software, re.IGNORECASE)
            for antivirus in common_av))


@api(risk=LOW, kind=DAST)
@unknown_if(ConnError)
def are_syncookies_disabled(server: str) -> tuple:
    """
    Check if SynCookies or similar is enabled in Windows Server.

    :param server: URL or IP of host to test.
    :param username: User to connect to WinRM.
    :param password: Password for given user.
    """
    # On Windows, SYN Cookies are enabled by default and there's no
    # way to disable it.
    return _get_result_as_tuple(
        system='Windows', host=server,
        msg_open='Server has not SYN Cookies enabled',
        msg_closed='Server has SYN Cookies enabled',
        open_if=False)


@api(risk=HIGH, kind=DAST)
@unknown_if(ConnError)
def are_protected_users_disabled(server: str, username: str,
                                 password: str) -> tuple:
    """
    Check if protected users is enabled on system.

    If the result is True, executing mimikatz would give dangerous results.

    :param server: URL or IP of host to test.
    :param username: User to connect to WinRM.
    :param password: Password for given user.
    """
    security_patches = ('KB2871997',)

    msg_closed: str = 'Server has all required patches'

    query: str = ('reg query "HKLM\\SOFTWARE\\Microsoft\\Windows\\'
                  'CurrentVersion\\ComponentBased Servicing\\Packages" /s')

    installed_software = winrm_exec_command(server, username, password, query)

    server_needed_patches = (
        len(security_patches)
        - sum(1
              for patch in security_patches
              if re.search(patch, installed_software, re.IGNORECASE)))

    if server_needed_patches > 0:

        query = ('reg query "HKLM\\System\\CurrentControlSet\\'
                 'Control\\SecurityProviders\\WDigest" /v UseLogonCredential')

        logon_credentials = winrm_exec_command(server,
                                               username,
                                               password,
                                               query)

        safe_use_logon_credentials: bool = bool(re.search(
            r'UseLogonCredential.*0x0', logon_credentials, re.I))

        if safe_use_logon_credentials:
            msg_closed = 'Server has UseLogonCredentials set to 0x0'

    return _get_result_as_tuple(
        system='Windows', host=server,
        msg_open='Server is missing KB2871997 update',
        msg_closed=msg_closed,
        open_if=server_needed_patches > 0 and not safe_use_logon_credentials)
