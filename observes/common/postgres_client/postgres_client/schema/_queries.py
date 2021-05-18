# Standard libraries
from typing import (
    List,
)

# Third party libraries
# Local libraries
from postgres_client.cursor import (
    Cursor,
    CursorAction,
    DynamicSQLargs,
)


def get_tables(cursor: Cursor, schema: str) -> List[CursorAction]:
    statement: str = (
        "SELECT tables.table_name FROM information_schema.tables "
        "WHERE table_schema = %(schema_name)s"
    )
    args = DynamicSQLargs(values={"schema_name": schema})
    actions: List[CursorAction] = [
        cursor.execute(statement, args),
        cursor.fetchall(),
    ]
    return actions


def exist_on_db(cursor: Cursor, schema: str) -> List[CursorAction]:
    statement: str = (
        "SELECT EXISTS("
        "SELECT 1 FROM pg_namespace "
        "WHERE nspname = %(schema_name)s);"
    )
    args = DynamicSQLargs(values={"schema_name": schema})
    actions: List[CursorAction] = [
        cursor.execute(statement, args),
        cursor.fetchone(),
    ]
    return actions


def delete_on_db(cursor: Cursor, schema: str) -> CursorAction:
    statement: str = "DROP SCHEMA {schema_name}"
    args = DynamicSQLargs(identifiers={"schema_name": schema})
    return cursor.execute(statement, args)
