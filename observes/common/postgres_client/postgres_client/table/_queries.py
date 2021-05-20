# Standard libraries
from typing import (
    Dict,
    FrozenSet,
    List,
    Optional,
    Tuple,
)

# Local libraries
from postgres_client.cursor import (
    Cursor,
    CursorExeAction,
    CursorFetchAction,
    DynamicSQLargs,
)
from postgres_client.table.common import MetaTable, TableID
from postgres_client.table.common.column import IsolatedColumn


class MutateColumnException(Exception):
    pass


class TableCreationFail(Exception):
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


def exist(cursor: Cursor, table_id: TableID) -> CursorFetchAction:
    """Check existence of a Table on the DB"""
    statement = """
        SELECT EXISTS (
            SELECT * FROM information_schema.tables
            WHERE table_schema = %(table_schema)s
            AND table_name = %(table_name)s
        );
    """
    action = cursor.execute(
        statement,
        DynamicSQLargs(
            values={
                "table_schema": table_id.schema,
                "table_name": table_id.table_name,
            }
        ),
    )
    action.act()
    return cursor.fetchone()


def retrieve(
    cursor: Cursor, table_id: TableID
) -> Tuple[CursorExeAction, CursorFetchAction]:
    """Retrieve Table from DB"""
    statement = """
        SELECT ordinal_position AS position,
            column_name,
            data_type,
            CASE WHEN character_maximum_length IS not null
                    THEN character_maximum_length
                    ELSE numeric_precision end AS max_length,
            is_nullable,
            column_default AS default_value
        FROM information_schema.columns
        WHERE table_name = %(table_name)s
            AND table_schema = %(table_schema)s
        ORDER BY ordinal_position;
    """
    action: CursorExeAction = cursor.execute(
        statement,
        DynamicSQLargs(
            values={
                "table_schema": table_id.schema,
                "table_name": table_id.table_name,
            }
        ),
    )
    fetch_action = cursor.fetchall()
    return (action, fetch_action)


def create(
    cursor: Cursor, table: MetaTable, if_not_exist: bool = False
) -> CursorExeAction:
    table_path: str = table.path
    pkeys_fields: str = ""
    if table.primary_keys:
        p_fields: str = ",".join(
            [f"{{pkey_{n}}}" for n in range(len(table.primary_keys))]
        )
        pkeys_fields = f",PRIMARY KEY({p_fields})"
    not_exists: str = "" if not if_not_exist else "IF NOT EXISTS "
    fields: str = ",".join(
        [f"{{name_{n}}} {{field_type_{n}}}" for n in range(len(table.columns))]
    )
    fields_def: str = f"{fields}{pkeys_fields}"
    statement: str = f"CREATE TABLE {not_exists}{{table_path}} ({fields_def})"
    identifiers: Dict[str, Optional[str]] = {"table_path": table_path}
    for index, value in enumerate(table.primary_keys):
        identifiers[f"pkey_{index}"] = value
    for index, column in enumerate(table.columns):
        identifiers[f"name_{index}"] = column.name
        identifiers[f"field_type_{index}"] = column.field_type.value

    action = cursor.execute(statement, DynamicSQLargs(identifiers=identifiers))
    return action
