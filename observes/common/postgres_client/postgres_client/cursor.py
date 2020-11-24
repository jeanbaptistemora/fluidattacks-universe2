# Standard libraries
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    NamedTuple,
    Optional,
    Union,
)
# Third party libraries
import psycopg2 as postgres
from psycopg2 import sql as postgres_sql
# Local libraries


class FetchAction(Enum):
    ALL = 'all'
    ONE = 'one'


class DynamicSQLargs(NamedTuple):
    values: Dict[str, Optional[str]] = {}
    identifiers: Dict[str, Optional[str]] = {}


class Cursor(NamedTuple):
    execute: Callable[..., 'CursorExeAction']
    fetchall: Callable[[], 'CursorFetchAction']
    fetchone: Callable[[], 'CursorFetchAction']
    close: Callable[[], None]


class CursorExeAction(NamedTuple):
    act: Callable[[], Any]
    statement: str


class CursorFetchAction(NamedTuple):
    act: Callable[[], Union[Iterable[Any]]]
    fetch_type: FetchAction


SQLidPurifier = Callable[[str, Optional[DynamicSQLargs]], str]
MakeExeAction = Callable[
    [str, Optional[DynamicSQLargs]], CursorExeAction
]
MakeFetchAction = Callable[[FetchAction], CursorFetchAction]


def make_exe_action_builder(
    cursor: Cursor,
    sql_id_purifier: SQLidPurifier
) -> MakeExeAction:
    def exe_action(
        statement: str,
        args: Optional[DynamicSQLargs] = None
    ) -> CursorExeAction:
        def action() -> Any:
            try:
                safe_stm = sql_id_purifier(statement, args)
                stm_values = args.values if args else {}
                cursor.execute(safe_stm, stm_values)
            except postgres.ProgrammingError as exc:
                raise exc
        return CursorExeAction(
            statement=statement,
            act=action
        )
    return exe_action


def make_fetch_action_builder(cursor: Cursor) -> MakeFetchAction:
    def fetch_action(f_action: FetchAction) -> CursorFetchAction:
        """Generator of `CursorFetchAction` objects"""
        def action() -> Any:
            try:
                if f_action == FetchAction.ALL:
                    return cursor.fetchall()
                return cursor.fetchone()
            except postgres.ProgrammingError as exc:
                raise exc
        return CursorFetchAction(
            act=action,
            fetch_type=f_action
        )
    return fetch_action


def sql_id_purifier_builder(sql_lib: Any = postgres_sql) -> SQLidPurifier:
    def purifier(
        statement: str, args: Optional[DynamicSQLargs] = None
    ) -> str:
        raw_sql = sql_lib.SQL(statement)
        format_input = {}
        if args:
            for key, value in args.identifiers.items():
                format_input[key] = sql_lib.Identifier(value)
        if format_input:
            return raw_sql.format(**format_input)
        return statement
    return purifier
