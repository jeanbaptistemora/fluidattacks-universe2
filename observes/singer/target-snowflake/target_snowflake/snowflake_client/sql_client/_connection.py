# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from ._cursor import (
    Cursor,
)
from ._identifier import (
    Identifier,
)
from ._inner import (
    RawCursor,
)
from dataclasses import (
    dataclass,
)
from fa_purity.cmd import (
    Cmd,
)
from logging import (
    Logger,
)
from snowflake.connector import (
    connect as snowflake_connect,
    SnowflakeConnection,
)
from typing import (
    cast,
    Optional,
)


@dataclass(frozen=True)
class DatabaseId:
    db_name: Identifier
    host: Optional[str]
    port: Optional[int]


@dataclass(frozen=True)
class Credentials:
    user: str
    password: str
    account: str

    def __repr__(self) -> str:
        return "[MASKED]"

    def __str__(self) -> str:
        return "[MASKED]"


@dataclass(frozen=True)
class _DbConnection:
    _connection: SnowflakeConnection


@dataclass(frozen=True)
class DbConnection:
    _inner: _DbConnection

    def close(self) -> Cmd[None]:
        return Cmd.from_cmd(lambda: cast(None, self._inner._connection.close())).map(lambda _: None)  # type: ignore[no-untyped-call]

    def commit(self) -> Cmd[None]:
        return Cmd.from_cmd(lambda: cast(None, self._inner._connection.commit())).map(lambda _: None)  # type: ignore[no-untyped-call]

    def cursor(self, log: Logger) -> Cmd[Cursor]:
        def _action() -> Cursor:
            return Cursor(log, RawCursor(self._inner._connection.cursor()))

        return Cmd.from_cmd(_action)


@dataclass(frozen=True)
class DbConnector:
    _creds: Credentials

    def connect_db(self, database: DatabaseId) -> Cmd[DbConnection]:
        def _action() -> DbConnection:
            connection = snowflake_connect(
                user=self._creds.user,
                password=self._creds.password,
                account=self._creds.account,
                database=database.db_name.sql_identifier,
            )
            draft = _DbConnection(connection)
            return DbConnection(draft)

        return Cmd.from_cmd(_action)
