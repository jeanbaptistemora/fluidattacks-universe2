# -*- coding: utf-8 -*-

"""This module allows to check generic MySQL/MariaDB DB vulnerabilities."""

# standard imports
from typing import Any, Dict, Iterator, List, NamedTuple, Optional, Tuple
from contextlib import contextmanager

# 3rd party imports
import mysql.connector
import mysql.connector.errorcode

# local imports
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts import DAST, LOW, MEDIUM, HIGH
from fluidasserts.db import _get_result_as_tuple
from fluidasserts.utils.decorators import track, level, notify, api, unknown_if


class ConnError(Exception):
    """
    A connection error occurred.

    :py:exc:`mysql.connector.errors.InterfaceError` wrapper exception.
    """


def _get_mysql_cursor(server: str,
                      username: str,
                      password: str,
                      port: int) -> mysql.connector.MySQLConnection:
    """Get MySQL cursor."""
    try:
        mydb = mysql.connector.connect(
            host=server,
            user=username,
            passwd=password,
            port=port
        )
    except (mysql.connector.errors.InterfaceError,
            mysql.connector.errors.ProgrammingError) as exc:
        raise ConnError(exc)
    else:
        return mydb


# Containers
#: Container with connection parameters and credentials
ConnectionString = NamedTuple(
    'ConnectionString', [
        ('user', str),
        ('passwd', str),
        ('host', str),
        ('port', int),
    ])


def _execute(connection_string: ConnectionString,
             query: str,
             variables: Optional[Dict[str, Any]] = None) -> Iterator[Any]:
    """Yield the result of executing a command."""
    variables = variables or {}
    with database(connection_string) as (_, cursor):
        cursor.execute(query, variables)
        yield from cursor


@contextmanager
def database(connection_string: ConnectionString) -> Iterator[Tuple[Any, Any]]:
    """
    Context manager to get a safe connection and a cursor.

    :param connection_string: Connection parameter and credentials.
    :returns: A tuple of (connection object, cursor object).
    """
    connection = mysql.connector.connect(
        user=connection_string.user,
        passwd=connection_string.passwd,
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
@unknown_if(mysql.connector.Error)
def have_access(server: str, username: str, password: str,
                port: int = 3306) -> tuple:
    """Check if there is access to database server."""
    connection_string = ConnectionString(username, password, server, port)

    success: bool = False
    msg_open: str = 'MySQL is accessible with given credentials'
    msg_closed: str = 'MySQL is not accessible with given credentials'

    try:
        with database(connection_string):
            success = True
    except mysql.connector.Error as exc:
        if exc.errno != mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            raise exc

    vulns: List[str] = []
    safes: List[str] = []

    (vulns if success else safes).append(msg_open if success else msg_closed)

    return _get_result_as_tuple(
        host=server,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(mysql.connector.Error)
def test_db_exists(server: str, username: str, password: str,
                   port: int = 3306) -> tuple:
    """Check if "test" database exists."""
    connection_string = ConnectionString(username, password, server, port)

    msg_open: str = 'test Database is present'
    msg_closed: str = 'test Database is not present'

    vulnerable: bool = any(db == 'test'
                           for db, in _execute(connection_string,
                                               'SHOW DATABASES'))

    vulns: List[str] = []
    safes: List[str] = []

    (vulns if vulnerable else safes).append(
        msg_open if vulnerable else msg_closed)

    return _get_result_as_tuple(
        host=server,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(mysql.connector.Error)
def local_infile_enabled(server: str, username: str, password: str,
                         port: int = 3306) -> tuple:
    """Check if 'local_infile' parameter is set to ON."""
    connection_string = ConnectionString(username, password, server, port)

    msg_open: str = 'Parameter "local_infile" is ON on server'
    msg_closed: str = 'Parameter "local_infile" is OFF on server'

    query: str = """
        SHOW VARIABLES
        WHERE Variable_name = 'local_infile'
        """

    vulnerable: bool = any(row == ('local_infile', 'ON')
                           for row in _execute(connection_string, query))

    vulns: List[str] = []
    safes: List[str] = []

    (vulns if vulnerable else safes).append(
        msg_open if vulnerable else msg_closed)

    return _get_result_as_tuple(
        host=server,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(mysql.connector.Error)
def symlinks_enabled(server: str, username: str, password: str,
                     port: int = 3306) -> tuple:
    """Check if symbolic links are enabled on MySQL server."""
    connection_string = ConnectionString(username, password, server, port)

    msg_open: str = 'Symbolic links are supported by server'
    msg_closed: str = 'Symbolic links are not supported by server'

    query: str = """
        SHOW VARIABLES LIKE 'have_symlink'
        """

    vulnerable: bool = not any(row == ('have_symlink', 'DISABLED')
                               for row in _execute(connection_string, query))

    vulns: List[str] = []
    safes: List[str] = []

    (vulns if vulnerable else safes).append(
        msg_open if vulnerable else msg_closed)

    return _get_result_as_tuple(
        host=server,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(mysql.connector.Error)
def memcached_enabled(server: str, username: str, password: str,
                      port: int = 3306) -> tuple:
    """Check if memcached daemon is enabled on server."""
    connection_string = ConnectionString(username, password, server, port)

    msg_open: str = 'Memcached daemon is enabled on server'
    msg_closed: str = 'Memcached daemon is disabled on server'

    query: str = """
        SELECT * FROM information_schema.plugins
        WHERE PLUGIN_NAME = 'daemon_memcached'
        """

    # vulnerable if there are returned rows
    vulnerable: bool = bool(tuple(_execute(connection_string, query)))

    vulns: List[str] = []
    safes: List[str] = []

    (vulns if vulnerable else safes).append(
        msg_open if vulnerable else msg_closed)

    return _get_result_as_tuple(
        host=server,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(mysql.connector.Error)
def secure_file_priv_disabled(server: str, username: str,
                              password: str, port: int = 3306) -> tuple:
    """Check if secure_file_priv is configured on server."""
    connection_string = ConnectionString(username, password, server, port)

    msg_open: str = 'Parameter secure_file_priv is not established'
    msg_closed: str = 'Parameter secure_file_priv is established'

    query: str = """
        SHOW GLOBAL VARIABLES
        WHERE Variable_name = 'secure_file_priv' AND Value <> ''
        """

    # vulnerable if there are no returned rows
    vulnerable: bool = not bool(tuple(_execute(connection_string, query)))

    vulns: List[str] = []
    safes: List[str] = []

    (vulns if vulnerable else safes).append(
        msg_open if vulnerable else msg_closed)

    return _get_result_as_tuple(
        host=server,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(mysql.connector.Error)
def strict_all_tables_disabled(server: str, username: str,
                               password: str, port: int = 3306) -> tuple:
    """Check if STRICT_ALL_TABLES is enabled on MySQL server."""
    connection_string = ConnectionString(username, password, server, port)

    msg_open: str = 'STRICT_ALL_TABLES is not enabled on by server'
    msg_closed: str = 'STRICT_ALL_TABLES is enabled on by server'

    query: str = """
        SHOW VARIABLES LIKE 'sql_mode'
        """

    vulnerable: bool = not any(value == 'STRICT_ALL_TABLES'
                               for _, value in _execute(connection_string,
                                                        query))

    vulns: List[str] = []
    safes: List[str] = []

    (vulns if vulnerable else safes).append(
        msg_open if vulnerable else msg_closed)

    return _get_result_as_tuple(
        host=server,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(mysql.connector.Error)
def log_error_disabled(server: str, username: str, password: str,
                       port: int = 3306) -> tuple:
    """Check if 'log_error' parameter is set on MySQL server."""
    connection_string = ConnectionString(username, password, server, port)

    msg_open: str = 'Parameter log_error not set on server'
    msg_closed: str = 'Parameter log_error is set on server'

    query: str = """
        SHOW VARIABLES LIKE 'log_error'
        """

    vulnerable: bool = any(row == ('log_error', '')
                           for row in _execute(connection_string, query))

    vulns: List[str] = []
    safes: List[str] = []

    (vulns if vulnerable else safes).append(
        msg_open if vulnerable else msg_closed)

    return _get_result_as_tuple(
        host=server,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(mysql.connector.Error)
def logs_on_system_fs(server: str, username: str, password: str,
                      port: int = 3306) -> tuple:
    """Check if logs are stored on a system filesystem on server."""
    connection_string = ConnectionString(username, password, server, port)

    msg_open: str = 'Logs are stored on system filesystems on server'
    msg_closed: str = 'Logs are outside system filesystems on server'

    query: str = 'SELECT @@global.log_bin_basename'

    vulnerable: bool = any(value.startswith('/var') or value.startswith('/usr')
                           for value, in _execute(connection_string, query))

    vulns: List[str] = []
    safes: List[str] = []

    (vulns if vulnerable else safes).append(
        msg_open if vulnerable else msg_closed)

    return _get_result_as_tuple(
        host=server,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(mysql.connector.Error)
def logs_verbosity_low(server: str, username: str, password: str,
                       port: int = 3306) -> tuple:
    """Check if logs verbosity includes errors, warnings and notes."""
    connection_string = ConnectionString(username, password, server, port)

    msg_open: str = 'Logs verbosity is not enough'
    msg_closed: str = 'Logs verbosity is sufficient'

    query: str = """
        SHOW GLOBAL VARIABLES LIKE 'log_error_verbosity'
        """

    is_safe: bool = any(value in ('2', '3')
                        for _, value in _execute(connection_string, query))

    vulns: List[str] = []
    safes: List[str] = []

    (safes if is_safe else vulns).append(
        msg_closed if is_safe else msg_open)

    return _get_result_as_tuple(
        host=server,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(mysql.connector.Error)
def auto_creates_users(server: str, username: str, password: str,
                       port: int = 3306) -> tuple:
    """Check if 'NO_AUTO_CREATE_USER' param is set."""
    connection_string = ConnectionString(username, password, server, port)

    msg_open: str = 'Param "NO_AUTO_CREATE_USER" not set on server'
    msg_closed: str = 'Param "NO_AUTO_CREATE_USER" is set on server'

    query: str = """
        SELECT @@global.sql_mode
        UNION ALL
        SELECT @@session.sql_mode
        """

    is_safe: bool = any('NO_AUTO_CREATE_USER' in var
                        for var, in _execute(connection_string, query))

    vulns: List[str] = []
    safes: List[str] = []

    (safes if is_safe else vulns).append(
        msg_closed if is_safe else msg_open)

    return _get_result_as_tuple(
        host=server,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(mysql.connector.Error)
def has_users_without_password(server: str, username: str,
                               password: str, port: int = 3306) -> tuple:
    """Check if users have a password set."""
    connection_string = ConnectionString(username, password, server, port)

    msg_open: str = 'There are users without password on server'
    msg_closed: str = 'All users have passwords on server'

    query: str = """
        SELECT user FROM mysql.user WHERE password = ''
        """

    vulnerable: bool = bool(tuple(_execute(connection_string, query)))

    vulns: List[str] = []
    safes: List[str] = []

    (vulns if vulnerable else safes).append(
        msg_open if vulnerable else msg_closed)

    return _get_result_as_tuple(
        host=server,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(mysql.connector.Error)
def password_expiration_unsafe(server: str, username: str,
                               password: str, port: int = 3306) -> tuple:
    """Check if password expiration time is safe."""
    connection_string = ConnectionString(username, password, server, port)

    msg_open: str = 'Password lifetime is unsafe'
    msg_closed: str = 'Password lifetime is safe'

    query: str = """
        SHOW VARIABLES LIKE "default_password_lifetime"
        """
    results: Tuple[Any] = tuple(_execute(connection_string, query))
    vulnerable: bool = not results or any(int(val) > 90 for _, val in results)

    vulns: List[str] = []
    safes: List[str] = []

    (vulns if vulnerable else safes).append(
        msg_open if vulnerable else msg_closed)

    return _get_result_as_tuple(
        host=server,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(mysql.connector.Error)
def password_equals_to_user(server: str, username: str,
                            password: str, port: int = 3306) -> bool:
    """Check if users' password is the same username."""
    connection_string = ConnectionString(username, password, server, port)

    msg_open: str = 'There are users whose username is their password'
    msg_closed: str = 'There are no users whose username is their password'

    query: str = """
        SELECT User, password
        FROM mysql.user
        WHERE (
            password = MD5(%(username)s)
            or password = SHA1(%(username)s)
            or password = PASSWORD(%(username)s)
            or password = ENCRYPT(%(username)s)
        )
        """
    variables: Dict[str, str] = {
        'username': username
    }

    # vulnerable if there are returned rows
    vulnerable: bool = bool(tuple(_execute(connection_string,
                                           query, variables)))

    vulns: List[str] = []
    safes: List[str] = []

    (vulns if vulnerable else safes).append(
        msg_open if vulnerable else msg_closed)

    return _get_result_as_tuple(
        host=server,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@notify
@level('high')
@track
def users_have_wildcard_host(server: str, username: str,
                             password: str, port: int = 3306) -> bool:
    """Check if users have a wildcard host grants."""
    try:
        mydb = _get_mysql_cursor(server, username, password, port)
    except ConnError as exc:
        show_unknown('There was an error connecting to MySQL engine',
                     details=dict(server=server, user=username,
                                  error=str(exc)))
        return False
    else:
        mycursor = mydb.cursor()

        query = 'SELECT user FROM mysql.user WHERE host = "%"'
        try:
            mycursor.execute(query)
        except mysql.connector.errors.ProgrammingError as exc:
            show_unknown('There was an error executing query',
                         details=dict(server=server, username=username,
                                      error=str(exc).replace(':', ',')))
            return False

        _result = list(mycursor)
        result = len(_result) != 0

        if result:
            show_open('There are users with wildcard hosts',
                      details=dict(server=server,
                                   users=", ".join([x[0].decode()
                                                    for x in _result])))
        else:
            show_close('There are not users with wildcard hosts',
                       details=dict(server=server))
        return result


@notify
@level('high')
@track
def not_use_ssl(server: str, username: str, password: str,
                port: int = 3306) -> bool:
    """Check if MySQL server uses SSL."""
    try:
        mydb = _get_mysql_cursor(server, username, password, port)
    except ConnError as exc:
        show_unknown('There was an error connecting to MySQL engine',
                     details=dict(server=server, user=username,
                                  error=str(exc)))
        return False
    else:
        mycursor = mydb.cursor()

        query = 'SHOW variables WHERE variable_name = "have_ssl"'
        try:
            mycursor.execute(query)
        except mysql.connector.errors.ProgrammingError as exc:
            show_unknown('There was an error executing query',
                         details=dict(server=server, username=username,
                                      error=str(exc).replace(':', ',')))
            return False

        _result = list(mycursor)
        result = _result[0][1] == 'DISABLED'

        if result:
            show_open('Server don\'t use SSL',
                      details=dict(server=server))
        else:
            show_close('Server uses SSL',
                       details=dict(server=server))
        return result


@notify
@level('high')
@track
def ssl_unforced(server: str, username: str, password: str,
                 port: int = 3306) -> bool:
    """Check if users are forced to use SSL."""
    try:
        mydb = _get_mysql_cursor(server, username, password, port)
    except ConnError as exc:
        show_unknown('There was an error connecting to MySQL engine',
                     details=dict(server=server, user=username,
                                  error=str(exc)))
        return False
    else:
        mycursor = mydb.cursor()

        query = 'SELECT user, ssl_type FROM mysql.user WHERE NOT HOST \
IN ("::1", "127.0.0.1", "localhost") AND \
NOT ssl_type IN ("ANY", "X509", "SPECIFIED")'
        try:
            mycursor.execute(query)
        except mysql.connector.errors.ProgrammingError as exc:
            show_unknown('There was an error executing query',
                         details=dict(server=server, username=username,
                                      error=str(exc).replace(':', ',')))
            return False

        _result = list(mycursor)
        result = len(_result) != 0

        if result:
            show_open('Users are not forced to use SSL',
                      details=dict(server=server,
                                   users=", ".join([x[0].decode()
                                                    for x in _result])))
        else:
            show_close('Users are forced to use SSL',
                       details=dict(server=server))
        return result
