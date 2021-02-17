# Standard libraries
from typing import (
    Any,
    Callable,
    NamedTuple,
    Optional,
)
# Third party libraries
import psycopg2 as postgres
import psycopg2.extensions as postgres_extensions
# Local libraries


class DbConnection(NamedTuple):
    close: Callable[[], None]
    commit: Callable[[], None]
    get_cursor: Callable[[], Any]
    options: 'Options'


class ConnectionID(NamedTuple):
    dbname: str
    user: str
    password: str
    host: str
    port: str


class DatabaseID(NamedTuple):
    db_name: str
    host: str
    port: int


class Credentials(NamedTuple):
    user: str
    password: str

    def __repr__(self) -> str:
        return "Creds(user={})".format(self.user)


class Options(NamedTuple):
    isolation_lvl: Optional[int] = \
        postgres_extensions.ISOLATION_LEVEL_AUTOCOMMIT


DbConn = Any


def adapt_connection(
    connection: DbConn, options: Options = Options()
) -> DbConnection:
    connection.set_session(readonly=False)
    connection.set_isolation_level(options.isolation_lvl)
    return DbConnection(
        close=connection.close,
        get_cursor=connection.cursor,
        commit=connection.commit,
        options=options
    )


def connect(
    db_id: DatabaseID,
    creds: Credentials,
    options: Options = Options()
) -> DbConnection:
    dbcon = postgres.connect(
        dbname=db_id.db_name,
        user=creds.user,
        password=creds.password,
        host=db_id.host,
        port=db_id.port
    )
    return adapt_connection(dbcon, options)
