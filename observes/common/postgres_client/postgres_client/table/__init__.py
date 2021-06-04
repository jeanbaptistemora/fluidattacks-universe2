# pylint: skip-file

from __future__ import (
    annotations,
)

from deprecated import (
    deprecated,
)
from postgres_client.client import (
    Client,
)
from postgres_client.cursor import (
    Cursor,
)
from postgres_client.data_type import (
    to_rs_datatype,
)
from postgres_client.table import (
    _queries as queries,
)
from postgres_client.table._objs import (
    Column,
    MetaTable,
    TableID,
)
from returns.io import (
    IO,
    IOFailure,
    IOResult,
    IOSuccess,
)
from returns.pipeline import (
    is_successful,
)
from returns.primitives.types import (
    Immutable,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from typing import (
    Any,
    FrozenSet,
    Literal,
    NamedTuple,
)

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
            Column(column[1], to_rs_datatype(column[2].upper()), column[5])
            for column in raw
        )
        return MetaTable.new(table_id, frozenset(), columns)

    return results.map(_extract)


class _DbTable(NamedTuple):
    cursor: Cursor
    table: MetaTable
    redshift: bool


class DbTable(Immutable):
    """Use TableFactory for building a DbTable element"""

    cursor: Cursor
    table: MetaTable
    redshift: bool

    def __new__(cls, obj: _DbTable) -> DbTable:
        self = object.__new__(cls)
        for prop, val in obj._asdict().items():
            object.__setattr__(self, prop, val)
        return self

    def __str__(self) -> str:
        return "Table(data={}, redshift={})".format(self.table, self.redshift)

    def add_columns(self, columns: FrozenSet[Column]) -> IO[None]:
        _queries = queries.add_columns(self.table, columns)
        self.cursor.execute_queries(_queries)
        return IO(None)

    def rename(self, new_name: str) -> IO[TableID]:
        self.cursor.execute_query(
            queries.rename(self.table.table_id, new_name)
        )
        return IO(TableID(self.table.table_id.schema, new_name))

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
    @deprecated(reason="use factory")
    def exist(cls, cursor: Cursor, table_id: TableID) -> IOResultBool:
        return _exist(cursor, table_id)

    @classmethod
    @deprecated(reason="use factory")
    def retrieve(
        cls, cursor: Cursor, table_id: TableID, redshift_queries: bool = True
    ) -> IO[DbTable]:
        table = unsafe_perform_io(_retrieve(cursor, table_id))
        draft = _DbTable(cursor=cursor, table=table, redshift=redshift_queries)
        return IO(cls(draft))

    @classmethod
    @deprecated(reason="use factory")
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


class _TableFactory(NamedTuple):
    cursor: Cursor
    redshift_queries: bool


class TableFactory(Immutable):
    cursor: Cursor
    redshift_queries: bool

    def __new__(
        cls, cursor: Cursor, redshift_queries: bool = True
    ) -> TableFactory:
        self = object.__new__(cls)
        obj = _TableFactory(cursor, redshift_queries)
        for prop, val in obj._asdict().items():
            object.__setattr__(self, prop, val)
        return self

    def exist(self, table_id: TableID) -> IOResultBool:
        return _exist(self.cursor, table_id)

    def retrieve(self, table_id: TableID) -> IO[DbTable]:
        table = unsafe_perform_io(_retrieve(self.cursor, table_id))
        draft = _DbTable(
            cursor=self.cursor, table=table, redshift=self.redshift_queries
        )
        return IO(DbTable(draft))

    def new_table(
        self,
        table: MetaTable,
        if_not_exist: bool = False,
    ) -> IO[DbTable]:
        query = queries.create(table, if_not_exist)
        self.cursor.execute_query(query)
        return self.retrieve(table.table_id)

    def create_like(
        self,
        blueprint: TableID,
        new_table: TableID,
    ) -> IO[DbTable]:
        query = queries.create_like(blueprint, new_table)
        self.cursor.execute_query(query)
        return self.retrieve(new_table)


__all__ = [
    "Column",
    "MetaTable",
    "TableID",
]
