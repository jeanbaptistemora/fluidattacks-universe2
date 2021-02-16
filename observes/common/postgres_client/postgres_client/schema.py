# Standard libraries
from typing import (
    Callable,
    Iterable, List,
    NamedTuple,
)
# Third party libraries
# Local libraries
from postgres_client.cursor import (
    Cursor,
    CursorAction,
    DynamicSQLargs
)


class Schema(NamedTuple):
    get_tables: Callable[[], Iterable[str]]


def _get_tables(cursor: Cursor, schema: str) -> Iterable[str]:
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


def db_schema(cursor: Cursor, schema: str) -> Schema:

    def get_tables() -> Iterable[str]:
        return _get_tables(cursor, schema)

    return Schema(
        get_tables=get_tables
    )
