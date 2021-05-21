# pylint: skip-file
# Standard libraries
from typing import (
    Any,
    Callable,
    FrozenSet,
    List,
    Literal,
    NamedTuple,
    Optional,
)

# Third party libraries
from returns.io import (
    IO,
    IOFailure,
    IOResult,
    IOSuccess,
)

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
    add_columns: Callable[[FrozenSet[IsolatedColumn]], List[CursorExeAction]]


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


def table_builder(
    db_client: Client,
    table_draft: TableDraft,
) -> Table:
    def table_path() -> str:
        return f'"{table_draft.id.schema}"."{table_draft.id.table_name}"'

    def _add_columns(
        columns: FrozenSet[IsolatedColumn],
    ) -> List[CursorExeAction]:
        return _adapt_queries(
            db_client.cursor,
            queries.add_columns(table_draft.id, table_draft.columns, columns),
        )

    return Table(
        id=table_draft.id,
        primary_keys=table_draft.primary_keys,
        columns=table_draft.columns,
        table_path=table_path,
        add_columns=_add_columns,
    )


def exist(
    db_client: Client, table_id: TableID
) -> IOResult[Literal[True], Literal[False]]:
    cursor = db_client.cursor
    query = queries.exist(table_id)
    cursor.execute_query(query)
    result = cursor.fetch_one()
    success = result.map(lambda r: bool(tuple(r)[0]))
    if success == IO(True):
        return IOSuccess(True)
    return IOFailure(False)


def retrieve(db_client: Client, table_id: TableID) -> IO[Optional[Table]]:
    cursor = db_client.cursor
    query = queries.retrieve(table_id)
    cursor.execute_query(query)
    results = cursor.fetch_all()

    def _extract(raw: Any) -> Optional[Table]:
        columns = set()
        for column in raw:
            columns.add(IsolatedColumn(column[1], column[2], column[5]))
        table_draft = TableDraft(
            id=table_id, primary_keys=frozenset(), columns=frozenset(columns)
        )
        return table_builder(db_client, table_draft)

    return results.map(_extract)


def create(
    db_client: Client, table: Table, if_not_exist: bool = False
) -> IO[Table]:
    cursor = db_client.cursor
    _table = adapt(table)
    query = queries.create(_table, if_not_exist)
    cursor.execute_query(query)
    result = retrieve(db_client, _table.table_id)

    def _to_table(table: Optional[Table]) -> Table:
        if table:
            return table
        raise queries.TableCreationFail(
            "Could not create and verify the existence of table: "
            f"{_table.table_id}"
        )

    return result.map(_to_table)


__all__ = [
    "Column",
    "DbTypes",
    "IsolatedColumn",
    "TableID",
]
