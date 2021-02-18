# Standard libraries
from typing import (
    Iterable,
    List,
)
# Third party libraries
# Local libraries
from postgres_client.client import Client
from postgres_client.cursor import (
    CursorAction,
    DynamicSQLargs
)
from postgres_client.schema import Schema


def _get_tables(db_client: Client, schema: str) -> Iterable[str]:
    cursor = db_client.cursor
    statement: str = (
        'SELECT tables.table_name FROM information_schema.tables '
        'WHERE table_schema = %(schema_name)s'
    )
    args = DynamicSQLargs(
        values={'schema_name': schema}
    )
    actions: List[CursorAction] = [
        cursor.execute(statement, args),
        cursor.fetchall()
    ]
    return list(map(lambda item: item[0], cursor.act(actions)[1]))


def _exist_on_db(db_client: Client, schema: str) -> bool:
    cursor = db_client.cursor
    statement: str = (
        'SELECT EXISTS('
        'SELECT 1 FROM pg_namespace '
        'WHERE nspname = %(schema_name)s);'
    )
    args = DynamicSQLargs(
        values={'schema_name': schema}
    )
    actions: List[CursorAction] = [
        cursor.execute(statement, args),
        cursor.fetchone()
    ]
    return cursor.act(actions)[1][0]


def _delete_on_db(db_client: Client, schema: str) -> None:
    cursor = db_client.cursor
    statement: str = (
        'DROP SCHEMA {schema_name}'
    )
    args = DynamicSQLargs(
        identifiers={'schema_name': schema}
    )
    cursor.execute(statement, args).act()


def db_schema(db_client: Client, schema: str) -> Schema:

    def get_tables() -> Iterable[str]:
        return _get_tables(db_client, schema)

    def exist_on_db() -> bool:
        return _exist_on_db(db_client, schema)

    def delete_on_db() -> None:
        return _delete_on_db(db_client, schema)

    return Schema(
        name=schema,
        delete_on_db=delete_on_db,
        exist_on_db=exist_on_db,
        get_tables=get_tables,
    )
