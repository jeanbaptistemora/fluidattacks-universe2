# Standard libraries
from enum import Enum
from typing import (
    Any,
    Callable, Optional,
    cast,
    FrozenSet,
    List,
    NamedTuple,
    Set,
)
# Third party libraries
# Local libraries

PGCONN = Any
PGCURR = Any


# Supported JSON Schema types
class DbTypes(Enum):
    BOOLEAN = 'BOOLEAN'
    NUMERIC = 'NUMERIC(38)'
    FLOAT = 'FLOAT8'
    VARCHAR = 'VARCHAR'
    TIMESTAMP = 'TIMESTAMP'


class ConnectionID(NamedTuple):
    dbname: str
    user: str
    password: str
    host: str
    port: str

    def __repr__(self):
        return "ConnectionID(dbname={}, ****)".format(self.dbname)


class SchemaID(NamedTuple):
    connection: Optional[ConnectionID]
    schema_name: str


class TableID(NamedTuple):
    schema: SchemaID
    table_name: str


class IsolatedColumn(NamedTuple):
    name: str
    field_type: str
    default_val: Optional[str] = None


class Column(NamedTuple):
    table: 'TableID'
    column: IsolatedColumn


class CursorAction(NamedTuple):
    cursor: PGCURR
    statement: str
    act: Callable[[], Any]


class Client(NamedTuple):
    make_action: Callable[[PGCURR, str], CursorAction]
    connection: PGCONN
    cursor: PGCURR

    def drop_access_point(self: 'Client') -> None:
        self.cursor.close()
        self.connection.close()

    def execute(self: 'Client', statement: str) -> CursorAction:
        return self.make_action(
            self.cursor,
            statement
        )


class Schema(NamedTuple):
    id: SchemaID


class Table(NamedTuple):
    id: TableID
    primary_keys: FrozenSet[str]
    columns: FrozenSet[IsolatedColumn]
    db_client: Client

    def table_path(self: 'Table') -> str:
        return f"\"{self.id.schema.schema_name}\".\"{self.id.table_name}\""

    def add_columns(
        self: 'Table', new_columns: FrozenSet[IsolatedColumn]
    ) -> List[CursorAction]:
        diff_columns: Set[IsolatedColumn] = \
            cast(Set[IsolatedColumn], new_columns) - self.columns
        diff_names: Set[str] = set(map(lambda c: c.name, diff_columns))
        current_names: Set[str] = set(map(lambda c: c.name, self.columns))
        if not diff_names.isdisjoint(current_names):
            raise Exception(
                'Cannot update the type of existing columns.'
                f'Columns: {diff_names.intersection(current_names)}'
            )
        actions: List[CursorAction] = []
        table_path: str = self.table_path()
        for column in diff_columns:
            statement: str = (
                f'ALTER TABLE {table_path} '
                f'ADD COLUMN {column.name} '
                f'{column.field_type} default {column.default_val}'
            )
            actions.append(self.db_client.execute(statement))
        return actions
