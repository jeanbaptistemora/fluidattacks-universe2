# pylint: skip-file

from __future__ import (
    annotations,
)

import logging
from postgres_client.connection import (
    DbConnection,
)
from postgres_client.query import (
    Query,
)
from returns.io import (
    impure,
    IO,
)
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    NamedTuple,
    Optional,
    Tuple,
)

DbCursor = Any
LOG = logging.getLogger(__name__)


class Cursor(NamedTuple):
    db_cursor: DbCursor

    @impure
    def close(self) -> None:
        return self.db_cursor.close()

    def execute_query(self, query: Query) -> IO[None]:
        stm_values: Dict[str, Optional[str]] = query.args.map(
            lambda args: args.values
        ).value_or({})
        try:
            LOG.debug(
                "Executing: %s",
                self.db_cursor.mogrify(query.query, stm_values),
            )
        except TypeError:
            LOG.error("raw: %s\nvals: %s", query.query, stm_values)
        self.db_cursor.execute(query.query, stm_values)
        return IO(None)

    def execute_queries(self, queries: List[Query]) -> IO[None]:
        for query in queries:
            self.execute_query(query)
        return IO(None)

    def fetch_all(self) -> IO[Iterator[Tuple[Any, ...]]]:
        return IO(self.db_cursor.fetchall())

    def fetch_many(self, limit: int) -> IO[Tuple[Tuple[Any, ...]]]:
        return IO(tuple(self.db_cursor.fetchmany(limit)))

    def fetch_one(self) -> IO[Tuple[Any, ...]]:
        return IO(self.db_cursor.fetchone())

    @classmethod
    def new(cls, connection: DbConnection) -> Cursor:
        db_cursor = connection.get_cursor()
        return cls(db_cursor)

    @classmethod
    def from_raw(cls, db_cursor: DbCursor) -> Cursor:
        return cls(db_cursor)
