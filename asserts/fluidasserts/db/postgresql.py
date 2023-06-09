# -*- coding: utf-8 -*-

"""
``Dynamic Application Security Testing`` Suite of PostgreSQL Databases.

The entire suite has been tested on the following PostgreSQL releases:

- `Postgres v12 <https://www.postgresql.org/docs/12/index.html>`_.

- `Postgres v11 <https://www.postgresql.org/docs/11/index.html>`_.

- `Postgres v10 <https://www.postgresql.org/docs/10/index.html>`_.

- `Postgres v9.6 <https://www.postgresql.org/docs/9.6/index.html>`_.

- `Postgres v9.5 <https://www.postgresql.org/docs/9.5/index.html>`_.

- `Postgres v9.4 <https://www.postgresql.org/docs/9.4/index.html>`_.
"""


from contextlib import (
    contextmanager,
)
from fluidasserts import (
    DAST,
    HIGH,
    LOW,
    MEDIUM,
)
from fluidasserts.db import (
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import (
    api,
    unknown_if,
)
import psycopg2
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    NamedTuple,
    Optional,
    Tuple,
)

# Containers
#: Container with connection parameters and credentials
ConnectionString = NamedTuple(
    "ConnectionString",
    [
        ("dbname", str),
        ("user", str),
        ("password", str),
        ("host", str),
        ("port", int),
        ("sslmode", str),
    ],
)


def _is_auth_error(exception: psycopg2.Error) -> bool:
    """Return True if the exception is an authentication exception."""
    return "authentication" in str(exception)


def _is_ssl_error(exception: psycopg2.Error) -> bool:
    """Return True if the exception is an SSL exception."""
    return "SSL" in str(exception)


def _execute(
    connection_string: ConnectionString,
    query: str,
    variables: Optional[Dict[str, Any]],
) -> Iterator[Any]:
    """Yield the result of executing a command."""
    with database(connection_string) as (_, cursor):
        cursor.execute(query, variables)
        yield from cursor


def _get_var(
    connection_string: ConnectionString,
    variable_name: str,
    case_insensitive: bool = True,
) -> str:
    """Return the value of a system variable or an empty string."""
    var_value: str = str()
    query: str = """
        SELECT setting FROM pg_settings WHERE name = %(variable_name)s
        """
    variables: Dict[str, str] = {
        "variable_name": variable_name,
    }

    for row in _execute(connection_string, query, variables):
        # Variable is defined
        (var_value,) = row
        break

    return var_value.lower() if case_insensitive else var_value


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
        sslmode=connection_string.sslmode,
    )

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
def have_access(
    dbname: str, user: str, password: str, host: str, port: int
) -> tuple:
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
        dbname, user, password, host, port, "prefer"
    )

    success: bool = False
    msg_open: str = "PostgreSQL is accessible with given credentials"
    msg_closed: str = "PostgreSQL is not accessible with given credentials"

    try:
        with database(connection_string):
            success = True
    except psycopg2.OperationalError as exc:
        if not _is_auth_error(exc):
            raise exc

    vulns: List[str] = []
    safes: List[str] = []

    (vulns if success else safes).append(
        (dbname, "database is accessible with given credentials")
    )

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(psycopg2.Error)
def does_not_support_ssl(
    dbname: str, user: str, password: str, host: str, port: int
) -> tuple:
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
    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port, "require"
    )

    supports_ssl: bool = False
    msg_open: str = "PostgreSQL does not support SSL connections"
    msg_closed: str = "PostgreSQL supports SSL connections"

    try:
        with database(connection_string):
            supports_ssl = True
    except psycopg2.OperationalError as exc:
        if not _is_ssl_error(exc):
            raise exc

    vulns: List[str] = []
    safes: List[str] = []

    (safes if supports_ssl else vulns).append(
        (dbname, "must enable ssl connections")
    )

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(psycopg2.Error)
def has_not_logging_enabled(
    dbname: str, user: str, password: str, host: str, port: int
) -> tuple:
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
    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port, "prefer"
    )

    is_safe: bool
    vulns, safes = [], []

    #
    # Needed to enable logging
    #

    is_safe = _get_var(connection_string, "logging_collector") == "on"
    (safes if is_safe else vulns).append(
        (
            "pg_settings.logging_collector",
            "logging_collector must be set to on",
        )
    )

    is_safe = _get_var(connection_string, "log_statement") == "all"
    (safes if is_safe else vulns).append(
        ("pg_settings.log_statement", "log_statement must be set to all")
    )

    is_safe = bool(_get_var(connection_string, "log_directory"))
    (safes if is_safe else vulns).append(
        ("pg_settings.log_directory", "log_directory must be set")
    )

    is_safe = bool(_get_var(connection_string, "log_filename"))
    (safes if is_safe else vulns).append(
        ("pg_settings.log_filename", "log_filename must be set")
    )

    #
    # Below are hardening configurations
    #

    is_safe = _get_var(connection_string, "log_checkpoints") == "on"
    (safes if is_safe else vulns).append(
        ("pg_settings.log_checkpoints", "log_checkpoints must be set to on")
    )

    # csvlog is just a format, syslog and eventlog have problems
    # use this in conjunction with logging_collector 'on' for a strong setting
    is_safe = "stderr" in _get_var(connection_string, "log_destination")
    (safes if is_safe else vulns).append(
        (
            "pg_settings.log_destination",
            "log_destination must be set to stderr",
        )
    )

    accepted = ("default", "verbose")
    is_safe = _get_var(connection_string, "log_error_verbosity") in accepted
    (safes if is_safe else vulns).append(
        (
            "pg_settings.log_error_verbosity",
            "log_error_verbosity must be set to default or verbose",
        )
    )

    #
    # Repudiation
    #

    is_safe = _get_var(connection_string, "log_connections") == "on"
    (safes if is_safe else vulns).append(
        ("pg_settings.log_connections", "log_connections must be set to on")
    )

    is_safe = _get_var(connection_string, "log_disconnections") == "on"
    (safes if is_safe else vulns).append(
        (
            "pg_settings.log_disconnections",
            "log_disconnections must be set to on",
        )
    )

    log_line_prefix: str = _get_var(connection_string, "log_line_prefix")

    for prefix in ("%m", "%u", "%d", "%r", "%c"):
        is_safe = prefix in log_line_prefix
        (safes if is_safe else vulns).append(
            (
                "pg_settings.log_line_prefix",
                f"log_line_prefix must contain {prefix}",
            )
        )

    #
    # Performance
    #

    is_safe = _get_var(connection_string, "log_duration") == "on"
    (safes if is_safe else vulns).append(
        ("pg_settings.log_duration", "log_duration must be set to on")
    )

    is_safe = _get_var(connection_string, "log_lock_waits") == "on"
    (safes if is_safe else vulns).append(
        ("pg_settings.log_lock_waits", "log_lock_waits must be set to on")
    )

    # Disable log_statement_stats
    #   Enable log_executor_stats
    #   Enable log_parser_stats
    #   Enable log_planner_stats
    # For a detailed log
    is_safe = _get_var(connection_string, "log_statement_stats") == "off"
    (safes if is_safe else vulns).append(
        (
            "pg_settings.log_statement_stats",
            "log_statement_stats must be set to on",
        )
    )

    is_safe = _get_var(connection_string, "log_executor_stats") == "on"
    (safes if is_safe else vulns).append(
        (
            "pg_settings.log_executor_stats",
            "log_executor_stats must be set to on",
        )
    )

    is_safe = _get_var(connection_string, "log_parser_stats") == "on"
    (safes if is_safe else vulns).append(
        ("pg_settings.log_parser_stats", "log_parser_stats must be set to on")
    )

    is_safe = _get_var(connection_string, "log_planner_stats") == "on"
    (safes if is_safe else vulns).append(
        (
            "pg_settings.log_planner_stats",
            "log_planner_stats must be set to on",
        )
    )

    is_safe = _get_var(connection_string, "log_autovacuum_min_duration") == "0"
    (safes if is_safe else vulns).append(
        (
            "pg_settings.log_autovacuum_min_duration",
            "log_autovacuum_min_duration must be set to 0",
        )
    )

    #
    # Logging levels
    #

    is_safe = _get_var(connection_string, "log_min_duration_statement") == "0"
    (safes if is_safe else vulns).append(
        (
            "pg_settings.log_min_duration_statement",
            "log_min_duration_statement must be set to 0",
        )
    )

    is_safe = _get_var(connection_string, "log_min_error_statement") == "error"
    (safes if is_safe else vulns).append(
        (
            "pg_settings.log_min_error_statement",
            "log_min_error_statement must be set to error",
        )
    )

    is_safe = _get_var(connection_string, "log_min_messages") == "warning"
    (safes if is_safe else vulns).append(
        (
            "pg_settings.log_min_messages",
            "log_min_messages must be set to warning",
        )
    )

    is_safe = _get_var(connection_string, "log_replication_commands") == "on"
    (safes if is_safe else vulns).append(
        (
            "pg_settings.log_replication_commands",
            "log_replication_commands must be set to on",
        )
    )

    #
    # Avoid overwriting logs !
    #

    is_safe = _get_var(connection_string, "log_truncate_on_rotation") == "off"
    (safes if is_safe else vulns).append(
        (
            "pg_settings.log_truncate_on_rotation",
            "log_truncate_on_rotation must be set to off",
        )
    )

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open="PostgreSQL has not logging enabled",
        msg_closed="PostgreSQL has logging enabled",
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(psycopg2.Error)
def has_not_data_checksums_enabled(
    dbname: str, user: str, password: str, host: str, port: int
) -> tuple:
    """
    Check if the PostgreSQL implementation has data checksums disabled.

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
    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port, "prefer"
    )

    # data_checksums must be 'on'
    safe_data_checksums: bool = (
        _get_var(connection_string, "data_checksums") == "on"
    )

    # ignore_checksum_failure must be 'off'
    safe_ignore_checksum_fail: bool = (
        _get_var(connection_string, "ignore_checksum_failure") == "off"
    )

    vulns: List[str] = []
    safes: List[str] = []

    (safes if safe_data_checksums else vulns).append(
        ("pg_settings.data_checksums", "data_checksums must be set to on")
    )

    (safes if safe_ignore_checksum_fail else vulns).append(
        (
            "pg_settings.ignore_checksum_failure",
            "ignore_checksum_failure must be set to off",
        )
    )

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open="PostgreSQL has data checksums disabled",
        msg_closed="PostgreSQL has data checksums enabled",
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(psycopg2.Error)
def has_insecure_password_encryption(
    dbname: str, user: str, password: str, host: str, port: int
) -> tuple:
    """
    Check if PostgreSQL implementation stores passwords using weak algorithms.

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
    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port, "prefer"
    )

    # password_encryption must not be 'off'
    vuln_encryption_1: bool = (
        _get_var(connection_string, "password_encryption") == "off"
    )

    # password_encryption must not be 'on' (alias for md5)
    vuln_encryption_2: bool = (
        _get_var(connection_string, "password_encryption") == "on"
    )

    # password_encryption must not be 'md5'
    vuln_encryption_3: bool = (
        _get_var(connection_string, "password_encryption") == "md5"
    )

    secure_digests: tuple = ("scram-sha-256",)

    # password_encryption must be any of `secure_digests`
    safe_encryption: bool = (
        _get_var(connection_string, "password_encryption") in secure_digests
    )

    vulns: List[str] = []
    safes: List[str] = []

    (vulns if vuln_encryption_1 else safes).append(
        (
            "pg_settings.password_encryption",
            "password_encryption must not be set to off",
        )
    )

    (vulns if vuln_encryption_2 else safes).append(
        (
            "pg_settings.password_encryption",
            "password_encryption must not be set to on (alias for md5)",
        )
    )

    (vulns if vuln_encryption_3 else safes).append(
        (
            "pg_settings.password_encryption",
            "password_encryption must not be set to md5",
        )
    )

    (safes if safe_encryption else vulns).append(
        (
            "pg_settings.password_encryption",
            "password_encryption must be set to scram-sha-256",
        )
    )

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open="PostgreSQL has insecure password_encryption",
        msg_closed="PostgreSQL has secure password_encryption",
        vulns=vulns,
        safes=safes,
    )


@api(risk=HIGH, kind=DAST)
@unknown_if(psycopg2.Error)
def has_insecurely_stored_passwords(
    dbname: str, user: str, password: str, host: str, port: int
) -> tuple:
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
    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port, "prefer"
    )

    vulns: List[str] = []
    safes: List[str] = []

    query: str = "SELECT usename, passwd FROM pg_shadow"

    safe_digests = ("scram-sha-256",)

    for usename, passwd in _execute(connection_string, query, {}):
        is_safe: bool = any(passwd.lower().startswith(s) for s in safe_digests)
        assertion: str = "securely" if is_safe else "insecurely"
        specific: str = f"{usename} user password is {assertion} stored"
        (safes if is_safe else vulns).append(("pg_shadow.pg_shadow", specific))

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open="PostgreSQL has insecurely stored passwords",
        msg_closed="PostgreSQL has safely stored passwords",
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(psycopg2.Error)
def has_insecure_file_permissions(
    dbname: str, user: str, password: str, host: str, port: int
) -> tuple:
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
    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port, "prefer"
    )

    is_safe: bool
    accepted: tuple

    vulns: List[str] = []
    safes: List[str] = []

    accepted = ("700", "0700")
    is_safe = _get_var(connection_string, "data_directory_mode") in accepted
    (safes if is_safe else vulns).append(
        (
            "pg_settings.data_directory_mode",
            "data_directory_mode must be set to 0700",
        )
    )

    accepted = ("600", "0600")
    is_safe = _get_var(connection_string, "log_file_mode") in accepted
    (safes if is_safe else vulns).append(
        ("pg_settings.log_file_mode", "log_file_mode must be set to 0600")
    )

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open="PostgreSQL has data checksums disabled",
        msg_closed="PostgreSQL has data checksums enabled",
        vulns=vulns,
        safes=safes,
    )


@api(
    risk=MEDIUM,
    kind=DAST,
    references=[
        "https://www.stigviewer.com/"
        + "stig/postgresql_9.x/2017-01-20/finding/V-72863",
        "https://www.postgresql.org/"
        + "docs/current/runtime-config-connection.html",
    ],
    standards={
        "STIG": "V-72863",
    },
)
@unknown_if(psycopg2.Error)
def allows_too_many_concurrent_connections(
    dbname: str,
    user: str,
    password: str,
    host: str,
    port: int,
    max_connections: int = 100,
) -> tuple:
    """
    Check if number of allowed connections exceed the organization threshold.

    An unlimited or high number of concurrent connections to PostgreSQL
    could allow a successful Denial of Service (DoS) attack by exhausting
    connection resources; and a system can also fail or be degraded by an
    overload of legitimate users.

    Limiting the number of concurrent sessions per user is helpful in
    reducing these risks.

    See:

    - `STIG <https://www.stigviewer.com/stig/
      postgresql_9.x/2017-01-20/finding/V-72863>`_.
    - `PostgreSQL doc <https://www.postgresql.org/
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
    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port, "prefer"
    )

    vulns: List[str] = []
    safes: List[str] = []

    value: str = _get_var(connection_string, "max_connections")
    is_safe: bool = bool(value) and int(value) <= max_connections

    (safes if is_safe else vulns).append(
        (
            "pg_settings.max_connections",
            f"max_connections must be less than {max_connections}",
        )
    )

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open="PostgreSQL allows too many concurrent connections",
        msg_closed=(
            "PostgreSQL allows a reasonable number of "
            "concurrent connections"
        ),
        vulns=vulns,
        safes=safes,
    )


@api(
    risk=MEDIUM,
    kind=DAST,
    references=[
        "https://www.stigviewer.com/"
        + "stig/postgresql_9.x/2017-01-20/finding/V-73037",
        "https://www.postgresql.org/"
        + "docs/current/runtime-config-client.html",
        "https://www.postgresql.org/"
        + "docs/current/runtime-config-connection.html",
    ],
    standards={
        "STIG": "V-73037",
    },
)
@unknown_if(psycopg2.Error)
def does_not_invalidate_session_ids(
    dbname: str,
    user: str,
    password: str,
    host: str,
    port: int,
    statement_timeout: int = 60000,
    tcp_keepalives_idle: int = 7200,
    tcp_keepalives_interval: int = 75,
    tcp_keepalives_count: int = 9,
) -> tuple:
    """
    Check if session IDs are properly invalidated by timing out the connection.

    Session IDs are tokens generated by PostgreSQL to uniquely
    identify a user's (or process's) session.

    Based on this session ID, the Database Management System will make access
    decisions and execute operational logic.

    Having unique session IDs help to reduce the predictability of said
    identifiers, and to prevent **reuse** and **replay** attacks.

    See:

    - `STIG <https://www.stigviewer.com/
      stig/postgresql_9.x/2017-01-20/finding/V-73037>`_.
    - `PostgreSQL Client Connection Defaults <https://www.postgresql.org/
      docs/current/runtime-config-client.html>`_.
    - `PostgreSQL Connections and Authentication <https://www.postgresql.org/
      docs/current/runtime-config-client.html>`_.

    Default TCP keepalives values taken from the
    `TCP Man Pages <https://man7.org/linux/man-pages/man7/tcp.7.html>`_.

    :param dbname: database name.
    :param user: username with access permissions to the database.
    :param password: database password.
    :param host: database ip.
    :param port: database port.
    :param statement_timeout: organization defined timeout in milliseconds for
                              an statement.
    :param tcp_keepalives_idle: organization defined number of seconds of
                                inactivity after which TCP should send a
                                keepalive message to the client.
    :param tcp_keepalives_interval: organization defined number of seconds
                                    after which a TCP keepalive message that is
                                    not acknowledged by the client should be
                                    retransmitted.
    :param tcp_keepalives_count: organization defined number of TCP keepalives
                                 that can be lost before the server's
                                 connection to the client is considered dead.
    :returns: - ``OPEN`` if any of **statement_timeout**,
                **tcp_keepalives_idle**, **tcp_keepalives_interval**, or
                **tcp_keepalives_count** system variables is greater than the
                specified parameters.
              - ``UNKNOWN`` on errors,
              - ``CLOSED`` otherwise.

              Note that setting the **TCP** options to 0 is valid too, as it
              would use the system defaults.
    :rtype: :class:`fluidasserts.Result`
    """
    connection_string: ConnectionString = ConnectionString(
        dbname, user, password, host, port, "prefer"
    )

    vulns: List[str] = []
    safes: List[str] = []

    value: str
    is_safe: bool
    vars_to_check: List[Tuple[str, int, int]] = [
        ("statement_timeout", 1, statement_timeout),
        ("tcp_keepalives_idle", 0, tcp_keepalives_idle),
        ("tcp_keepalives_interval", 0, tcp_keepalives_interval),
        ("tcp_keepalives_count", 0, tcp_keepalives_count),
    ]

    for var_name, min_value, max_value in vars_to_check:
        value = _get_var(connection_string, var_name)
        is_safe = bool(value) and min_value <= int(value) <= max_value
        (safes if is_safe else vulns).append(
            (
                "pg_settings.max_connections",
                (
                    f"{var_name} must be between"
                    f" {min_value} and {max_value}"
                ),
            )
        )

    return _get_result_as_tuple(
        host=host,
        port=port,
        msg_open="PostgreSQL does not properly invalidate session IDs",
        msg_closed="PostgreSQL does properly invalidate session IDs",
        vulns=vulns,
        safes=safes,
    )
