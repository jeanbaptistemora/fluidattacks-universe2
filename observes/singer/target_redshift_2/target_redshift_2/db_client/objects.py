"""Define interface of db objects"""
# Standard libraries
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    Tuple,
    Union,
    FrozenSet,
    List,
    NamedTuple,
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


class DynamicSQLargs(NamedTuple):
    values: Dict[str, Any] = {}
    identifiers: Dict[str, Any] = {}


SQLidPurifier = Callable[[str, Optional[DynamicSQLargs]], str]


# ----------------- db actions ------------------
class FetchAction(Enum):
    ALL = 'all'
    ONE = 'one'


class CursorExeAction(NamedTuple):
    cursor: PGCURR
    act: Callable[[], Any]
    statement: str


class CursorFetchAction(NamedTuple):
    cursor: PGCURR
    act: Callable[
        [], Union[
            Tuple[Any, ...], Tuple[Tuple[Any, ...], ...]
        ]
    ]
    fetch_type: FetchAction


# ----------------- column ------------------
class IsolatedColumn(NamedTuple):
    name: str
    field_type: str
    default_val: Optional[str] = None


class Column(NamedTuple):
    table: 'TableID'
    column: IsolatedColumn


# ----------------- table ------------------
class TableID(NamedTuple):
    schema: 'SchemaID'
    table_name: str


class TablePrototype(NamedTuple):
    # Any should be `Table` but mypy do not support recursive types
    table_path: Callable[[Any], str]
    add_columns: Callable[
        [Any, FrozenSet[IsolatedColumn]], List[CursorExeAction]
    ]


class Table(NamedTuple):
    id: TableID
    primary_keys: FrozenSet[str]
    columns: FrozenSet[IsolatedColumn]
    prototype: TablePrototype

    def table_path(self: 'Table') -> str:
        return self.prototype.table_path(self)

    def add_columns(
        self: 'Table', new_columns: FrozenSet[IsolatedColumn]
    ) -> List[CursorExeAction]:
        return self.prototype.add_columns(self, new_columns)


# ----------------- db schema ------------------
class SchemaID(NamedTuple):
    connection: Optional[ConnectionID]
    schema_name: str


class Schema(NamedTuple):
    id: SchemaID


# ----------------- client ------------------
class ClientPrototype(NamedTuple):
    # Any should be `Client` but mypy do not support recursive types
    execute: Callable[[Any, str, Optional[DynamicSQLargs]], CursorExeAction]
    fetchall: Callable[[Any], CursorFetchAction]
    fetchone: Callable[[Any], CursorFetchAction]
    drop_access_point: Callable[[Any], None]


class Client(NamedTuple):
    connection: PGCONN
    cursor: PGCURR
    prototype: ClientPrototype

    def drop_access_point(self: 'Client') -> None:
        return self.prototype.drop_access_point(self)

    def execute(
        self: 'Client', statement: str, args: Optional[DynamicSQLargs] = None
    ) -> CursorExeAction:
        return self.prototype.execute(self, statement, args)

    def fetchall(self: 'Client') -> CursorFetchAction:
        return self.prototype.fetchall(self)

    def fetchone(self: 'Client') -> CursorFetchAction:
        return self.prototype.fetchone(self)


class MutateColumnException(Exception):
    pass


class TableCreationFail(Exception):
    pass
