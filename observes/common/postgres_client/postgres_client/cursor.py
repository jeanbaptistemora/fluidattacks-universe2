# Standard libraries
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Union,
)
# Third party libraries
from psycopg2 import sql as postgres_sql
# Local libraries
from postgres_client.connection import DbConnection


class FetchAction(Enum):
    ALL = 'all'
    ONE = 'one'


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


class Cursor(NamedTuple):
    act: Callable[[List[CursorAction]], List[Any]]
    execute: Callable[[str, Optional[DynamicSQLargs]], CursorExeAction]
    fetchall: Callable[[], CursorFetchAction]
    fetchone: Callable[[], CursorFetchAction]
    close: Callable[[], None]


SQLidPurifier = Callable[[str, Optional[DynamicSQLargs]], str]
DbCursor = Any


def sql_id_purifier(
    statement: str, args: Optional[DynamicSQLargs] = None
) -> Any:
    raw_sql = postgres_sql.SQL(statement)
    format_input = dict(
        map(
            lambda t: (t[0], postgres_sql.Identifier(t[1])),
            args.identifiers.items()
        )
    ) if args else {}
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


def _act(actions: List[CursorAction]) -> List[Any]:
    return list(map(lambda action: action.act(), actions))


def _make_exe_action(
    cursor: DbCursor,
    statement: str,
    args: Optional[DynamicSQLargs] = None,
) -> CursorExeAction:
    def action() -> None:
        _act_exe_action(sql_id_purifier, cursor, statement, args)

    return CursorExeAction(
        statement=statement,
        act=action
    )


def _make_fetch_action(
    cursor: DbCursor, f_action: FetchAction
) -> CursorFetchAction:
    action = \
        cursor.fetchall if f_action == FetchAction.ALL else cursor.fetchone
    return CursorFetchAction(
        act=action,
        fetch_type=f_action
    )


def _cursor_builder(db_cursor: DbCursor) -> Cursor:
    def exe(
        stm: str, args: Optional[DynamicSQLargs] = None
    ) -> CursorExeAction:
        return _make_exe_action(db_cursor, stm, args)

    def f_all() -> CursorFetchAction:
        return _make_fetch_action(db_cursor, FetchAction.ALL)

    def f_one() -> CursorFetchAction:
        return _make_fetch_action(db_cursor, FetchAction.ONE)

    return Cursor(
        act=_act,
        execute=exe,
        fetchall=f_all,
        fetchone=f_one,
        close=db_cursor.close
    )


def adapt_cursor(db_cursor: DbCursor) -> Cursor:
    return _cursor_builder(db_cursor)


def new_cursor(connection: DbConnection) -> Cursor:
    db_cursor = connection.get_cursor()
    return _cursor_builder(db_cursor)
