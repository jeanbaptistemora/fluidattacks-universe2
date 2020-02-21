# -*- coding: utf-8 -*-

# pylint: disable=too-many-lines
"""``Dynamic Application Security Testing`` Suite of Microsoft SQL Server."""

# standard imports
from contextlib import contextmanager
from typing import Any, Dict, Iterable, List, NamedTuple, Optional, Tuple

# 3rd party imports
import pyodbc
from pyodbc import Connection, Cursor

# local imports
from fluidasserts import DAST, HIGH, LOW, MEDIUM
from fluidasserts.db import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if

ConnectionString = NamedTuple('ConnectionString', [
    ('dbname', str),
    ('user', str),
    ('password', str),
    ('host', str),
    ('port', int),
])


def _is_auth_error(exception: pyodbc.InterfaceError) -> bool:
    """Return True if the exception is an authentication exception."""
    return exception.args[0] == '28000'


def _is_xp_cmdshell_error(exception: pyodbc.OperationalError) -> bool:
    """Return True if the exception is an xp_cmdshell exception."""
    return exception.args[0] == 15281


def _is_permission_error(exception: pyodbc.ProgrammingError) -> bool:
    """Return True if the exception is an permission exception."""
    return '42000' in exception.args[0]


def _is_compatibility_error(exception: pyodbc.OperationalError) -> bool:
    """Return True if the exception is an pecompatibility exception."""
    return exception.args[0] == 16202


def _is_auth_permission_error(exception: pyodbc.Error) -> bool:
    allow_exceptions = [_is_permission_error, _is_auth_error]
    return any(map(lambda x: x(exception), allow_exceptions))


@contextmanager
def _execute(connection_string: ConnectionString,
             query: str,
             variables: Optional[Dict[str, Any]] = None) -> Cursor:
    """Cursor with state after execute a query."""
    with database(connection_string) as (_, cursor):
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
def database(connection_string: ConnectionString
             ) -> Iterable[Tuple[Connection, Cursor]]:
    """
    Context manager to get a safe connection and a cursor.

    :param connection_string: Connection parameter and credentials.
    :returns: A tuple of (connection object, cursor object).
    """
    server = f'{connection_string.host}'
    server = f'{server},{str(connection_string.port)}' \
        if connection_string.port else f'{server}'
    dbname = connection_string.dbname
    username = connection_string.user
    password = connection_string.password
    connection: Connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={dbname};'
        f'UID={username};'
        f'PWD={password}',
        timeout=5)
    try:
        cursor = connection.cursor()
        try:
            yield connection, cursor
        finally:
            cursor.close()
    finally:
        connection.close()


def _check_permission(connection_string: ConnectionString,
                      permission: str) -> List[str]:
    """Check if the permission is assigned to any account."""
    vulns, safes = [], []
    query = """
            SELECT who.name, what.permission_name
            FROM sys.server_permissions what
                     INNER JOIN sys.server_principals who
                                ON who.principal_id = what.grantee_principal_id
            WHERE who.name NOT LIKE '##MS%##'
              AND who.type_desc <> 'SERVER_ROLE'"""
    try:
        with database(connection_string) as (_, cursor):
            accounts = cursor.execute(query).fetchall()
            for account in accounts:
                (vulns
                 if account.permission_name.lower() == permission.lower() else
                 safes).append(
                     (f'sys.server_principals.{account.name}',
                      (f'{permission} permission must only be granted to'
                       ' individual administration accounts through roles.')))

    except (pyodbc.ProgrammingError, pyodbc.OperationalError) as exc:
        if not _is_auth_permission_error(exc):
            raise exc

    return (vulns, safes)


def _check_configuration(connection_string: ConnectionString,
                         configuration: str) -> bool:
    """Check if a system configuration option is enabled."""
    query = f"""SELECT 1
                FROM master.sys.configurations
                WHERE lower(name) = '{configuration.lower()}'
                  AND (value_in_use = 1 or value = 1)"""  # nosec
    try:
        with database(connection_string) as (_, cursor):
            return bool(cursor.execute(query).fetchone())

    except (pyodbc.OperationalError, pyodbc.InterfaceError) as exc:
        if not _is_permission_error(exc):
            raise exc


@api(risk=LOW, kind=DAST)
@unknown_if(pyodbc.OperationalError, pyodbc.InterfaceError)
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
        with database(connection_string):
            success = True
    except pyodbc.InterfaceError as exc:
        if not _is_auth_error(exc):
            raise exc

    vulns: List[str] = []
    safes: List[str] = []

    (vulns if success else safes).append(
        ('master',
         'server database is accessible with given credentials'))

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(pyodbc.OperationalError, pyodbc.InterfaceError)
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
    msg_open: str = 'The user can execute OS commands'
    msg_closed: str = 'The user can\'t execute OS commands'

    vulns: List[str] = []
    safes: List[str] = []
    (vulns if _check_configuration(connection_string,
                                   'xp_cmdshell') else
     safes).append(('master.sys.configuration.xp_cmdshell',
                    'must disabled procedure xp_cmdshell'))

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(pyodbc.OperationalError, pyodbc.InterfaceError)
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

    (vulns if success else safes).append(
        (database, msg_open if success else msg_closed))

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(pyodbc.OperationalError, pyodbc.InterfaceError)
def has_login_password_expiration_disabled(dbname: str,
                                           user: str,
                                           password: str,
                                           host: str,
                                           port: int) -> Tuple:
    """
    Check if login password expiration policy is disabled.

    Unchanged passwords provide a means for compromised passwords to be used
    for unauthorized access to DBMS accounts over a long period of time.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.

    :returns: - ``OPEN`` if there are logins that have password expiration
                 policy disabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    vulns: List[str] = []
    safes: List[str] = []

    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port)

    msg_open: str = 'Loggings have password expiration policy disabled.'
    msg_closed: str = 'Loggings have password expiration policy enabled.'

    try:
        with database(connection_string) as (_, cursor):
            cursor.execute(
                """select name, is_expiration_checked
                   from master.sys.sql_logins
                   where type = 'S'
                     and name not in ('##MS_PolicyEventProcessingLogin##',
                     '##MS_PolicyTsqlExecutionLogin##')""")
            for row in cursor:
                value = {}
                for des_name in enumerate(row.cursor_description):
                    value[des_name[1][0]] = row[des_name[0]]
                (vulns if not value['is_expiration_checked'] else
                 safes).append((f'master.sys.sql_logins.{value["name"]}',
                                'login password must expirate'))
    except (pyodbc.ProgrammingError, pyodbc.OperationalError) as exception:
        if not _is_auth_permission_error(exception):
            raise exception

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(pyodbc.OperationalError, pyodbc.ProgrammingError)
def has_enabled_ad_hoc_queries(dbname: str,
                               user: str,
                               password: str,
                               host: str,
                               port: int) -> Tuple:
    """
    Check if Ad Hoc Distributed Queries option is enabled.

    Ad hoc queries allow undefined access to remote database sources.
    Access to untrusted databases could result in execution of malicious
    applications and/or a compromise of local data confidentiality and
    integrity.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.

    :returns: - ``OPEN`` if ad hoc distributed queries option is enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    vulns: List[str] = []
    safes: List[str] = []

    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port)

    msg_open: str = 'Ad Hoc distributed queries option is enabled.'
    msg_closed: str = 'Ad Hoc distributed queries option is disabled.'

    (vulns if _check_configuration(connection_string,
                                   'ad hoc distributed queries') else
     safes).append(('master.sys.configuration.ad hoc distributed queries',
                    'must disable ad hoc distributed queries config option'))

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(pyodbc.OperationalError, pyodbc.ProgrammingError)
def can_alter_any_database(dbname: str,
                           user: str,
                           password: str,
                           host: str,
                           port: int) -> Tuple:
    """
    Check if any user accounts have access to **ALTER ANY DATABASE**.

    SQL Server's **ALTER ANY DATABASE** permission is a high server-level
    privilege that must only be granted to individual administration accounts
    through roles.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.

    :returns: - ``OPEN`` if there are users that have access to
                 **ALTER ANY DATABASE**
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    vulns: List[str] = []
    safes: List[str] = []

    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port)

    msg_open: str = 'User accounts have access to ALTER ANY DATABASE.'
    msg_closed: str = 'User accounts do not have access to ALTER ANY DATABASE.'

    vulns, safes = _check_permission(connection_string, 'ALTER ANY DATABASE')

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(pyodbc.OperationalError, pyodbc.InterfaceError)
def has_password_policy_check_disabled(dbname: str,
                                       user: str,
                                       password: str,
                                       host: str,
                                       port: int) -> Tuple:
    """
    Check if login passwords are tested for complexity requirements.

    Weak passwords are a primary target for attack to gain unauthorized access
    to databases and other systems. Where username/password is used for
    identification and authentication to the database, requiring the use of
    strong passwords can help prevent simple and more sophisticated methods
    for guessing.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.

    :returns: - ``OPEN`` if there are logins that have password policy
                 complexity check disabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    vulns: List[str] = []
    safes: List[str] = []

    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port)

    msg_open: str = \
        'Passwords are not verified to meet complexity requirements.'
    msg_closed: str = 'Passwords are verified to meet complexity requirements.'

    try:
        with database(connection_string) as (_, cursor):
            cursor.execute("""SELECT is_policy_checked, name FROM
                              master.sys.sql_logins WHERE type = 'S'
                              AND name NOT LIKE '##MS%##'""")
            for login in cursor:
                (vulns if not login.is_policy_checked else safes).append(
                    (f'master.sys.sql_logins.{login.name}',
                     'must enable password policy check'))

    except (pyodbc.InterfaceError, pyodbc.OperationalError) as exc:
        if not _is_auth_permission_error(exc):
            raise exc
    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(pyodbc.OperationalError, pyodbc.InterfaceError)
def has_xps_option_enabled(dbname: str, user: str, password: str, host: str,
                           port: int) -> Tuple:
    """
    Check if agent XPs option is enabled.

    The Agent XPs are extended stored procedures used by the SQL Server Agent
    that provide privileged actions that run externally to the DBMS under the
    security context of the SQL Server Agent service account. If these
    procedures are available from a database session, an exploit to the SQL
    Server instance could result in a compromise of the host system and
    external SQL Server resources.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.

    :returns: - ``OPEN`` if agent XPs option is enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    vulns: List[str] = []
    safes: List[str] = []

    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port)

    msg_open: str = 'Agent XPs Option is Enabled'
    msg_closed: str = 'Agent XPs Option is Disabled'

    (vulns if _check_configuration(connection_string, 'agent xps') else
     safes).append(
         ('master.sys.configuration.agent xps',
          'Must disable Agent XPs Option.'))

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(pyodbc.OperationalError, pyodbc.InterfaceError)
def has_asymmetric_keys_with_unencrypted_private_keys(dbname: str,
                                                      user: str,
                                                      password: str,
                                                      host: str,
                                                      port: int) -> Tuple:
    """
    Check for asymmetric keys with a private key that is not encrypted.

    Encryption is only effective if the encryption method is robust and the
    keys used to provide the encryption are not easily discovered. Without
    effective encryption, sensitive data is vulnerable to unauthorized access.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.

    :returns: - ``OPEN`` if there are asymmetric keys with unencrypted private
                 keys
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    vulns: List[str] = []
    safes: List[str] = []

    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port)

    msg_open: str = 'Asymmetric keys have unencrypted private keys.'
    msg_closed: str = 'Asymmetric keys have encrypted private keys.'

    try:
        with database(connection_string) as (_, cursor):
            keys = cursor.execute("""SELECT name, pvt_key_encryption_type
                                     FROM sys.asymmetric_keys""").fetchall()
        for key in keys:
            (vulns if key.pvt_key_encryption_type == 'NA' else safes).append(
                (f'{dbname}.asymmetric_keys.{key.name}',
                 'must encrypt the private key'))

    except (pyodbc.OperationalError, pyodbc.InterfaceError) as exc:
        if not _is_auth_permission_error(exc):
            raise exc
    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(pyodbc.OperationalError, pyodbc.InterfaceError)
def has_smo_and_dmo_xps_option_enabled(dbname: str,
                                       user: str,
                                       password: str,
                                       host: str,
                                       port: int) -> Tuple:
    """
    Check if SMO and DMO XPs options are enabled.

    The SMO and DMO XPs are management object extended stored procedures that
    provide highly-privileged actions that run externally to the DBMS under
    the security context of the SQL Server service account. If these procedures
    are available from a database session, an exploit to the SQL Server
    instance could result in a compromise of the host system and external SQL
    Server resources.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.

    :returns: - ``OPEN`` if SMO and DMO XPs options are enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    vulns: List[str] = []
    safes: List[str] = []

    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port)

    msg_open: str = 'SMO and DMO XPs options are enabled.'
    msg_closed: str = 'SMO and DMO XPs options are disablede.'

    (vulns if _check_configuration(connection_string, 'SMO and DMO XPs') else
     safes).append(
         ('master.sys.configuration.SMO and DMO XPs',
          f'Must disable SMO and DMO XPs options.'))

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(pyodbc.OperationalError, pyodbc.ProgrammingError)
def has_contained_dbs_with_auto_close_enabled(dbname: str,
                                              user: str,
                                              password: str,
                                              host: str,
                                              port: int) -> Tuple:
    """
    Check if there are contained databases that are set to AUTO_CLOSE ON.

    Opening contained databases to authenticate a user consumes additional
    server resources and may contribute to a denial of service.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.

    :returns: - ``OPEN`` if there are contained databases that are set to
                 AUTO_CLOSE ON.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    vulns: List[str] = []
    safes: List[str] = []

    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port)

    msg_open: str = 'Contained databases are set to AUTO_CLOSE ON.'
    msg_closed: str = 'Contained databases are set to AUTO_CLOSE OFF.'

    try:
        with database(connection_string) as (_, cursor):
            databases = cursor.execute(
                """SELECT name, is_auto_close_on
                   FROM sys.databases
                   WHERE containment <> 0""").fetchall()
        for database_ in databases:
            (vulns if database_.is_auto_close_on else
             safes).append((f'sys.databases.{database_.name}',
                            'must set AUTO_CLOSE to OFF'))

    except (pyodbc.OperationalError, pyodbc.InterfaceError) as exc:
        if not _is_auth_permission_error(exc):
            raise exc
    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(pyodbc.OperationalError, pyodbc.ProgrammingError)
def can_alter_any_login(dbname: str, user: str, password: str, host: str,
                        port: int) -> Tuple:
    """
    Check if there are accounts that have permission to ``Alter any login``.

    SQL Server's 'Alter any login' permission is a high server-level privilege
    that must only be granted to individual administration accounts through
    roles. If any user accounts have direct access to administrative
    privileges, this access must be removed.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.

    :returns: - ``OPEN`` if there are accounts that have permission to alter
                 any login.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port)

    msg_open: str = 'Accounts have permission to Alter any login.'
    msg_closed: str = 'Accounts do not have permission to Alter any login.'

    vulns, safes = _check_permission(connection_string, 'ALTER ANY LOGIN')

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(pyodbc.OperationalError, pyodbc.ProgrammingError)
def can_control_server(dbname: str,
                       user: str,
                       password: str,
                       host: str,
                       port: int) -> Tuple:
    """
    Check if there are accounts that have permission to ``Control Server``.

    SQL Server's 'Control Server' permission is a high server-level privilege
    that must only be granted to individual administration accounts through
    roles. If any user accounts have direct access to administrative
    privileges, this access must be removed.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.

    :returns: - ``OPEN`` if there are users that have permission to
                 Control Server.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port)

    msg_open: str = 'Accounts have permission to Control Server.'
    msg_closed: str = 'Accounts do not have permission to Control Server.'

    vulns, safes = _check_permission(connection_string, 'CONTROL SERVER')

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(pyodbc.OperationalError, pyodbc.InternalError)
def can_alter_any_credential(dbname: str,
                             user: str,
                             password: str,
                             host: str,
                             port: int) -> Tuple:
    """
    Check if there are accounts that have permission to Alter any credential.

    SQL Server's 'Alter any credential' permission is a high server-level
    privilege that must only be granted to individual administration accounts
    through roles. If any user accounts have direct access to administrative
    privileges, this access must be removed.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.

    :returns: - ``OPEN`` if there are accounts that haver permission to alter
                 any credential.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port)

    msg_open: str = 'Accounts have permission to Alter any credential.'
    msg_closed: str = \
        'Accounts do not have permission to Alter any credential.'

    vulns, safes = _check_permission(connection_string, 'Alter Any Credential')

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(pyodbc.OperationalError, pyodbc.InterfaceError)
def has_sa_account_login_enabled(dbname: str, user: str, password: str,
                                 host: str, port: int) -> Tuple:
    """
    Check if the sa login account is enabled.

    Enforcing the sa login to be disabled reduces the probability of an
    attacker executing brute force attacks against a well-known principal.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.

    :returns: - ``OPEN`` if the sa login account is enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    vulns: List[str] = []
    safes: List[str] = []

    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port)

    msg_open: str = 'SA login account is enabled.'
    msg_closed: str = 'SA login account is disabled.'

    query = """SELECT 1
               FROM master.sys.server_principals
               WHERE sid = 0x01
                 AND is_disabled = 0"""
    try:
        with database(connection_string) as (_, cursor):
            cursor.execute(query)
            (vulns if cursor.fetchone() else
             safes).append(
                 ('master.sys.server_principals',
                  ('must disable the sa account because it could be '
                   'the target of attacks')))

    except (pyodbc.OperationalError, pyodbc.InterfaceError) as exc:
        if not _is_auth_permission_error(exc):
            raise exc
    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(pyodbc.OperationalError, pyodbc.ProgrammingError)
def has_remote_access_option_enabled(dbname: str,
                                     user: str,
                                     password: str,
                                     host: str,
                                     port: int) -> Tuple:
    """
    Check if remote access is enabled.

    The remote access option determines if connections to and from other
    Microsoft SQL Servers are allowed. Remote connections are used to support
    distributed queries and other data access and command executions across
    and between remote database hosts. Remote servers and logins that are not
    properly secured can be used to compromise the server.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.

    :returns: - ``OPEN`` if remote access is enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    vulns: List[str] = []
    safes: List[str] = []

    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port)

    msg_open: str = 'Remote access is enabled.'
    msg_closed: str = 'Remote access is disabled.'

    (vulns if _check_configuration(connection_string, 'remote access') else
     safes).append(('master.sys.configuration.remote access',
                    f'Must disable the remote access.'))
    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(pyodbc.OperationalError, pyodbc.ProgrammingError)
def has_unencrypted_storage_procedures(dbname: str,
                                       user: str,
                                       password: str,
                                       host: str,
                                       port: int) -> Tuple:
    """
    Check if stored procedures are kept in the database without encryption.

    Protect sensitive code and data used in stored procedures code.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.

    :returns: - ``OPEN`` if the sa login account is enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    vulns: List[str] = []
    safes: List[str] = []

    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port)

    msg_open: str = 'Stored Procedures are Kept in non Encrypted Format.'
    msg_closed: str = 'Stored Procedures are Kept in Encrypted Format.'

    query = """SELECT sqlmod.definition, sysobj.name
               FROM sys.sql_modules AS sqlmod (NOLOCK)
                        INNER JOIN sys.objects AS sysobj (NOLOCK)
                                   on sqlmod.object_id = sysobj.object_id
               WHERE sysobj.type = 'P'
                 AND sysobj.is_ms_shipped = 0
               """
    try:
        with database(connection_string) as (_, cursor):
            for procedure in cursor.execute(query).fetchall():
                (vulns if procedure.definition else
                 safes).append((f'sys.objects.{procedure.name}',
                                'must use WITH ENCRYPT option'))

    except (pyodbc.OperationalError, pyodbc.InterfaceError) as exc:
        if not _is_auth_permission_error(exc):
            raise exc
    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(pyodbc.OperationalError, pyodbc.InterfaceError)
def can_shutdown_server(dbname: str,
                        user: str,
                        password: str,
                        host: str,
                        port: int) -> Tuple:
    """
    Check if there are accounts that have permission to Shutdown the Server.

    SQL Server's 'Shutdown' permission is a high server-level
    privilege that must only be granted to individual administration accounts
    through roles. If any user accounts have direct access to administrative
    privileges, this access must be removed.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.

    :returns: - ``OPEN`` if there are users that have permission to
                Shutdown the server.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port)

    msg_open: str = 'Accounts have permission to Shutdown the server.'
    msg_closed: str = 'Accounts do not have permission to Shutdown the server.'

    vulns, safes = _check_permission(connection_string, 'Shutdown')

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(pyodbc.OperationalError, pyodbc.ProgrammingError)
def sa_account_has_not_been_renamed(dbname: str,
                                    user: str,
                                    password: str,
                                    host: str,
                                    port: int) -> Tuple:
    """
    Check if the SA account has not been renamed.

    Enforcing the sa login to be disabled or rename reduces the probability of
    an attacker executing brute force attacks against a well-known principal.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.

    :returns: - ``OPEN`` if the sa login account is enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    vulns: List[str] = []
    safes: List[str] = []

    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port)

    msg_open: str = 'SA login account has not been renamed.'
    msg_closed: str = 'SA login account has been renamed.'

    query = "SELECT 1 FROM master.dbo.syslogins WHERE name = 'sa'"
    try:
        with database(connection_string) as (_, cursor):
            cursor.execute(query)
            (vulns if cursor.fetchone() else safes).append(
                ('master.dbo.syslogins.sa', 'must disabled sa login'))

    except (pyodbc.OperationalError, pyodbc.InterfaceError) as exc:
        if not _is_auth_permission_error(exc):
            raise exc
    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(pyodbc.OperationalError, pyodbc.ProgrammingError)
def has_clr_option_enabled(dbname: str,
                           user: str,
                           password: str,
                           host: str,
                           port: int) -> Tuple:
    """
    Check if CLR option is enabled enabled.

    The clr_enabled parameter configures SQL Server to allow or disallow use of
    Command Language Runtime objects. CLR objects is managed code that
    integrates with the .NET Framework. This is a more secure method than
    external stored procedures, although it still contains some risk.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.

    :returns: - ``OPEN`` if CLR option is enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    vulns: List[str] = []
    safes: List[str] = []

    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port)

    msg_open: str = 'CLR option is enabled.'
    msg_closed: str = 'CLR option is disabled.'

    (vulns if _check_configuration(connection_string, 'clr enabled') else
     safes).append(
         ('master.sys.configuration.clr enabled', 'Must disable CLR option.'))

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
