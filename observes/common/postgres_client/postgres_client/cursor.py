# pylint: skip-file
# Standard libraries
from __future__ import annotations
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    NamedTuple,
    Optional,
    Union,
)

# Third party libraries
from deprecated import deprecated
from returns.maybe import Maybe
from returns.io import IO, impure
from psycopg2 import sql as postgres_sql

# Local libraries
from postgres_client.connection import DbConnection


class FetchAction(Enum):
    ALL = "all"
    ONE = "one"


class DynamicSQLargs(NamedTuple):
    values: Dict[str, Optional[str]] = {}
    identifiers: Dict[str, Optional[str]] = {}


class CursorExeAction(NamedTuple):
    act: Callable[[], Any]
    statement: str


class CursorFetchAction(NamedTuple):
    act: Callable[[], Union[Iterable[Any]]]
    fetch_type: FetchAction


CursorAction = Union[CursorExeAction, CursorFetchAction]
SQLidPurifier = Callable[[str, Optional[DynamicSQLargs]], str]
DbCursor = Any


def sql_id_purifier(
    statement: str, args: Optional[DynamicSQLargs] = None
) -> Any:
    raw_sql = postgres_sql.SQL(statement)
    format_input = (
        dict(
            map(
                lambda t: (t[0], postgres_sql.Identifier(t[1])),
                args.identifiers.items(),
            )
        )
        if args
        else {}
    )
    if format_input:
        return raw_sql.format(**format_input)
    return statement


def _act_exe_action(
    purify_sql_ids: SQLidPurifier,
    cursor: DbCursor,
    statement: str,
    args: Optional[DynamicSQLargs] = None,
) -> None:
    safe_stm = purify_sql_ids(statement, args)
    stm_values = args.values if args else {}
    cursor.execute(safe_stm, stm_values)


def _make_exe_action(
    cursor: DbCursor,
    statement: str,
    args: Optional[DynamicSQLargs] = None,
) -> CursorExeAction:
    def action() -> None:
        _act_exe_action(sql_id_purifier, cursor, statement, args)

    return CursorExeAction(statement=statement, act=action)


def _make_fetch_action(
    cursor: DbCursor, f_action: FetchAction
) -> CursorFetchAction:
    action = (
        cursor.fetchall if f_action == FetchAction.ALL else cursor.fetchone
    )
    return CursorFetchAction(act=action, fetch_type=f_action)


class Query(NamedTuple):
    query: str
    args: Maybe[DynamicSQLargs]

    @classmethod
    def new(cls, query: str, args: Maybe[DynamicSQLargs]) -> Query:
        return cls(
            query=sql_id_purifier(query, args.value_or(None)), args=args
        )


class Cursor(NamedTuple):
    db_cursor: DbCursor

    @deprecated(reason="Use execute_query instead")
    def execute(
        self, stm: str, args: Optional[DynamicSQLargs] = None
    ) -> CursorExeAction:
        return _make_exe_action(self.db_cursor, stm, args)

    @deprecated(reason="Use fetch_all instead")
    def fetchall(self) -> CursorFetchAction:
        return _make_fetch_action(self.db_cursor, FetchAction.ALL)

    @deprecated(reason="Use fetch_one instead")
    def fetchone(self) -> CursorFetchAction:
        return _make_fetch_action(self.db_cursor, FetchAction.ONE)

    @impure
    def close(self) -> None:
        return self.db_cursor.close()

    @impure
    def execute_query(self, query: Query) -> None:
        stm_values: Dict[str, Optional[str]] = query.args.map(
            lambda args: args.values
        ).value_or({})
        self.db_cursor.execute(query.query, stm_values)

    def fetch_all(self) -> IO[Any]:
        return IO(self.db_cursor.fetchall())

    def fetch_one(self) -> IO[Iterator[Any]]:
        return IO(self.db_cursor.fetchone())

    @classmethod
    def new(cls, connection: DbConnection) -> Cursor:
        db_cursor = connection.get_cursor()
        return cls(db_cursor)

    @classmethod
    def from_raw(cls, db_cursor: DbCursor) -> Cursor:
        return cls(db_cursor)


def act(actions: List[CursorAction]) -> List[Any]:
    return list(map(lambda action: action.act(), actions))


def adapt_cursor(db_cursor: DbCursor) -> Cursor:
    return Cursor.from_raw(db_cursor)


def new_cursor(connection: DbConnection) -> Cursor:
    return Cursor.new(connection)
