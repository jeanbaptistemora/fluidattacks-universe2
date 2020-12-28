# Standard libraries
from typing import (
    Any,
    Callable,
    NamedTuple,
)
# Third party libraries
import psycopg2 as postgres
import psycopg2.extensions as postgres_extensions
# Local libraries


class DbConnection(NamedTuple):
    close: Callable[[], None]
    get_cursor: Callable[[], Any]


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
        return "Creds(user={}, password=****)".format(self.user)


class Options(NamedTuple):
    isolation_lvl: Any = postgres_extensions.ISOLATION_LEVEL_AUTOCOMMIT


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
    dbcon.set_session(readonly=False)
    dbcon.set_isolation_level(options.isolation_lvl)
    return DbConnection(
        close=dbcon.close,
        get_cursor=dbcon.cursor
    )


def make_access_point(
    auth: ConnectionID,
    isolation_lvl: Any = postgres_extensions.ISOLATION_LEVEL_AUTOCOMMIT
) -> DbConnection:
    dbcon = postgres.connect(
        dbname=auth.dbname,
        user=auth.user,
        password=auth.password,
        host=auth.host,
        port=auth.port
    )
    dbcon.set_session(readonly=False)
    dbcon.set_isolation_level(isolation_lvl)

    return DbConnection(
        close=dbcon.close,
        get_cursor=dbcon.cursor
    )
