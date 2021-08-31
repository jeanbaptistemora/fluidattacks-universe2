from __future__ import (
    annotations,
)

from deprecated import (  # type: ignore
    deprecated,
)
import psycopg2 as postgres
import psycopg2.extensions as postgres_extensions
from typing import (
    Any,
    NamedTuple,
    Optional,
)


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
    isolation_lvl: Optional[
        int
    ] = postgres_extensions.ISOLATION_LEVEL_AUTOCOMMIT


DbConn = Any


class DbConnection(NamedTuple):
    raw_connection: DbConn
    options: Options

    def close(self) -> None:
        return self.raw_connection.close()

    def commit(self) -> None:
        return self.raw_connection.commit()

    def get_cursor(self) -> Any:
        return self.raw_connection.cursor()

    @classmethod
    def from_raw(
        cls, connection: DbConn, options: Options = Options()
    ) -> DbConnection:
        connection.set_session(readonly=False)
        connection.set_isolation_level(options.isolation_lvl)
        return cls(
            raw_connection=connection,
            options=options,
        )

    @classmethod
    def new(
        cls,
        db_id: DatabaseID,
        creds: Credentials,
        options: Options = Options(),
    ) -> DbConnection:
        dbcon = postgres.connect(
            dbname=db_id.db_name,
            user=creds.user,
            password=creds.password,
            host=db_id.host,
            port=db_id.port,
        )
        return cls.from_raw(dbcon, options)


@deprecated
def adapt_connection(
    connection: DbConn, options: Options = Options()
) -> DbConnection:
    return DbConnection.from_raw(connection, options)


@deprecated
def connect(
    db_id: DatabaseID, creds: Credentials, options: Options = Options()
) -> DbConnection:
    return DbConnection.new(db_id, creds, options)
