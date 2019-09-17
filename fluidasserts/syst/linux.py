# -*- coding: utf-8 -*-

"""This module allows to check generic Linux vulnerabilities."""

# local imports
from fluidasserts import DAST, LOW, MEDIUM, HIGH
from fluidasserts.syst import _get_result_as_tuple
from fluidasserts.helper.ssh import ssh_exec_command, ConnError
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=MEDIUM, kind=DAST)
@unknown_if(OSError, ConnError)
def is_min_priv_disabled(server: str, username: str, password: str,
                         ssh_config: str = None) -> tuple:
    """
    Check if ``umask`` or similar is secure in ``os_linux``.

    :param server: URL or IP of host to test.
    :param username: User to connect to server.
    :param password: Password for given user.
    :param ssh_config: Path to SSH connection config file.
    """
    out, _ = ssh_exec_command(
        server, username, password, 'umask', ssh_config)

    return _get_result_as_tuple(
        system='Unix', host=server,
        msg_open='Server has insecure default privileges',
        msg_closed='Server has secure default privileges',
        open_if=out != b'0027')


@api(risk=MEDIUM, kind=DAST)
@unknown_if(OSError, ConnError)
def is_sudo_disabled(server: str, username: str, password: str,
                     ssh_config: str = None) -> tuple:
    """
    Check if there's ``sudo`` or similar installed in ``os_linux``.

    :param server: URL or IP of host to test.
    :param username: User to connect to server.
    :param password: Password for given user.
    :param ssh_config: Path to SSH connection config file.
    """
    cmd: str = 'which sudo'
    out, _ = ssh_exec_command(
        server, username, password, cmd, ssh_config, raise_errors=True)

    is_sudo_installed: bool = bool(out)

    return _get_result_as_tuple(
        system='Unix', host=server,
        msg_open='Server has not "sudo" or similar installed',
        msg_closed='Server has "sudo" or similar installed',
        open_if=not is_sudo_installed)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(OSError, ConnError)
def are_compilers_installed(server: str, username: str, password: str,
                            ssh_config: str = None) -> tuple:
    """
    Check if there is any compiler installed in ``os_linux``.

    :param server: URL or IP of host to test.
    :param username: User to connect to server.
    :param password: Password for given user.
    :param ssh_config: Path to SSH connection config file.
    """
    cmd: str = 'which cc gcc c++ g++ javac ld as nasm'
    out, _ = ssh_exec_command(
        server, username, password, cmd, ssh_config, raise_errors=True)

    have_compilers: bool = bool(out)

    return _get_result_as_tuple(
        system='Unix', host=server,
        msg_open='Server has compilers installed',
        msg_closed='Server has not compilers installed',
        open_if=have_compilers)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(OSError, ConnError)
def is_antimalware_not_installed(server: str, username: str, password: str,
                                 ssh_config: str = None) -> tuple:
    """
    Check if there is any antimalware installed in ``os_linux``.

    :param server: URL or IP of host to test.
    :param username: User to connect to server.
    :param password: Password for given user.
    :param ssh_config: Path to SSH connection config file.
    """
    cmd: str = 'which clamscan avgscan'
    out, _ = ssh_exec_command(
        server, username, password, cmd, ssh_config, raise_errors=True)

    is_antivirus_installed: bool = bool(out)

    return _get_result_as_tuple(
        system='Unix', host=server,
        msg_open='Server has not an antivirus installed',
        msg_closed='Server has an antivirus installed',
        open_if=not is_antivirus_installed)


@api(risk=HIGH, kind=DAST)
@unknown_if(OSError, ConnError)
def is_remote_admin_enabled(server: str, username: str, password: str,
                            ssh_config: str = None) -> tuple:
    """
    Check if admins can remotely log into ``os_linux``.

    :param server: URL or IP of host to test.
    :param username: User to connect to server.
    :param password: Password for given user.
    :param ssh_config: Path to SSH connection config file.
    """
    cmd: str = 'grep -i "^PermitRootLogin.*yes" /etc/ssh/sshd_config'
    out, _ = ssh_exec_command(
        server, username, password, cmd, ssh_config, raise_errors=True)

    is_remote_admin_enabled_enabled: bool = bool(out)

    return _get_result_as_tuple(
        system='Unix', host=server,
        msg_open='Server has remote admin login enabled',
        msg_closed='Server has not remote admin login enabled',
        open_if=is_remote_admin_enabled_enabled)


@api(risk=LOW, kind=DAST)
@unknown_if(OSError, ConnError)
def are_syncookies_disabled(server: str, username: str, password: str,
                            ssh_config: str = None) -> tuple:
    """
    Check if ``SynCookies`` or similar is enabled in ``os_linux``.

    :param server: URL or IP of host to test.
    :param username: User to connect to server.
    :param password: Password for given user.
    :param ssh_config: Path to SSH connection config file.
    """
    cmd: str = 'sysctl -q -n net.ipv4.tcp_syncookies'
    out, _ = ssh_exec_command(
        server, username, password, cmd, ssh_config, raise_errors=True)

    are_syn_cookies_enabled: bool = bool(out)

    return _get_result_as_tuple(
        system='Unix', host=server,
        msg_open='Server has not SynCookies enabled',
        msg_closed='Server has SynCookies enabled',
        open_if=not are_syn_cookies_enabled)
