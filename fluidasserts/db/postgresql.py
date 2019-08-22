# -*- coding: utf-8 -*-

"""This module allows to check generic PostgreSQL DB vulnerabilities."""

# standard imports
from typing import List
from contextlib import contextmanager
from collections import namedtuple

# 3rd party imports
import psycopg2

# local imports
from fluidasserts import Unit, LOW, DAST, OPEN, CLOSED, UNKNOWN
from fluidasserts.utils.decorators import api

# Containers
ConnectionString = namedtuple('ConnectionString', [
    'dbname', 'user', 'password', 'host', 'port'
])


def _is_auth_error(exception) -> bool:
    """Return True if the exception is an authentication exception."""
    return 'authentication' in str(exception)


@contextmanager
def database(connection_string: ConnectionString):
    """Context manager to get a safe connection and a cursor."""
    connection = psycopg2.connect(
        dbname=connection_string.dbname,
        user=connection_string.user,
        password=connection_string.password,
        host=connection_string.host,
        port=connection_string.port)

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
