# Standard libraries
from typing import (
    Any,
    Dict, NamedTuple,
)
# Third party libraries
import psycopg2 as postgres
import psycopg2.extensions as postgres_extensions
# Local libraries
from dif_gitlab_etl.utils import log

PGCONN = Any
PGCURR = Any


class DbState(NamedTuple):
    connection: PGCONN
    cursor: PGCURR


def make_access_point(auth: Dict[str, str]) -> DbState:
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

    return DbState(connection=dbcon, cursor=dbcur)


def drop_access_point(state: DbState) -> None:
    state.cursor.close()
    state.connection.close()


def execute(state: DbState, statement: str) -> None:
    log('debug', f"EXEC: {statement}.")
    try:
        state.cursor.execute(statement)
    except postgres.ProgrammingError as exc:
        log('EXCEPTION', f'{type(exc)} {exc}')
