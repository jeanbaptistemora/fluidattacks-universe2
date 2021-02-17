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
    return map(lambda item: item[0], cursor.act(actions)[1])


def db_schema(db_client: Client, schema: str) -> Schema:

    def get_tables() -> Iterable[str]:
        return _get_tables(db_client, schema)

    return Schema(
        name=schema,
        get_tables=get_tables
    )
