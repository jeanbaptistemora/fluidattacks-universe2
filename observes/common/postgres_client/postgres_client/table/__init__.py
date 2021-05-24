# pylint: skip-file
# Standard libraries
from __future__ import annotations
from typing import (
    Any,
    Callable,
    FrozenSet,
    List,
    Literal,
    NamedTuple,
)

# Third party libraries
from returns.io import (
    IO,
    IOFailure,
    IOResult,
    IOSuccess,
)
from returns.pipeline import is_successful
from returns.unsafe import unsafe_perform_io

# Local libraries
from postgres_client.client import Client
from postgres_client.cursor import Cursor, CursorExeAction, Query
from postgres_client.table import _queries as queries
from postgres_client.table.common import MetaTable, TableID
from postgres_client.table.common.column import (
    Column,
    DbTypes,
    IsolatedColumn,
    adapt_set,
)


class TableDraft(NamedTuple):
    id: TableID
    primary_keys: FrozenSet[str]
    columns: FrozenSet[IsolatedColumn]


class Table(NamedTuple):
    id: TableID
    primary_keys: FrozenSet[str]
    columns: FrozenSet[IsolatedColumn]
    table_path: Callable[[], str]


def adapt(table: Table) -> MetaTable:
    return MetaTable.new(
        table.id, table.primary_keys, adapt_set(table.columns)
    )


def _adapt_query(cursor: Cursor, query: Query) -> CursorExeAction:
    return cursor.execute(query.query, query.args.value_or(None))


def _adapt_queries(
    cursor: Cursor, queries: List[Query]
) -> List[CursorExeAction]:
    return [_adapt_query(cursor, query) for query in queries]


IOResultBool = IOResult[Literal[True], Literal[False]]


def _exist(cursor: Cursor, table_id: TableID) -> IOResultBool:
    query = queries.exist(table_id)
    cursor.execute_query(query)
    result = cursor.fetch_one()
    success = result.map(lambda r: bool(tuple(r)[0]))
    if success == IO(True):
        return IOSuccess(True)
    return IOFailure(False)


def exist(db_client: Client, table_id: TableID) -> IOResultBool:
    return _exist(db_client.cursor, table_id)


def _retrieve(cursor: Cursor, table_id: TableID) -> IO[MetaTable]:
    query = queries.retrieve(table_id)
    cursor.execute_query(query)
    results = cursor.fetch_all()

    def _extract(raw: Any) -> MetaTable:
        columns = frozenset(
            Column(column[1], DbTypes(column[2].upper()), column[5])
            for column in raw
        )
        return MetaTable.new(table_id, frozenset(), columns)

    return results.map(_extract)


class DbTable(NamedTuple):
    cursor: Cursor
    table: MetaTable
    redshift: bool

    def add_columns(self, columns: FrozenSet[Column]) -> IO[None]:
        _queries = queries.add_columns(self.table, columns)
        self.cursor.execute_queries(_queries)
        return IO(None)

    def rename(self, new_name: str) -> IO[None]:
        self.cursor.execute_query(
            queries.rename(self.table.table_id, new_name)
        )
        return IO(None)

    def delete(self) -> IO[None]:
        self.cursor.execute_query(queries.delete(self.table.table_id))
        return IO(None)

    def move_data(self, target: TableID) -> IO[None]:
        """move data from source into target. target must exist."""
        if self.redshift:
            self.cursor.execute_queries(
                queries.redshift_move(self.table.table_id, target)
            )
        else:
            self.cursor.execute_queries(
                queries.move(self.table.table_id, target)
            )
        return IO(None)

    def move(self, target: TableID) -> IO[None]:
        source = self.table.table_id
        if is_successful(DbTable.exist(self.cursor, target)):
            target_table = DbTable.retrieve(self.cursor, target, self.redshift)
            target_table.map(lambda table: table.delete())
        DbTable.create_like(self.cursor, source, target, self.redshift)
        source_table = DbTable.retrieve(self.cursor, source, self.redshift)
        source_table.map(lambda table: table.move_data(target))
        return IO(None)

    @classmethod
    def exist(cls, cursor: Cursor, table_id: TableID) -> IOResultBool:
        return _exist(cursor, table_id)

    @classmethod
    def retrieve(
        cls, cursor: Cursor, table_id: TableID, redshift_queries: bool = True
    ) -> IO[DbTable]:
        table = unsafe_perform_io(_retrieve(cursor, table_id))
        return IO(cls(cursor=cursor, table=table, redshift=redshift_queries))

    @classmethod
    def new(
        cls,
        cursor: Cursor,
        table: MetaTable,
        if_not_exist: bool = False,
        redshift_queries: bool = True,
    ) -> IO[DbTable]:
        query = queries.create(table, if_not_exist)
        cursor.execute_query(query)
        return cls.retrieve(cursor, table.table_id, redshift_queries)

    @classmethod
    def create_like(
        cls,
        cursor: Cursor,
        blueprint: TableID,
        new_table: TableID,
        redshift_queries: bool = True,
    ) -> IO[DbTable]:
        query = queries.create_like(blueprint, new_table)
        cursor.execute_query(query)
        return cls.retrieve(cursor, new_table, redshift_queries)


__all__ = [
    "Column",
    "DbTypes",
    "IsolatedColumn",
    "TableID",
]
