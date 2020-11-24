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
from postgres_client.cursor import Cursor


class DbConnection(NamedTuple):
    close: Callable[[], None]
    get_cursor: Callable[[], Cursor]


class ConnectionID(NamedTuple):
    dbname: str
    user: str
    password: str
    host: str
    port: str

    def __repr__(self):
        return "ConnectionID(dbname={}, ****)".format(self.dbname)


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
