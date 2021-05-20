# Standard libraries
from typing import (
    Callable,
    FrozenSet,
    List,
    NamedTuple,
    Optional,
)

# Third party libraries
from returns.curry import partial

# Local libraries
from postgres_client.client import Client
from postgres_client.cursor import CursorExeAction
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


def table_builder(
    db_client: Client,
    table_draft: TableDraft,
) -> Table:
    def table_path() -> str:
        return f'"{table_draft.id.schema}"."{table_draft.id.table_name}"'

    return Table(
        id=table_draft.id,
        primary_keys=table_draft.primary_keys,
        columns=table_draft.columns,
        table_path=table_path,
        add_columns=partial(
            queries.add_columns,
            db_client.cursor,
            table_draft.id,
            table_draft.columns,
        ),
    )


def exist(db_client: Client, table_id: TableID) -> bool:
    f_action = queries.exist(db_client.cursor, table_id)
    result = tuple(f_action.act())
    return bool(result[0])


def retrieve(db_client: Client, table_id: TableID) -> Optional[Table]:
    actions = queries.retrieve(db_client.cursor, table_id)
    actions[0].act()
    results = actions[1].act()
    columns = set()
    for column in results:
        columns.add(IsolatedColumn(column[1], column[2], column[5]))
    table_draft = TableDraft(
        id=table_id, primary_keys=frozenset(), columns=frozenset(columns)
    )
    return table_builder(db_client, table_draft)


def create(
    db_client: Client, table: Table, if_not_exist: bool = False
) -> Table:
    _table = adapt(table)
    action = queries.create(db_client.cursor, _table, if_not_exist)
    action.act()
    result: Optional[Table] = retrieve(db_client, _table.table_id)
    if result:
        return result
    raise queries.TableCreationFail(
        "Could not create and verify the existence of table: "
        f"{_table.table_id}"
    )


__all__ = [
    "Column",
    "DbTypes",
    "IsolatedColumn",
    "TableID",
]
