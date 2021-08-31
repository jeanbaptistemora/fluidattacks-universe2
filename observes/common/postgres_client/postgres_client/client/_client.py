from __future__ import (
    annotations,
)

from deprecated import (  # type: ignore
    deprecated,
)
import json
from postgres_client import (
    connection as connection_module,
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
from returns.primitives.types import (
    Immutable,
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


class _Client(NamedTuple):
    cursor: Cursor
    connection: DbConnection


class Client(Immutable):
    cursor: Cursor
    connection: DbConnection

    def close(self) -> None:
        self.cursor.close()
        self.connection.close()

    def __new__(cls, obj: _Client) -> Client:
        self = object.__new__(cls)
        for prop, val in obj._asdict().items():
            object.__setattr__(self, prop, val)
        return self

    @classmethod
    @deprecated
    def new(
        cls,
        db_connection: DbConnection,
        db_cursor: Cursor,
    ) -> Client:
        return cls(
            _Client(
                cursor=db_cursor,
                connection=db_connection,
            )
        )

    @classmethod
    @deprecated
    def from_creds(cls, db_id: DatabaseID, cred: Credentials) -> Client:
        db_connection = connection_module.connect(db_id, cred)
        db_cursor = Cursor.new(db_connection)
        return cls.new(db_connection, db_cursor)

    @classmethod
    @deprecated
    def from_conf(cls, auth_file: IO[str]) -> Client:
        return cls.from_creds(*_extract_conf_info(auth_file))

    @classmethod
    @deprecated
    def test_client(cls, connection: DbConn) -> Client:
        db_connection = DbConnection.from_raw(connection)
        db_cursor = Cursor.from_raw(connection.cursor())
        return cls.new(db_connection, db_cursor)


@deprecated
def new_client(db_id: DatabaseID, cred: Credentials) -> Client:
    return Client.from_creds(db_id, cred)


@deprecated
def new_client_from_conf(auth_file: IO[str]) -> Client:
    return Client.from_conf(auth_file)


@deprecated
def new_test_client(connection: DbConn) -> Client:
    return Client.test_client(connection)
