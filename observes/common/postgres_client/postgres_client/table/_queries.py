# Standard libraries
from typing import (
    FrozenSet,
    List,
)

# Local libraries
from postgres_client.cursor import Cursor, CursorExeAction, DynamicSQLargs
from postgres_client.table.common import TableID
from postgres_client.table.common.column import IsolatedColumn


class MutateColumnException(Exception):
    pass


def add_columns(
    cursor: Cursor,
    table_id: TableID,
    old_columns: FrozenSet[IsolatedColumn],
    new_columns: FrozenSet[IsolatedColumn],
) -> List[CursorExeAction]:
    diff_columns: FrozenSet[IsolatedColumn] = new_columns - old_columns
    diff_names: FrozenSet[str] = frozenset(col.name for col in diff_columns)
    current_names: FrozenSet[str] = frozenset(col.name for col in old_columns)
    if not diff_names.isdisjoint(current_names):
        raise MutateColumnException(
            "Cannot update the type of existing columns."
            f"Columns: {diff_names.intersection(current_names)}"
        )
    actions: List[CursorExeAction] = []
    table_path: str = f'"{table_id.schema}"."{table_id.table_name}"'
    for column in diff_columns:
        statement: str = (
            "ALTER TABLE {table_path} "
            "ADD COLUMN {column_name} "
            "{field_type} default %(default_val)s"
        )
        action = cursor.execute(
            statement,
            DynamicSQLargs(
                values={"default_val": column.default_val},
                identifiers={
                    "table_path": table_path,
                    "column_name": column.name,
                    "field_type": column.field_type,
                },
            ),
        )
        actions.append(action)
    return actions
