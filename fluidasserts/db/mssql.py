# -*- coding: utf-8 -*-
"""``Dynamic Application Security Testing`` Suite of Microsoft SQL Server."""

# standard imports
from contextlib import contextmanager
from typing import Any, Dict, Iterable, List, NamedTuple, Optional, Tuple

# 3rd party imports
import pymssql
from pymssql import Connection, Cursor
# local imports
from fluidasserts import DAST, HIGH, LOW
from fluidasserts.db import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if

ConnectionString = NamedTuple('ConnectionString', [
    ('dbname', str),
    ('user', str),
    ('password', str),
    ('host', str),
    ('port', int),
])


def _is_auth_error(exception: pymssql.Error) -> bool:
    """Return True if the exception is an authentication exception."""
    return 'Login failed' in str(exception)


def _is_xp_cmdshell_error(exception: pymssql.Error) -> bool:
    """Return True if the exception is an xp_cmdshell exception."""
    return exception.args[0] == 15281


def _is_permission_error(exception: pymssql.Error) -> bool:
    """Return True if the exception is an permission exception."""
    return exception.args[0] == 229


def _is_compatibility_error(exception: pymssql.Error) -> bool:
    """Return True if the exception is an pecompatibility exception."""
    return exception.args[0] == 16202


@contextmanager
def _execute(connection_string: ConnectionString, query: str,
             variables: Optional[Dict[str, Any]] = None) -> Cursor:
    """Cursor with state after execute a query."""
    with databse(connection_string) as (_, cursor):
        cursor.execute(query)
        row = cursor.fetchone()
        while row:
            row = cursor.fetchone()
        try:
            if not variables:
                cursor.execute(query)
            else:
                cursor.execute(query, variables)
            yield cursor
        finally:
            pass


@contextmanager
def databse(connection_string: ConnectionString
            ) -> Iterable[Tuple[Connection, Cursor]]:
    """
    Context manager to get a safe connection and a cursor.

    :param connection_string: Connection parameter and credentials.
    :returns: A tuple of (connection object, cursor object).
    """
    connection = pymssql.connect(
        server=connection_string.host,
        port=str(connection_string.port),
        database=connection_string.dbname,
        user=connection_string.user,
        password=connection_string.password)

    try:
        cursor = connection.cursor()
        try:
            yield connection, cursor
        finally:
            cursor.close()
    finally:
        connection.close()


@api(risk=LOW, kind=DAST)
@unknown_if(pymssql.Error)
def have_access(dbname: str, user: str, password: str, host: str,
                port: int) -> Tuple:
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
    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port)
    success: bool = False
    msg_open: str = 'SQL Server is accessible with given credentials'
    msg_closed: str = 'SQL Server is not accessible with given credentials'

    try:
        with databse(connection_string):
            success = True
    except pymssql.Error as exc:
        if not _is_auth_error(exc):
            raise exc

    vulns: List[str] = []
    safes: List[str] = []

    (vulns if success else safes).append(msg_open if success else msg_closed)

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(pymssql.Error)
def can_execute_commands(dbname: str, user: str, password: str, host: str,
                         port: int) -> Tuple:
    """
    Check if the user can execute OS commands.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.
    :returns: - ``OPEN`` if we were able execute OS commands.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port)
    success: bool = False
    msg_open: str = 'The user can execute OS commands'
    msg_closed: str = 'The user can\'t execute OS commands'

    try:
        with databse(connection_string) as database:
            database[1].execute('EXEC xp_cmdshell \'mkdir test, NO_OUTPUT\'')
            success = True
    except pymssql.Error as exc:
        if not _is_compatibility_error and not _is_permission_error(
                exc) and not _is_xp_cmdshell_error(exc):
            raise exc

    vulns: List[str] = []
    safes: List[str] = []

    (vulns if success else safes).append(msg_open if success else msg_closed)

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(pymssql.Error)
def has_text(dbname: str, user: str, password: str, host: str, port: int,
             query: str, expected_text: str) -> Tuple:
    """
    Check if the executed query return the expected text.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.
    :param query: query to execute.
    :param expected_text: expected text of the query.
    :returns: - ``OPEN`` if query result is equal to the ``expected_text``
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port)
    success: bool = False
    msg_open: str = 'The query result matches the expected text'
    msg_closed: str = 'The query result doesn\'t match the expected text'

    vulns: List[str] = []
    safes: List[str] = []
    with _execute(connection_string, query) as cursor:
        data = cursor.fetchall()
        for row in data:
            beaked = False
            for column in row:
                if expected_text == column:
                    success = True
                    beaked = True
                    break
            if beaked:
                break

    (vulns if success else safes).append(msg_open if success else msg_closed)

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
