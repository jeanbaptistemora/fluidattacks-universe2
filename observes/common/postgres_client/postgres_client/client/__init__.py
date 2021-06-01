from __future__ import (
    annotations,
)

import json
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
from typing import (
    IO,
    NamedTuple,
    Tuple,
)


def _extract_conf_info(auth_file: IO[str]) -> Tuple[DatabaseID, Credentials]:
    auth = json.load(auth_file)
    auth["db_name"] = auth["dbname"]
    db_id_raw = dict(
        filter(lambda x: x[0] in DatabaseID._fields, auth.items())
    )
    creds_raw = dict(
        filter(lambda x: x[0] in Credentials._fields, auth.items())
    )
    return (DatabaseID(**db_id_raw), Credentials(**creds_raw))


class Client(NamedTuple):
    cursor: Cursor
    connection: DbConnection

    def close(self) -> None:
        self.cursor.close()
        self.connection.close()

    @classmethod
    def new(
        cls,
        db_connection: DbConnection,
        db_cursor: Cursor,
    ) -> Client:
        return cls(
            cursor=db_cursor,
            connection=db_connection,
        )

    @classmethod
    def from_creds(cls, db_id: DatabaseID, cred: Credentials) -> Client:
        db_connection = connection_module.connect(db_id, cred)
        db_cursor = cursor_module.new_cursor(db_connection)
        return cls.new(db_connection, db_cursor)

    @classmethod
    def from_conf(cls, auth_file: IO[str]) -> Client:
        return cls.from_creds(*_extract_conf_info(auth_file))

    @classmethod
    def test_client(cls, connection: DbConn) -> Client:
        db_connection = DbConnection.from_raw(connection)
        db_cursor = cursor_module.adapt_cursor(connection.cursor())
        return cls.new(db_connection, db_cursor)


# old interface support
def new_client(db_id: DatabaseID, cred: Credentials) -> Client:
    return Client.from_creds(db_id, cred)


def new_client_from_conf(auth_file: IO[str]) -> Client:
    return Client.from_conf(auth_file)


def new_test_client(connection: DbConn) -> Client:
    return Client.test_client(connection)


# -- old interface support
