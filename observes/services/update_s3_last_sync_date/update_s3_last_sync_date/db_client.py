# Standard libraries
from typing import (
    Any,
    Dict, NamedTuple,
)
# Third party libraries
import psycopg2 as postgres
import psycopg2.extensions as postgres_extensions
# Local libraries

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


def create_timestamp(state: DbState, group: str) -> None:
    query = (
        "INSERT INTO \"repos-s3-sync\".last_sync_date "
        f"(group_name,sync_date) VALUES ('{group}',getdate())"
    )
    state.cursor.execute(query)


def update_timestamp(state: DbState, group: str) -> None:
    query = (
        "UPDATE \"repos-s3-sync\".last_sync_date "
        f"set sync_date=getdate() WHERE group_name='{group}'"
    )
    state.cursor.execute(query)


def create_or_update(state: DbState, group: str) -> None:
    query = (
        "SELECT * FROM \"repos-s3-sync\".last_sync_date "
        f"WHERE group_name='{group}'"
    )
    state.cursor.execute(query)
    result = state.cursor.fetchall()
    if not result:
        create_timestamp(state, group)
    else:
        update_timestamp(state, group)
