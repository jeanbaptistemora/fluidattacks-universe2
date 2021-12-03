from __future__ import (
    annotations,
)

import json
from postgres_client.client import (
    Client,
)
from postgres_client.client._client import (
    _Client,
)
from postgres_client.connection import (
    connect,
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
    Tuple,
)


def _extract_conf_info(
    auth_file: IO[str],
) -> Tuple[DatabaseID, Credentials]:
    auth = json.load(auth_file)
    auth["db_name"] = auth["dbname"]
    db_id_raw = dict(
        filter(lambda x: x[0] in DatabaseID.__annotations__, auth.items())
    )
    creds_raw = dict(
        filter(lambda x: x[0] in Credentials.__annotations__, auth.items())
    )
    return (DatabaseID(**db_id_raw), Credentials(**creds_raw))


class ClientFactory(Immutable):
    def __new__(cls) -> ClientFactory:
        self = object.__new__(cls)
        return self

    # pylint: disable=no-self-use
    def from_creds(self, db_id: DatabaseID, cred: Credentials) -> Client:
        db_connection = connect(db_id, cred)
        db_cursor = Cursor.new(db_connection)
        draft = _Client(db_cursor, db_connection)
        return Client(draft)

    def from_conf(self, auth_file: IO[str]) -> Client:
        return self.from_creds(*_extract_conf_info(auth_file))

    # pylint: disable=no-self-use
    def test_client(self, connection: DbConn) -> Client:
        db_connection = DbConnection.from_raw(connection)
        db_cursor = Cursor.from_raw(connection.cursor())
        draft = _Client(db_cursor, db_connection)
        return Client(draft)
