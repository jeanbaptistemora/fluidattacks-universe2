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
from fluidasserts import DAST, LOW, MEDIUM
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
                           for db, in _execute(
                               connection_string, 'SHOW DATABASES', {}))

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
                         port: int = 3306) -> bool:
    """Check if 'local_infile' parameter is set to ON."""
    connection_string = ConnectionString(username, password, server, port)

    msg_open: str = 'Parameter "local_infile" is ON on server'
    msg_closed: str = 'Parameter "local_infile" is OFF on server'

    query: str = 'SHOW VARIABLES WHERE Variable_name = %(Variable_name)s'
    parameters: Dict[str, str] = {'Variable_name': 'local_infile'}

    vulnerable: bool = any(var_name == 'local_infile' and var_value == 'ON'
                           for var_name, var_value in _execute(
                               connection_string, query, parameters))

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
@level('low')
@track
def symlinks_enabled(server: str, username: str, password: str,
                     port: str = 3306) -> bool:
    """Check if symbolic links are enabled on MySQL server."""
    try:
        mydb = _get_mysql_cursor(server, username, password, port)
    except ConnError as exc:
        show_unknown('There was an error connecting to MySQL engine',
                     details=dict(server=server, user=username,
                                  error=str(exc)))
        return False
    else:
        mycursor = mydb.cursor()

        query = "SHOW variables LIKE 'have_symlink'"
        try:
            mycursor.execute(query)
        except mysql.connector.errors.ProgrammingError as exc:
            show_unknown('There was an error executing query',
                         details=dict(server=server, username=username,
                                      error=str(exc).replace(':', ',')))
            return False

        result = ('have_symlink', 'DISABLED') not in list(mycursor)

        if result:
            show_open('Symbolic links are supported by server',
                      details=dict(server=server))
        else:
            show_close('Symbolic links are not supported by server',
                       details=dict(server=server))
        return result


@notify
@level('low')
@track
def memcached_enabled(server: str, username: str, password: str,
                      port: str = 3306) -> bool:
    """Check if memcached daemon is enabled on server."""
    try:
        mydb = _get_mysql_cursor(server, username, password, port)
    except ConnError as exc:
        show_unknown('There was an error connecting to MySQL engine',
                     details=dict(server=server, user=username,
                                  error=str(exc)))
        return False
    else:
        mycursor = mydb.cursor()

        query = "SELECT * FROM information_schema.plugins WHERE \
PLUGIN_NAME='daemon_memcached'"
        try:
            mycursor.execute(query)
        except mysql.connector.errors.ProgrammingError as exc:
            show_unknown('There was an error executing query',
                         details=dict(server=server, username=username,
                                      error=str(exc).replace(':', ',')))
            return False

        result = len(list(mycursor)) != 0

        if result:
            show_open('Memcached daemon enabled on server',
                      details=dict(server=server))
        else:
            show_close('Memcached daemon not enabled on server',
                       details=dict(server=server))
        return result


@notify
@level('medium')
@track
def secure_file_priv_disabled(server: str, username: str,
                              password: str, port: int = 3306) -> bool:
    """Check if secure_file_priv is configured on server."""
    try:
        mydb = _get_mysql_cursor(server, username, password, port)
    except ConnError as exc:
        show_unknown('There was an error connecting to MySQL engine',
                     details=dict(server=server, user=username,
                                  error=str(exc)))
        return False
    else:
        mycursor = mydb.cursor()

        query = "SHOW GLOBAL VARIABLES WHERE \
Variable_name = 'secure_file_priv' AND Value<>''"
        try:
            mycursor.execute(query)
        except mysql.connector.errors.ProgrammingError as exc:
            show_unknown('There was an error executing query',
                         details=dict(server=server, username=username,
                                      error=str(exc).replace(':', ',')))
            return False

        result = len(list(mycursor)) == 0

        if result:
            show_open('Parameter "secure_file_priv" not established',
                      details=dict(server=server))
        else:
            show_close('Parameter "secure_file_priv" is established',
                       details=dict(server=server))
        return result


@notify
@level('medium')
@track
def strict_all_tables_disabled(server: str, username: str,
                               password: str, port: int = 3306) -> bool:
    """Check if STRICT_ALL_TABLES is enabled on MySQL server."""
    try:
        mydb = _get_mysql_cursor(server, username, password, port)
    except ConnError as exc:
        show_unknown('There was an error connecting to MySQL engine',
                     details=dict(server=server, user=username,
                                  error=str(exc)))
        return False
    else:
        mycursor = mydb.cursor()

        query = "SHOW VARIABLES LIKE 'sql_mode'"
        try:
            mycursor.execute(query)
        except mysql.connector.errors.ProgrammingError as exc:
            show_unknown('There was an error executing query',
                         details=dict(server=server, username=username,
                                      error=str(exc).replace(':', ',')))
            return False

        result = 'STRICT_ALL_TABLES' not in list(mycursor)[0][1]

        if result:
            show_open('STRICT_ALL_TABLES not enabled on by server',
                      details=dict(server=server))
        else:
            show_close('STRICT_ALL_TABLES enabled on by server',
                       details=dict(server=server))
        return result


@notify
@level('medium')
@track
def log_error_disabled(server: str, username: str, password: str,
                       port: int = 3306) -> bool:
    """Check if 'log_error' parameter is set on MySQL server."""
    try:
        mydb = _get_mysql_cursor(server, username, password, port)
    except ConnError as exc:
        show_unknown('There was an error connecting to MySQL engine',
                     details=dict(server=server, user=username,
                                  error=str(exc)))
        return False
    else:
        mycursor = mydb.cursor()

        query = "SHOW variables LIKE 'log_error'"
        try:
            mycursor.execute(query)
        except mysql.connector.errors.ProgrammingError as exc:
            show_unknown('There was an error executing query',
                         details=dict(server=server, username=username,
                                      error=str(exc).replace(':', ',')))
            return False

        result = ('log_error', '') in list(mycursor)

        if result:
            show_open('Parameter "log_error" not set on server',
                      details=dict(server=server))
        else:
            show_close('Parameter "log_error" is set on server',
                       details=dict(server=server))
        return result


@notify
@level('medium')
@track
def logs_on_system_fs(server: str, username: str, password: str,
                      port: int = 3306) -> bool:
    """Check if logs are stored on a system filesystem on server."""
    try:
        mydb = _get_mysql_cursor(server, username, password, port)
    except ConnError as exc:
        show_unknown('There was an error connecting to MySQL engine',
                     details=dict(server=server, user=username,
                                  error=str(exc)))
        return False
    else:
        mycursor = mydb.cursor()

        query = "SELECT @@global.log_bin_basename"
        try:
            mycursor.execute(query)
        except mysql.connector.errors.ProgrammingError as exc:
            show_unknown('There was an error executing query',
                         details=dict(server=server, username=username,
                                      error=str(exc).replace(':', ',')))
            return False

        _result = list(mycursor)[0][0]
        result = _result.startswith('/var') or _result.startswith('/usr')

        if result:
            show_open('Logs are stored on system filesystems on server',
                      details=dict(server=server))
        else:
            show_close('Logs are outside system filesystems on server',
                       details=dict(server=server))
        return result


@notify
@level('low')
@track
def logs_verbosity_low(server: str, username: str, password: str,
                       port: int = 3306) -> bool:
    """Check if logs verbosity includes errors, warnings and notes."""
    try:
        mydb = _get_mysql_cursor(server, username, password, port)
    except ConnError as exc:
        show_unknown('There was an error connecting to MySQL engine',
                     details=dict(server=server, user=username,
                                  error=str(exc)))
        return False
    else:
        mycursor = mydb.cursor()

        query = "SHOW GLOBAL VARIABLES LIKE 'log_error_verbosity'"
        try:
            mycursor.execute(query)
        except mysql.connector.errors.ProgrammingError as exc:
            show_unknown('There was an error executing query',
                         details=dict(server=server, username=username,
                                      error=str(exc).replace(':', ',')))
            return False

        res = list(mycursor)
        if res:
            verbosity = res[0][1]
            result = verbosity not in ('2', '3')
        else:
            verbosity = 'empty'
            result = True

        if result:
            show_open('Logs verbosity not enough',
                      details=dict(server=server, verbosity=verbosity))
        else:
            show_close('Logs verbosity is sufficient',
                       details=dict(server=server, verbosity=verbosity))
        return result


@notify
@level('high')
@track
def auto_creates_users(server: str, username: str, password: str,
                       port: int = 3306) -> bool:
    """Check if 'NO_AUTO_CREATE_USER' param is set."""
    try:
        mydb = _get_mysql_cursor(server, username, password, port)
    except ConnError as exc:
        show_unknown('There was an error connecting to MySQL engine',
                     details=dict(server=server, user=username,
                                  error=str(exc)))
        return False
    else:
        mycursor = mydb.cursor()

        queries = ['SELECT @@global.sql_mode', 'SELECT @@session.sql_mode']
        result = False
        for query in queries:
            try:
                mycursor.execute(query)
            except mysql.connector.errors.ProgrammingError as exc:
                show_unknown('There was an error executing query',
                             details=dict(server=server, username=username,
                                          error=str(exc).replace(':', ',')))
                return False

            _result = list(mycursor)[0][0]
            result = 'NO_AUTO_CREATE_USER' not in _result
            if result:
                break

        if result:
            show_open('Param "NO_AUTO_CREATE_USER" not set on server',
                      details=dict(server=server))
        else:
            show_close('Param "NO_AUTO_CREATE_USER" is set on server',
                       details=dict(server=server))
        return result


@notify
@level('high')
@track
def has_users_without_password(server: str, username: str,
                               password: str, port: int = 3306) -> bool:
    """Check if users have a password set."""
    try:
        mydb = _get_mysql_cursor(server, username, password, port)
    except ConnError as exc:
        show_unknown('There was an error connecting to MySQL engine',
                     details=dict(server=server, user=username,
                                  error=str(exc)))
        return False
    else:
        mycursor = mydb.cursor()

        query = 'select user from mysql.user where password=""'
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
            show_open('There are users without password on server',
                      details=dict(server=server,
                                   users=", ".join([x[0].decode()
                                                    for x in _result])))
        else:
            show_close('All users have passwords on server',
                       details=dict(server=server))
        return result


@notify
@level('high')
@track
def password_expiration_unsafe(server: str, username: str,
                               password: str, port: int = 3306) -> bool:
    """Check if password expiration time is safe."""
    try:
        mydb = _get_mysql_cursor(server, username, password, port)
    except ConnError as exc:
        show_unknown('There was an error connecting to MySQL engine',
                     details=dict(server=server, user=username,
                                  error=str(exc)))
        return False
    else:
        mycursor = mydb.cursor()

        query = 'SHOW VARIABLES LIKE "default_password_lifetime"'
        try:
            mycursor.execute(query)
        except mysql.connector.errors.ProgrammingError as exc:
            show_unknown('There was an error executing query',
                         details=dict(server=server, username=username,
                                      error=str(exc).replace(':', ',')))
            return False

        _result = list(mycursor)
        if not _result:
            result = True
        elif int(_result[0][1]) > 90:
            result = True
        else:
            result = False

        if result:
            show_open('Password lifetime is unsafe',
                      details=dict(server=server))

        else:
            show_close('Password lifetime is safe',
                       details=dict(server=server))
        return result


@notify
@level('high')
@track
def password_equals_to_user(server: str, username: str,
                            password: str, port: int = 3006) -> bool:
    """Check if users' password is the same username."""
    try:
        mydb = _get_mysql_cursor(server, username, password, port)
    except ConnError as exc:
        show_unknown('There was an error connecting to MySQL engine',
                     details=dict(server=server, user=username,
                                  error=str(exc)))
        return False
    else:
        mycursor = mydb.cursor()

        query = 'SELECT User,password FROM mysql.user \
WHERE BINARY password=CONCAT("*", UPPER(SHA1(UNHEX(SHA1(user)))))'
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
            show_open('There are users with the password=username',
                      details=dict(server=server,
                                   users=", ".join([x[0].decode()
                                                    for x in _result])))
        else:
            show_close('All users have passwords different to the username',
                       details=dict(server=server))
        return result


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
