# Standard libraries
from typing import (
    Callable,
    NamedTuple,
    Optional,
)
# Third party libraries
# Local libraries
from postgres_client import (
    connection as connection_module,
    cursor as cursor_module,
)
from postgres_client.connection import (
    Credentials,
    DatabaseID,
    DbConnection,
)
from postgres_client.cursor import (
    Cursor,
    CursorExeAction,
    CursorFetchAction,
    DynamicSQLargs,
)


class Client(NamedTuple):
    execute: Callable[[str, Optional[DynamicSQLargs]], CursorExeAction]
    fetchall: Callable[[], CursorFetchAction]
    fetchone: Callable[[], CursorFetchAction]
    drop_access_point: Callable[[], None]


class _Client(NamedTuple):
    cursor: Cursor
    connection: DbConnection
    close: Callable[[], None]


def _drop_access_point(cursor: Cursor, connection: DbConnection) -> None:
    cursor.close()
    connection.close()


def new_client(
    db_id: DatabaseID,
    cred: Credentials
) -> Client:
    db_connection = connection_module.connect(db_id, cred)
    db_cursor = cursor_module.new_cursor(db_connection)

    def close() -> None:
        _drop_access_point(db_cursor, db_connection)

    return Client(
        execute=db_cursor.execute,
        fetchall=db_cursor.fetchall,
        fetchone=db_cursor.fetchone,
        drop_access_point=close,
    )
