# -*- coding: utf-8 -*-

"""This module allows to check generic PostgreSQL DB vulnerabilities."""

# standard imports
from typing import List
from contextlib import contextmanager
from collections import namedtuple

# 3rd party imports
import psycopg2

# local imports
from fluidasserts import Unit, LOW, MEDIUM, DAST, OPEN, CLOSED, UNKNOWN
from fluidasserts.utils.decorators import api, unknown_if

# Containers
ConnectionString = namedtuple(
    typename='ConnectionString',
    field_names=[
        'dbname', 'user', 'password', 'host', 'port', 'sslmode'
    ],
    defaults=[
        'prefer',
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


@contextmanager
def database(connection_string: ConnectionString):
    """Context manager to get a safe connection and a cursor."""
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
    Check if the given connection string allows to connect to the DB.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.
    :rtype: :class:`fluidasserts.Result`
    """
    connection_string: ConnectionString = \
        ConnectionString(dbname, user, password, host, port)

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
    :rtype: :class:`fluidasserts.Result`
    """
    connection_string: ConnectionString = \
        ConnectionString(dbname, user, password, host, port, sslmode='require')

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
    :rtype: :class:`fluidasserts.Result`
    """
    connection_string: ConnectionString = \
        ConnectionString(dbname, user, password, host, port)

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
    :returns: OPEN if `initdb` started without the --data-checksums flag,
              UNKNOWN on errors, CLOSED otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    connection_string: ConnectionString = \
        ConnectionString(dbname, user, password, host, port)

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
def store_passwords_insecurely(dbname: str,
                               user: str, password: str,
                               host: str, port: int) -> tuple:
    """
    Check if PostgreSQL implementation store passwords with a risky algorithm.

    Use of SCRAM-SHA-256 is suggested.

    See `SCRAM <https://en.wikipedia.org/wiki/
    Salted_Challenge_Response_Authentication_Mechanism>`_.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.
    :returns: OPEN if a *risky* algorithm is used to store passwords in the
              database, UNKNOWN on errors, CLOSED otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    connection_string: ConnectionString = \
        ConnectionString(dbname, user, password, host, port)

    msg_open: str = 'PostgreSQL stores passwords insecurely'
    msg_closed: str = 'PostgreSQL stores passwords securely'

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
