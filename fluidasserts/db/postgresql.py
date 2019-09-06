# -*- coding: utf-8 -*-

"""This module allows to check generic PostgreSQL DB vulnerabilities."""

# standard imports
from typing import Any, Dict, Iterator, List, NamedTuple, Optional, Tuple
from contextlib import contextmanager

# 3rd party imports
import psycopg2

# local imports
from fluidasserts import Unit, LOW, MEDIUM, HIGH, DAST, OPEN, CLOSED, UNKNOWN
from fluidasserts.utils.decorators import api, unknown_if

# Containers
#: Container with connection parameters and credentials
ConnectionString = NamedTuple(
    'ConnectionString', [
        ('dbname', str),
        ('user', str),
        ('password', str),
        ('host', str),
        ('port', int),
        ('sslmode', str),
    ])


def _is_auth_error(exception: psycopg2.Error) -> bool:
    """Return True if the exception is an authentication exception."""
    return 'authentication' in str(exception)


def _is_ssl_error(exception: psycopg2.Error) -> bool:
    """Return True if the exception is an SSL exception."""
    return 'SSL' in str(exception)


def _get_var(connection_string: ConnectionString, variable_name: str) -> str:
    """Return the result of `SHOW variable_name;` or an empty string."""
    var_value: str = ''
    with database(connection_string) as (_, cursor):
        try:
            cursor.execute(f'SHOW {variable_name}')
        except psycopg2.errors.UndefinedObject:
            # var is not defined
            pass
        else:
            # var is defined
            row = cursor.fetchone()
            if len(row) == 1:
                # var has a value
                var_value, = row
    return var_value


def _execute(connection_string: ConnectionString,
             query: str,
             variables: Optional[Dict[str, Any]]) -> Iterator[Any]:
    """Yield the result of executing a command."""
    with database(connection_string) as (_, cursor):
        cursor.execute(query, variables)
        yield from cursor


@contextmanager
def database(connection_string: ConnectionString) -> Iterator[Tuple[Any, Any]]:
    """
    Context manager to get a safe connection and a cursor.

    :param connection_string: Connection parameter and credentials.
    """
    connection = psycopg2.connect(
        dbname=connection_string.dbname,
        user=connection_string.user,
        password=connection_string.password,
        host=connection_string.host,
        port=connection_string.port,
        sslmode=connection_string.sslmode)

    try:
        cursor = connection.cursor()
        try:
            yield connection, cursor
        finally:
            cursor.close()
    finally:
        connection.close()


@api(risk=LOW, kind=DAST)
def have_access(dbname: str,
                user: str, password: str,
                host: str, port: int) -> tuple:
    """
    Check if the given connection parameters allow to connect to the database.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.
    :returns: - ``OPEN`` if we were able to connect to the database.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    connection_string: ConnectionString = \
        ConnectionString(dbname, user, password, host, port, 'prefer')

    success: bool = False
    msg_open: str = 'PostgreSQL is accessible with given credentials'
    msg_closed: str = 'PostgreSQL is not accessible with given credentials'

    try:
        with database(connection_string):
            success = True
    except psycopg2.OperationalError as exc:
        if not _is_auth_error(exc):
            return UNKNOWN, f'An error occurred: {exc}'

    assertion: str = 'can' if success else 'can not'

    units: List[Unit] = [
        Unit(where=f'{host}:{port}',
             source='PostgreSQL/Configuration',
             specific=[f'{dbname} database {assertion} be accessed'],
             fingerprint=None)]

    if success:
        return OPEN, msg_open, units, []
    return CLOSED, msg_closed, [], units


@api(risk=MEDIUM, kind=DAST)
def does_not_support_ssl(dbname: str,
                         user: str, password: str,
                         host: str, port: int) -> tuple:
    """
    Check if the server supports SSL connections.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.
    :returns: - ``OPEN`` if server does not allow SSL connections.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    connection_string: ConnectionString = \
        ConnectionString(dbname, user, password, host, port, 'require')

    supports_ssl: bool = False
    msg_open: str = 'PostgreSQL does not support SSL connections'
    msg_closed: str = 'PostgreSQL supports SSL connections'

    try:
        with database(connection_string):
            supports_ssl = True
    except psycopg2.OperationalError as exc:
        if not _is_ssl_error(exc):
            return UNKNOWN, f'An error occurred: {exc}'

    assertion: str = 'supports' if supports_ssl else 'does not support'

    units: List[Unit] = [
        Unit(where=f'{host}:{port}',
             source='PostgreSQL/Configuration',
             specific=[f'PostgreSQL {assertion} SSL connections'],
             fingerprint=None)]

    if supports_ssl:
        return CLOSED, msg_closed, [], units
    return OPEN, msg_open, units, []


@api(risk=MEDIUM, kind=DAST)
@unknown_if(psycopg2.OperationalError)
def has_not_logging_enabled(dbname: str,
                            user: str, password: str,
                            host: str, port: int) -> tuple:
    """
    Check if the PostgreSQL implementation logs all transactions.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.
    :returns: - ``OPEN`` if system variables **logging_collector**,
                **log_statement**, **log_directory**, and **log_filename** are
                not configured to log all database transactions.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    connection_string: ConnectionString = \
        ConnectionString(dbname, user, password, host, port, 'prefer')

    msg_open: str = 'PostgreSQL has not logging enabled'
    msg_closed: str = 'PostgreSQL has logging enabled'

    # logging_collector must be 'on'
    safe_logging_collector: bool = \
        _get_var(connection_string, 'logging_collector') == 'on'

    # log_statement must be 'all'
    safe_log_statement: bool = \
        _get_var(connection_string, 'log_statement') == 'all'

    # log_directory must be set
    safe_log_directory: bool = \
        bool(_get_var(connection_string, 'log_directory'))

    # log_filename must be set
    safe_log_filename: bool = \
        bool(_get_var(connection_string, 'log_filename'))

    vulns: List[Unit] = []
    safes: List[Unit] = []
    vuln_specifics: List[str] = []
    safe_specifics: List[str] = []

    (safe_specifics if safe_logging_collector else vuln_specifics).append(
        'logging_collector must be set to on')
    (safe_specifics if safe_log_statement else vuln_specifics).append(
        'log_statement must be set to all')
    (safe_specifics if safe_log_directory else vuln_specifics).append(
        'log_directory must be set')
    (safe_specifics if safe_log_filename else vuln_specifics).append(
        'log_filename must be set')

    if vuln_specifics:
        vulns.append(Unit(
            where=f'{host}:{port}',
            source='PostgreSQL/Configuration',
            specific=vuln_specifics,
            fingerprint=None))
    if safe_specifics:
        safes.append(Unit(
            where=f'{host}:{port}',
            source='PostgreSQL/Configuration',
            specific=safe_specifics,
            fingerprint=None))

    if vulns:
        return OPEN, msg_open, vulns, safes
    return CLOSED, msg_closed, vulns, safes


@api(risk=MEDIUM, kind=DAST)
@unknown_if(psycopg2.OperationalError)
def has_not_data_checksums_enabled(dbname: str,
                                   user: str, password: str,
                                   host: str, port: int) -> tuple:
    """
    Check if the PostgreSQL implementation not data checksums enabled.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.
    :returns: - ``OPEN`` if system variables **data_checksums**, and
                **ignore_checksum_failure** are not configured to guarantee
                data integrity.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    connection_string: ConnectionString = \
        ConnectionString(dbname, user, password, host, port, 'prefer')

    msg_open: str = 'PostgreSQL has data checksums disabled'
    msg_closed: str = 'PostgreSQL has data checksums enabled'

    # data_checksums must be 'on'
    safe_data_checksums: bool = \
        _get_var(connection_string, 'data_checksums') == 'on'

    # ignore_checksum_failure must be 'off'
    safe_ignore_checksum_fail: bool = \
        _get_var(connection_string, 'ignore_checksum_failure') == 'off'

    vulns: List[Unit] = []
    safes: List[Unit] = []
    vuln_specifics: List[str] = []
    safe_specifics: List[str] = []

    (safe_specifics if safe_data_checksums else vuln_specifics).append(
        'data_checksums must be set to on')

    (safe_specifics if safe_ignore_checksum_fail else vuln_specifics).append(
        'ignore_checksum_failure must be set to off')

    if vuln_specifics:
        vulns.append(Unit(
            where=f'{host}:{port}',
            source='PostgreSQL/Configuration',
            specific=vuln_specifics,
            fingerprint=None))
    if safe_specifics:
        safes.append(Unit(
            where=f'{host}:{port}',
            source='PostgreSQL/Configuration',
            specific=safe_specifics,
            fingerprint=None))

    if vulns:
        return OPEN, msg_open, vulns, safes
    return CLOSED, msg_closed, vulns, safes


@api(risk=MEDIUM, kind=DAST)
@unknown_if(psycopg2.OperationalError)
def has_insecure_password_encryption(dbname: str,
                                     user: str, password: str,
                                     host: str, port: int) -> tuple:
    """
    Check if PostgreSQL implementation store passwords using weak algorithms.

    Commands like **CREATE USER** or **ALTER USER** use the algorithm specified
    in the system variable **password_encryption** to store the hashed
    username and password in the **pg_shadow** table.

    Setting **password_encryption** to
    `scram-sha-256 <https://en.wikipedia.org/wiki/
    Salted_Challenge_Response_Authentication_Mechanism>`_. is suggested.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.
    :returns: - ``OPEN`` if **password_encryption** is not set
                to a **strong** algorithm.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    connection_string: ConnectionString = \
        ConnectionString(dbname, user, password, host, port, 'prefer')

    msg_open: str = 'PostgreSQL has insecure password_encryption'
    msg_closed: str = 'PostgreSQL has secure password_encryption'

    # password_encryption must not be 'off'
    vuln_encryption_1: bool = \
        _get_var(connection_string, 'password_encryption') == 'off'

    # password_encryption must not be 'on' (alias for md5)
    vuln_encryption_2: bool = \
        _get_var(connection_string, 'password_encryption') == 'on'

    # password_encryption must not be 'md5'
    vuln_encryption_3: bool = \
        _get_var(connection_string, 'password_encryption') == 'md5'

    secure_digests: tuple = ('scram-sha-256',)

    # password_encryption must be any of `secure_digests`
    safe_encryption: bool = \
        _get_var(connection_string, 'password_encryption') in secure_digests

    vulns: List[Unit] = []
    safes: List[Unit] = []
    vuln_specifics: List[str] = []
    safe_specifics: List[str] = []

    (vuln_specifics if vuln_encryption_1 else safe_specifics).append(
        'password_encryption must not be set to off')

    (vuln_specifics if vuln_encryption_2 else safe_specifics).append(
        'password_encryption must not be set to on (alias for md5)')

    (vuln_specifics if vuln_encryption_3 else safe_specifics).append(
        'password_encryption must not be set to md5')

    (safe_specifics if safe_encryption else vuln_specifics).append(
        'password_encryption must be set to scram-sha-256')

    if vuln_specifics:
        vulns.append(Unit(
            where=f'{host}:{port}',
            source='PostgreSQL/Configuration',
            specific=vuln_specifics,
            fingerprint=None))
    if safe_specifics:
        safes.append(Unit(
            where=f'{host}:{port}',
            source='PostgreSQL/Configuration',
            specific=safe_specifics,
            fingerprint=None))

    if vulns:
        return OPEN, msg_open, vulns, safes
    return CLOSED, msg_closed, vulns, safes


@api(risk=HIGH, kind=DAST)
@unknown_if(psycopg2.OperationalError)
def has_insecurely_stored_passwords(dbname: str,
                                    user: str, password: str,
                                    host: str, port: int) -> tuple:
    """
    Check if database has passwords stored with a weak algorithm.

    PostgreSQL stores the database users and passwords hashed in the
    **pg_shadow** table. This method will check if any of them is hashed
    with a weak algorithm, or even in plain text.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.
    :returns: - ``OPEN`` if some shadow record in the **pg_shadow** table
                is not using a **strong** digest algorithm.
              - ``UNKNOWN`` on errors,
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    connection_string: ConnectionString = \
        ConnectionString(dbname, user, password, host, port, 'prefer')

    msg_open: str = 'PostgreSQL has insecurely stored passwords'
    msg_closed: str = 'PostgreSQL has safely stored passwords'

    vulns: List[Unit] = []
    safes: List[Unit] = []
    vuln_specifics: List[str] = []
    safe_specifics: List[str] = []

    query: str = 'SELECT usename, passwd FROM pg_shadow'

    safe_digests = ('scram-sha-256',)

    for usename, passwd in _execute(connection_string, query, {}):
        is_safe: bool = any(passwd.lower().startswith(s) for s in safe_digests)
        assertion: str = 'securely' if is_safe else 'insecurely'
        specific: str = f'{usename} user password is {assertion} stored'
        (safe_specifics if is_safe else vuln_specifics).append(specific)

    if vuln_specifics:
        vulns.append(Unit(
            where=f'{host}:{port}',
            source='PostgreSQL/Configuration',
            specific=vuln_specifics,
            fingerprint=None))
    if safe_specifics:
        safes.append(Unit(
            where=f'{host}:{port}',
            source='PostgreSQL/Configuration',
            specific=safe_specifics,
            fingerprint=None))

    if vulns:
        return OPEN, msg_open, vulns, safes
    return CLOSED, msg_closed, vulns, safes
