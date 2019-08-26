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
from fluidasserts.utils.decorators import api

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


def _get_var(
        connection_string: ConnectionString,
        variable_name: str) -> str:
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
    """Check if the given connection string allows to connect to the DB."""
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
    """Check if the server supports SSL connections."""
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
def has_not_logging_enabled(dbname: str,
                            user: str, password: str,
                            host: str, port: int) -> tuple:
    """Check if the PostgreSQL implementation logs all transactions."""
    connection_string: ConnectionString = \
        ConnectionString(dbname, user, password, host, port)

    msg_open: str = 'PostgreSQL has not logging enabled'
    msg_closed: str = 'PostgreSQL has logging enabled'

    try:
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

    except psycopg2.OperationalError as exc:
        return UNKNOWN, f'An error occurred: {exc}'

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
