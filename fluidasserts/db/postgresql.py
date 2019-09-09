# -*- coding: utf-8 -*-

"""Module for Dynamic Application Security Testing of PostgreSQL Databases."""

# standard imports
from typing import Any, Dict, Iterator, List, NamedTuple, Optional, Tuple
from contextlib import contextmanager

# 3rd party imports
import psycopg2

# local imports
from fluidasserts import Unit, LOW, MEDIUM, HIGH, DAST, OPEN, CLOSED
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


def _get_var(connection_string: ConnectionString,
             variable_name: str,
             case_insensitive: bool = True) -> str:
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
            var_value = var_value.lower() if case_insensitive else var_value
    return var_value


def _execute(connection_string: ConnectionString,
             query: str,
             variables: Optional[Dict[str, Any]]) -> Iterator[Any]:
    """Yield the result of executing a command."""
    with database(connection_string) as (_, cursor):
        cursor.execute(query, variables)
        yield from cursor


def _get_result_as_tuple(*,
                         host: str, port: int,
                         msg_open: str, msg_closed: str,
                         vulns: List[str], safes: List[str]) -> tuple:
    """Return the tuple version of the Result object."""
    vuln_units: List[Unit] = []
    safe_units: List[Unit] = []

    if vulns:
        vuln_units.append(Unit(where=f'{host}:{port}',
                               specific=vulns))
    if safes:
        safe_units.append(Unit(where=f'{host}:{port}',
                               specific=safes))

    if vulns:
        return OPEN, msg_open, vuln_units, safe_units
    return CLOSED, msg_closed, vuln_units, safe_units


@contextmanager
def database(connection_string: ConnectionString) -> Iterator[Tuple[Any, Any]]:
    """
    Context manager to get a safe connection and a cursor.

    :param connection_string: Connection parameter and credentials.
    :returns: A tuple of (connection object, cursor object).
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
@unknown_if(psycopg2.Error)
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


@api(risk=MEDIUM, kind=DAST)
@unknown_if(psycopg2.Error)
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
            raise exc

    vulns: List[str] = []
    safes: List[str] = []

    (safes if supports_ssl else vulns).append(
        msg_closed if supports_ssl else msg_open)

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(psycopg2.Error)
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
                not configured to log all database transactions, and other
                system variables as described in the check output are not set
                to the specified values.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    connection_string: ConnectionString = \
        ConnectionString(dbname, user, password, host, port, 'prefer')

    is_safe: bool
    vulns: List[str] = []
    safes: List[str] = []

    #
    # Needed to enable logging
    #

    is_safe = _get_var(connection_string, 'logging_collector') == 'on'
    (safes if is_safe else vulns).append(
        'logging_collector must be set to on')

    is_safe = _get_var(connection_string, 'log_statement') == 'all'
    (safes if is_safe else vulns).append(
        'log_statement must be set to all')

    is_safe = bool(_get_var(connection_string, 'log_directory'))
    (safes if is_safe else vulns).append(
        'log_directory must be set')

    is_safe = bool(_get_var(connection_string, 'log_filename'))
    (safes if is_safe else vulns).append(
        'log_filename must be set')

    #
    # Below are hardening configurations
    #

    is_safe = _get_var(connection_string, 'log_checkpoints') == 'on'
    (safes if is_safe else vulns).append(
        'log_checkpoints must be set to on')

    # csvlog is just a format, syslog and eventlog have problems
    # use this in conjunction with logging_collector 'on' for a strong setting
    is_safe = 'stderr' in _get_var(connection_string, 'log_destination')
    (safes if is_safe else vulns).append(
        'log_destination must be set to stderr')

    accepted = ('default', 'verbose')
    is_safe = _get_var(connection_string, 'log_error_verbosity') in accepted
    (safes if is_safe else vulns).append(
        'log_error_verbosity must be set to default or verbose')

    #
    # Repudiation
    #

    is_safe = _get_var(connection_string, 'log_connections') == 'on'
    (safes if is_safe else vulns).append(
        'log_connections must be set to on')

    is_safe = _get_var(connection_string, 'log_disconnections') == 'on'
    (safes if is_safe else vulns).append(
        'log_disconnections must be set to on')

    log_line_prefix: str = _get_var(connection_string, 'log_line_prefix')

    for prefix in ('%m', '%u', '%d', '%r', '%c'):
        is_safe = prefix in log_line_prefix
        (safes if is_safe else vulns).append(
            f'log_line_prefix must contain {prefix}')

    #
    # Performance
    #

    is_safe = _get_var(connection_string, 'log_duration') == 'on'
    (safes if is_safe else vulns).append(
        'log_duration must be set to on')

    is_safe = _get_var(connection_string, 'log_lock_waits') == 'on'
    (safes if is_safe else vulns).append(
        'log_lock_waits must be set to on')

    # Disable log_statement_stats
    #   Enable log_executor_stats
    #   Enable log_parser_stats
    #   Enable log_planner_stats
    # For a detailed log
    is_safe = _get_var(connection_string, 'log_statement_stats') == 'off'
    (safes if is_safe else vulns).append(
        'log_statement_stats must be set to on')

    is_safe = _get_var(connection_string, 'log_executor_stats') == 'on'
    (safes if is_safe else vulns).append(
        'log_executor_stats must be set to on')

    is_safe = _get_var(connection_string, 'log_parser_stats') == 'on'
    (safes if is_safe else vulns).append(
        'log_parser_stats must be set to on')

    is_safe = _get_var(connection_string, 'log_planner_stats') == 'on'
    (safes if is_safe else vulns).append(
        'log_planner_stats must be set to on')

    is_safe = _get_var(connection_string, 'log_autovacuum_min_duration') == '0'
    (safes if is_safe else vulns).append(
        'log_autovacuum_min_duration must be set to 0')

    #
    # Logging levels
    #

    is_safe = _get_var(connection_string, 'log_min_duration_statement') == '0'
    (safes if is_safe else vulns).append(
        'log_min_duration_statement must be set to 0')

    is_safe = _get_var(connection_string, 'log_min_error_statement') == 'error'
    (safes if is_safe else vulns).append(
        'log_min_error_statement must be set to error')

    is_safe = _get_var(connection_string, 'log_min_messages') == 'warning'
    (safes if is_safe else vulns).append(
        'log_min_messages must be set to warning')

    is_safe = _get_var(connection_string, 'log_replication_commands') == 'on'
    (safes if is_safe else vulns).append(
        'log_replication_commands must be set to on')

    #
    # Avoid overwriting logs !
    #

    is_safe = _get_var(connection_string, 'log_truncate_on_rotation') == 'off'
    (safes if is_safe else vulns).append(
        'log_truncate_on_rotation must be set to off')

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open='PostgreSQL has not logging enabled',
        msg_closed='PostgreSQL has logging enabled',
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(psycopg2.Error)
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

    # data_checksums must be 'on'
    safe_data_checksums: bool = \
        _get_var(connection_string, 'data_checksums') == 'on'

    # ignore_checksum_failure must be 'off'
    safe_ignore_checksum_fail: bool = \
        _get_var(connection_string, 'ignore_checksum_failure') == 'off'

    vulns: List[str] = []
    safes: List[str] = []

    (safes if safe_data_checksums else vulns).append(
        'data_checksums must be set to on')

    (safes if safe_ignore_checksum_fail else vulns).append(
        'ignore_checksum_failure must be set to off')

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open='PostgreSQL has data checksums disabled',
        msg_closed='PostgreSQL has data checksums enabled',
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(psycopg2.Error)
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

    vulns: List[str] = []
    safes: List[str] = []

    (vulns if vuln_encryption_1 else safes).append(
        'password_encryption must not be set to off')

    (vulns if vuln_encryption_2 else safes).append(
        'password_encryption must not be set to on (alias for md5)')

    (vulns if vuln_encryption_3 else safes).append(
        'password_encryption must not be set to md5')

    (safes if safe_encryption else vulns).append(
        'password_encryption must be set to scram-sha-256')

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open='PostgreSQL has insecure password_encryption',
        msg_closed='PostgreSQL has secure password_encryption',
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(psycopg2.Error)
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

    vulns: List[str] = []
    safes: List[str] = []

    query: str = 'SELECT usename, passwd FROM pg_shadow'

    safe_digests = ('scram-sha-256',)

    for usename, passwd in _execute(connection_string, query, {}):
        is_safe: bool = any(passwd.lower().startswith(s) for s in safe_digests)
        assertion: str = 'securely' if is_safe else 'insecurely'
        specific: str = f'{usename} user password is {assertion} stored'
        (safes if is_safe else vulns).append(specific)

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open='PostgreSQL has insecurely stored passwords',
        msg_closed='PostgreSQL has safely stored passwords',
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(psycopg2.Error)
def has_insecure_file_permissions(dbname: str,
                                  user: str, password: str,
                                  host: str, port: int) -> tuple:
    """
    Check if database's data directory and log files have insecure permissions.

    By default PostgreSQL set the **data_directory** file permissions
    (**data_directory_mode**) to **0700**,
    and the generated log files permissions (**log_file_mode**) at
    **log_directory**/**log_filename** to **0600**.

    This file permissions are reasonable, and must be kept like that!

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.
    :returns: - ``OPEN`` if **data_directory_mode** or **log_file_mode** are
                not set to **0700** and **0600**.
              - ``UNKNOWN`` on errors,
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    connection_string: ConnectionString = \
        ConnectionString(dbname, user, password, host, port, 'prefer')

    is_safe: bool
    accepted: tuple

    vulns: List[str] = []
    safes: List[str] = []

    accepted = ('700', '0700')
    is_safe = _get_var(connection_string, 'data_directory_mode') in accepted
    (safes if is_safe else vulns).append(
        'data_directory_mode must be set to 0700')

    accepted = ('600', '0600')
    is_safe = _get_var(connection_string, 'log_file_mode') in accepted
    (safes if is_safe else vulns).append(
        'log_file_mode must be set to 0600')

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open='PostgreSQL has data checksums disabled',
        msg_closed='PostgreSQL has data checksums enabled',
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM,
     kind=DAST,
     references=[
         'https://www.stigviewer.com/'
         'stig/postgresql_9.x/2017-01-20/finding/V-72863',
         'https://www.postgresql.org/'
         'docs/current/runtime-config-connection.html',
     ])
@unknown_if(psycopg2.Error)
def allows_too_many_concurrent_connections(dbname: str,
                                           user: str, password: str,
                                           host: str, port: int,
                                           max_connections: int = 100
                                           ) -> tuple:
    """
    Check if number of allowed connections exceed the organization threshold.

    An unlimited or high number of concurrent connections to PostgreSQL
    could allow a successful Denial of Service (DoS) attack by exhausting
    connection resources; and a system can also fail or be degraded by an
    overload of legitimate users.

    Limiting the number of concurrent sessions per user is helpful in
    reducing these risks.

    See `S.T.I.G. <https://www.stigviewer.com/stig/
    postgresql_9.x/2017-01-20/finding/V-72863>`_.

    See `PostgreSQL doc <https://www.postgresql.org/
    docs/current/runtime-config-connection.html>`_.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.
    :param max_connections: organization defined number of concurrent
                            connections, a hundred is PostgreSQL's default.
                            However, hardware and network settings are highly
                            coupled to a propper value for this setting.
    :returns: - ``OPEN`` if **max_connections** system variable is greater than
                the specified **max_connections** parameter.
              - ``UNKNOWN`` on errors,
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    connection_string: ConnectionString = \
        ConnectionString(dbname, user, password, host, port, 'prefer')

    vulns: List[str] = []
    safes: List[str] = []

    value: str = _get_var(connection_string, 'max_connections')
    is_safe: bool = value and int(value) <= max_connections

    (safes if is_safe else vulns).append(
        f'max_connections must be less than {max_connections}')

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open='PostgreSQL allows too many concurrent connections',
        msg_closed=('PostgreSQL allows a reasonable number of '
                    'concurrent connections'),
        vulns=vulns,
        safes=safes)
