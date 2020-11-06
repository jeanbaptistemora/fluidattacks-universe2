# Standard libraries
from typing import (
    Any,
    Callable,
    cast,
    Dict,
    FrozenSet,
    List,
    NamedTuple,
    Set,
)
# Third party libraries
import psycopg2 as postgres
import psycopg2.extensions as postgres_extensions
# Local libraries
from target_redshift_2.utils import log

PGCONN = Any
PGCURR = Any


class CursorAction(NamedTuple):
    cursor: PGCURR
    statement: str
    act: Callable[[], Any]


def make_c_action(cursor: PGCURR, statement: str) -> CursorAction:
    def action() -> Any:
        try:
            cursor.execute(statement)
        except postgres.ProgrammingError as exc:
            log('EXCEPTION', f'{type(exc)} {exc}')
            raise exc
    return CursorAction(
        cursor=cursor,
        statement=statement,
        act=action
    )


class DbClient(NamedTuple):
    connection: PGCONN
    cursor: PGCURR

    def drop_access_point(self: 'DbClient') -> None:
        self.cursor.close()
        self.connection.close()

    def execute(self: 'DbClient', statement: str) -> CursorAction:
        return make_c_action(
            cursor=self.cursor,
            statement=statement
        )


def make_access_point(auth: Dict[str, str]) -> DbClient:
    dbcon: PGCONN = postgres.connect(
        dbname=auth["dbname"],
        user=auth["user"],
        password=auth["password"],
        host=auth["host"],
        port=auth["port"]
    )
    dbcon.set_session(readonly=False)
    dbcon.set_isolation_level(postgres_extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    dbcur: PGCURR = dbcon.cursor()

    return DbClient(connection=dbcon, cursor=dbcur)


class DbSchema(NamedTuple):
    db_client: DbClient
    schema_name: str

    def create_schema(self: 'DbSchema') -> CursorAction:
        statement: str = f"CREATE SCHEMA \"{self.schema_name}\""
        return self.db_client.execute(statement)


class Column(NamedTuple):
    name: str
    field_type: str
    default_val: str = 'NULL'


class DbTable(NamedTuple):
    schema: DbSchema
    table_name: str
    primary_keys: FrozenSet[str]
    columns: FrozenSet[Column]

    def table_path(self: 'DbTable') -> str:
        return f"\"{self.schema.schema_name}\".\"{self.table_name}\""

    def create_table(
        self: 'DbTable', if_not_exist: bool = False
    ) -> CursorAction:
        table_path: str = self.table_path()
        pkeys_fields: str = '' if not self.primary_keys else \
            f',PRIMARY KEY({self.primary_keys})'
        not_exists: str = '' if not if_not_exist else 'IF NOT EXISTS '
        fields: str = ",".join(
            [f"\"{n.name}\" {n.field_type}" for n in self.columns]
        )
        fields_def: str = f'{fields}{pkeys_fields}'
        statement: str = (
            f"CREATE TABLE {not_exists}\"{table_path}\" ({fields_def})"
        )
        return self.schema.db_client.execute(statement)

    def new_columns(
        self: 'DbTable', new_columns: FrozenSet[Column]
    ) -> List[CursorAction]:
        diff_columns: Set[Column] = \
            cast(Set[Column], new_columns) - self.columns
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
            actions.append(self.schema.db_client.execute(statement))
        return actions
