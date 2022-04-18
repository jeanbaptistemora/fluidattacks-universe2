# pylint: skip-file

from __future__ import (
    annotations,
)

from postgres_client.column import (
    Column,
    ColumnType,
    DEFAULT_PRECISION,
    DEFAULT_SCALE,
    to_rs_datatype,
)
from postgres_client.cursor import (
    Cursor,
)
from postgres_client.ids import (
    TableID,
)
from postgres_client.table import (
    _queries as queries,
)
from postgres_client.table._objs import (
    MetaTable,
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
    Iterator,
    Literal,
    NamedTuple,
    Tuple,
)

IOResultBool = IOResult[Literal[True], Literal[False]]


def _exist(cursor: Cursor, table_id: TableID) -> IOResultBool:  # type: ignore
    query = queries.exist(table_id)
    cursor.execute_query(query)
    result = cursor.fetch_one()
    success = result.map(lambda r: bool(tuple(r)[0]))
    if success == IO(True):
        return IOSuccess(True)
    return IOFailure(False)


def _raw_to_coulmn(raw: Tuple[Any, ...]) -> Column:
    data_type = to_rs_datatype(str(raw[2]).upper())
    requires_precision = data_type in DEFAULT_PRECISION
    requires_scale = data_type in DEFAULT_SCALE
    return Column(
        raw[1],
        ColumnType(
            data_type,
            precision=int(raw[3]) if raw[3] and requires_precision else None,
            scale=int(raw[4]) if raw[4] and requires_scale else None,
            default_val=str(raw[5]) if raw[5] else None,
            nullable=str(raw[6]).upper() == "YES",
        ),
    )


def _retrieve(cursor: Cursor, table_id: TableID) -> IO[MetaTable]:
    query = queries.retrieve(table_id)
    cursor.execute_query(query)
    results = cursor.fetch_all()

    def _extract(raw: Iterator[Tuple[Any, ...]]) -> MetaTable:
        columns = frozenset(_raw_to_coulmn(column) for column in raw)
        return MetaTable.new(table_id, frozenset(), columns)

    return results.map(_extract)


class _Table(NamedTuple):
    cursor: Cursor
    table: MetaTable
    redshift: bool


class Table(Immutable):
    """Use TableFactory for building a Table element"""

    cursor: Cursor
    table: MetaTable
    redshift: bool

    def __new__(cls, obj: _Table) -> Table:
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

    def exist(self, table_id: TableID) -> IOResultBool:  # type: ignore
        return _exist(self.cursor, table_id)

    def retrieve(self, table_id: TableID) -> IO[Table]:
        table = unsafe_perform_io(_retrieve(self.cursor, table_id))
        draft = _Table(
            cursor=self.cursor, table=table, redshift=self.redshift_queries
        )
        return IO(Table(draft))

    def new_table(
        self,
        table: MetaTable,
        if_not_exist: bool = False,
    ) -> IO[Table]:
        query = queries.create(table, if_not_exist)
        self.cursor.execute_query(query)
        return self.retrieve(table.table_id)

    def create_like(
        self,
        blueprint: TableID,
        new_table: TableID,
    ) -> IO[Table]:
        query = queries.create_like(blueprint, new_table)
        self.cursor.execute_query(query)
        return self.retrieve(new_table)

    def move(self, source: TableID, target: TableID) -> IO[None]:
        if is_successful(self.exist(target)):
            target_table = self.retrieve(target)
            target_table.map(lambda table: table.delete())
        self.create_like(source, target)
        source_table = self.retrieve(source)
        source_table.map(lambda table: table.move_data(target))
        return IO(None)


__all__ = [
    "Column",
    "MetaTable",
    "TableID",
]
