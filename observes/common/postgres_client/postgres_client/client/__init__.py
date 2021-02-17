# Standard libraries
import json
from typing import (
    Callable,
    IO,
    NamedTuple,
    Tuple,
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


def _extract_conf_info(
    auth_file: IO[str]
) -> Tuple[DatabaseID, Credentials]:
    auth = json.load(auth_file)
    auth['db_name'] = auth['dbname']
    db_id_raw = dict(
        filter(lambda x: x[0] in DatabaseID._fields, auth.items())
    )
    creds_raw = dict(
        filter(lambda x: x[0] in Credentials._fields, auth.items())
    )
    return (DatabaseID(**db_id_raw), Credentials(**creds_raw))


def new_client(
    db_id: DatabaseID,
    cred: Credentials
) -> Client:
    db_connection = connection_module.connect(db_id, cred)
    db_cursor = cursor_module.new_cursor(db_connection)
    return _create_client(db_connection, db_cursor)


def new_client_from_conf(auth_file: IO[str]) -> Client:
    return new_client(*_extract_conf_info(auth_file))


def new_test_client(connection: DbConn) -> Client:
    db_connection = connection_module.adapt_connection(connection)
    db_cursor = cursor_module.adapt_cursor(connection.cursor())
    return _create_client(db_connection, db_cursor)
