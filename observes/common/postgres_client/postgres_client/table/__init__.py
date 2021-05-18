# Standard libraries
from typing import (
    Callable,
    Dict,
    FrozenSet,
    List,
    NamedTuple,
    Optional,
)

# Third party libraries
from returns.curry import partial

# Local libraries
from postgres_client.client import Client
from postgres_client.cursor import CursorExeAction, DynamicSQLargs
from postgres_client.table import _queries as queries
from postgres_client.table.common import TableID
from postgres_client.table.common.column import (
    Column,
    DbTypes,
    IsolatedColumn,
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
    db_client: Client, table_draft: Table, if_not_exist: bool = False
) -> Table:
    """Creates a Table in the DB and returns it"""
    table_path: str = table_draft.table_path()
    pkeys_fields: str = ""
    if table_draft.primary_keys:
        p_fields: str = ",".join(
            [f"{{pkey_{n}}}" for n in range(len(table_draft.primary_keys))]
        )
        pkeys_fields = f",PRIMARY KEY({p_fields})"
    not_exists: str = "" if not if_not_exist else "IF NOT EXISTS "
    fields: str = ",".join(
        [
            f"{{name_{n}}} {{field_type_{n}}}"
            for n in range(len(table_draft.columns))
        ]
    )
    fields_def: str = f"{fields}{pkeys_fields}"
    statement: str = f"CREATE TABLE {not_exists}{{table_path}} ({fields_def})"
    identifiers: Dict[str, Optional[str]] = {"table_path": table_path}
    for index, value in enumerate(table_draft.primary_keys):
        identifiers[f"pkey_{index}"] = value
    for index, column in enumerate(table_draft.columns):
        identifiers[f"name_{index}"] = column.name
        identifiers[f"field_type_{index}"] = column.field_type

    db_client.cursor.execute(
        statement, DynamicSQLargs(identifiers=identifiers)
    )
    result: Optional[Table] = retrieve(db_client, table_draft.id)
    if result:
        return result
    raise queries.TableCreationFail(
        "Could not create and verify the existence of table: "
        f"{table_draft.id}"
    )


__all__ = [
    "Column",
    "DbTypes",
    "IsolatedColumn",
    "TableID",
]
