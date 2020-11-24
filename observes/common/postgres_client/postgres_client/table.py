from enum import Enum
from typing import (
    Callable,
    Dict,
    FrozenSet,
    List,
    NamedTuple,
    Optional,
)
from postgres_client.client import Client
from postgres_client.cursor import CursorExeAction, DynamicSQLargs


# Supported JSON Schema types
class DbTypes(Enum):
    BOOLEAN = 'BOOLEAN'
    NUMERIC = 'NUMERIC(38)'
    FLOAT = 'FLOAT8'
    VARCHAR = 'VARCHAR'
    TIMESTAMP = 'TIMESTAMP'


class IsolatedColumn(NamedTuple):
    name: str
    field_type: str
    default_val: Optional[str] = None


class Column(NamedTuple):
    table: 'TableID'
    column: IsolatedColumn


class TableID(NamedTuple):
    schema: str
    table_name: str


class TableDraft(NamedTuple):
    id: TableID
    primary_keys: FrozenSet[str]
    columns: FrozenSet[IsolatedColumn]


class Table(NamedTuple):
    id: TableID
    primary_keys: FrozenSet[str]
    columns: FrozenSet[IsolatedColumn]
    table_path: Callable[[], str]
    add_columns: Callable[
        [FrozenSet[IsolatedColumn]], List[CursorExeAction]
    ]


class MutateColumnException(Exception):
    pass


class TableCreationFail(Exception):
    pass


def table_builder(
    db_client: Client,
    table_draft: TableDraft,
) -> Table:

    def table_path() -> str:
        return f"\"{table_draft.id.schema}\".\"{table_draft.id.table_name}\""

    def add_columns(
        new_columns: FrozenSet[IsolatedColumn]
    ) -> List[CursorExeAction]:
        diff_columns: FrozenSet[IsolatedColumn] = \
            new_columns - table_draft.columns
        diff_names: FrozenSet[str] = frozenset(
            map(lambda c: c.name, diff_columns)
        )
        current_names: FrozenSet[str] = frozenset(
            map(lambda c: c.name, table_draft.columns)
        )
        if not diff_names.isdisjoint(current_names):
            raise MutateColumnException(
                'Cannot update the type of existing columns.'
                f'Columns: {diff_names.intersection(current_names)}'
            )
        actions: List[CursorExeAction] = []
        table_path: str = \
            f"\"{table_draft.id.schema}\".\"{table_draft.id.table_name}\""
        for column in diff_columns:
            statement: str = (
                'ALTER TABLE {table_path} '
                'ADD COLUMN {column_name} '
                '{field_type} default %(default_val)s'
            )
            actions.append(
                db_client.execute(
                    statement,
                    DynamicSQLargs(
                        values={
                            'default_val': column.default_val
                        },
                        identifiers={
                            'table_path': table_path,
                            'column_name': column.name,
                            'field_type': column.field_type
                        }
                    )
                )
            )
        return actions

    return Table(
        id=table_draft.id,
        primary_keys=table_draft.primary_keys,
        columns=table_draft.columns,
        table_path=table_path,
        add_columns=add_columns,
    )


def exist(db_client: Client, table_id: TableID) -> bool:
    """Check existence of a Table on the DB"""
    statement = """
        SELECT EXISTS (
            SELECT * FROM information_schema.tables
            WHERE table_schema = %(table_schema)s
            AND table_name = %(table_name)s
        );
    """
    action = db_client.execute(
        statement,
        DynamicSQLargs(
            values={
                'table_schema': table_id.schema,
                'table_name': table_id.table_name
            }
        )
    )
    action.act()
    f_action = db_client.fetchone()
    result = tuple(f_action.act())
    return result[0]


def retrieve(db_client: Client, table_id: TableID) -> Optional[Table]:
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
    action: CursorExeAction = db_client.execute(
        statement,
        DynamicSQLargs(
            values={
                'table_schema': table_id.schema,
                'table_name': table_id.table_name
            }
        )
    )
    fetch_action = db_client.fetchall()
    action.act()
    results = fetch_action.act()
    columns = set()
    for column in results:
        columns.add(IsolatedColumn(column[1], column[2], column[5]))
    table_draft = TableDraft(
        id=table_id, primary_keys=frozenset(), columns=frozenset(columns)
    )
    return table_builder(db_client, table_draft)


def create(
    db_client: Client,
    table_draft: Table,
    if_not_exist: bool = False
) -> Table:
    """Creates a Table in the DB and returns it"""
    table_path: str = table_draft.table_path()
    pkeys_fields: str = ''
    if table_draft.primary_keys:
        p_fields: str = ",".join(
            [f"{{pkey_{n}}}" for n in range(len(table_draft.primary_keys))]
        )
        pkeys_fields = f',PRIMARY KEY({p_fields})'
    not_exists: str = '' if not if_not_exist else 'IF NOT EXISTS '
    fields: str = ",".join(
        [
            f"{{name_{n}}} {{field_type_{n}}}"
            for n in range(len(table_draft.columns))
        ]
    )
    fields_def: str = f'{fields}{pkeys_fields}'
    statement: str = (
        f"CREATE TABLE {not_exists}{{table_path}} ({fields_def})"
    )
    identifiers: Dict[str, Optional[str]] = {
        'table_path': table_path
    }
    for index, value in enumerate(table_draft.primary_keys):
        identifiers[f'pkey_{index}'] = value
    for index, column in enumerate(table_draft.columns):
        identifiers[f'name_{index}'] = column.name
        identifiers[f'field_type_{index}'] = column.field_type

    db_client.execute(
        statement,
        DynamicSQLargs(
            identifiers=identifiers
        )
    )
    result: Optional[Table] = retrieve(db_client, table_draft.id)
    if result:
        return result
    raise TableCreationFail(
        'Could not create and verify the existence of table: '
        f'{table_draft.id}'
    )
