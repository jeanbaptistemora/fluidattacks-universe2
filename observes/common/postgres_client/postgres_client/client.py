# Standard libraries
from typing import (
    Callable,
    NamedTuple,
    Optional,
)
# Third party libraries
# Local libraries
from postgres_client import cursor as cursor_module
from postgres_client.connection import DbConnection
from postgres_client.cursor import (
    CursorExeAction,
    CursorFetchAction,
    DynamicSQLargs,
    FetchAction,
)


class Client(NamedTuple):
    execute: Callable[[str, Optional[DynamicSQLargs]], CursorExeAction]
    fetchall: Callable[[], CursorFetchAction]
    fetchone: Callable[[], CursorFetchAction]
    drop_access_point: Callable[[], None]


def new_client(
    connection: DbConnection,
) -> Client:
    cursor = connection.get_cursor()
    sql_id_purifier = cursor_module.sql_id_purifier_builder()
    make_exe_action = cursor_module.make_exe_action_builder(
        cursor, sql_id_purifier
    )
    make_fetch_action = cursor_module.make_fetch_action_builder(
        cursor
    )

    def drop_access_point() -> None:
        cursor.close()
        connection.close()

    def execute(
        statement: str, args: Optional[DynamicSQLargs] = None
    ) -> CursorExeAction:
        return make_exe_action(statement, args)

    def fetchall() -> CursorFetchAction:
        return make_fetch_action(FetchAction.ALL)

    def fetchone() -> CursorFetchAction:
        return make_fetch_action(FetchAction.ONE)

    return Client(
        execute=execute,
        fetchall=fetchall,
        fetchone=fetchone,
        drop_access_point=drop_access_point,
    )
