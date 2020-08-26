# -*- coding: utf-8 -*-

"""This module allows to check generic MySQL OS (Linux) vulnerabilities."""

# standard imports
from typing import List, Tuple

# local imports
from fluidasserts import DAST, LOW, MEDIUM, HIGH
from fluidasserts.syst import _get_result_as_tuple
from fluidasserts.helper.ssh import ssh_exec_command, ConnError
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=HIGH, kind=DAST)
@unknown_if(ConnError)
def daemon_high_privileged(server: str, username: str, password: str,
                           ssh_config: str = None) -> tuple:
    """Check if current MySQL installation uses non-privileged user."""
    tests: List[Tuple[str, bytes]] = [
        ('ps -o user= -p $(pgrep mysql)', b'mysql'),
        ('grep -o ^mysql /etc/passwd', b'mysql'),
        ('stat -c %U /var/lib/mysql', b'mysql')
    ]

    privileged: bool = True
    for cmd, privileged_answer in tests:
        out, _ = ssh_exec_command(
            server, username, password, cmd, ssh_config, raise_errors=False)

        if out == privileged_answer:
            privileged = False
            break

    return _get_result_as_tuple(
        system='MySQL-OS', host=server,
        msg_open='MySQL server is running with a privileged account',
        msg_closed='MySQL server is running with a non-privileged account',
        open_if=privileged)


@api(risk=LOW, kind=DAST)
@unknown_if(OSError, ConnError)
def history_enabled(server: str, username: str, password: str,
                    ssh_config: str = None) -> tuple:
    """Check for .mysql_history files."""
    cmd: str = ('c=0;'
                'for i in $(find /home -name .mysql_history); do'
                '  size=$(stat -c %b $i);'
                '  c=$(($c+$size));'
                'done;'
                'echo $c')

    out, _ = ssh_exec_command(server, username, password, cmd, ssh_config)

    are_history_files_empty: bool = out in (b'0', b'')

    return _get_result_as_tuple(
        system='MySQL-OS', host=server,
        msg_open='MySQL history files are not empty',
        msg_closed='MySQL history files are empty',
        open_if=not are_history_files_empty)


@api(risk=HIGH, kind=DAST)
@unknown_if(OSError, ConnError)
def pwd_on_env(server: str, username: str, password: str,
               ssh_config: str = None) -> tuple:
    """Check for MYSQL_PWD env var."""
    cmd: str = ('grep -h MYSQL_PWD /proc/*/environ;'
                'grep -h MYSQL_PWD /home/*/.bashrc;'
                'grep -h MYSQL_PWD /home/*/.profile;'
                'grep -h MYSQL_PWD /home/*/.bash_profile;')

    out, _ = ssh_exec_command(
        server, username, password, cmd, ssh_config, raise_errors=False)

    is_mysql_pwd_var_set: bool = bool(out)

    return _get_result_as_tuple(
        system='MySQL-OS', host=server,
        msg_open='MYSQL_PWD found on environment',
        msg_closed='MYSQL_PWD not on environment',
        open_if=is_mysql_pwd_var_set)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(OSError, ConnError)
def has_insecure_shell(server: str, username: str, password: str,
                       ssh_config: str = None) -> tuple:
    """Check for mysql user with interactive shell."""
    cmd: str = 'getent passwd mysql | cut -d: -f7 | grep -e nologin -e false'

    out, _ = ssh_exec_command(server, username, password, cmd, ssh_config)

    interactive_shell: bool = bool(out)

    return _get_result_as_tuple(
        system='MySQL-OS', host=server,
        msg_open='MySQL user uses an interactive shell',
        msg_closed='MySQL user uses a non-interactive shell',
        open_if=not interactive_shell)
