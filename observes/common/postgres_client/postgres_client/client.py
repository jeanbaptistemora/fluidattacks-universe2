# Standard libraries
from typing import (
    Callable,
    NamedTuple,
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
    DbConn,
    DbConnection,
)
from postgres_client.cursor import (
    Cursor,
)


class Client(NamedTuple):
    cursor: Cursor
    connection: DbConnection
    close: Callable[[], None]


def _drop_access_point(cursor: Cursor, connection: DbConnection) -> None:
    cursor.close()
    connection.close()


def _create_client(
    db_connection: DbConnection,
    db_cursor: Cursor,
) -> Client:
    def close() -> None:
        _drop_access_point(db_cursor, db_connection)

    return Client(
        cursor=db_cursor,
        connection=db_connection,
        close=close,
    )


def new_client(
    db_id: DatabaseID,
    cred: Credentials
) -> Client:
    db_connection = connection_module.connect(db_id, cred)
    db_cursor = cursor_module.new_cursor(db_connection)
    return _create_client(db_connection, db_cursor)


def new_test_client(connection: DbConn) -> Client:
    db_connection = connection_module.adapt_connection(connection)
    db_cursor = cursor_module.adapt_cursor(connection.cursor())
    return _create_client(db_connection, db_cursor)
