# Standard libraries
from datetime import datetime
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
SCHEMA = 'repos-s3-sync'


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


def create_timestamp_group(state: DbState, group: str, table: str) -> None:
    timestamp = datetime.timestamp(datetime.now())
    query = (
        f"INSERT INTO \"{SCHEMA}\".{table} "
        f"(group_name,sync_date) VALUES ('{group}',{timestamp})"
    )
    state.cursor.execute(query)


def update_timestamp_group(state: DbState, group: str, table: str) -> None:
    timestamp = datetime.timestamp(datetime.now())
    query = (
        f"UPDATE \"{SCHEMA}\".{table} "
        f"set sync_date={timestamp} WHERE group_name='{group}'"
    )
    state.cursor.execute(query)


def create_or_update_group(state: DbState, group: str, table: str) -> None:
    query = (
        f"SELECT * FROM \"{SCHEMA}\".{table} "
        f"WHERE group_name='{group}'"
    )
    state.cursor.execute(query)
    result = state.cursor.fetchall()
    if not result:
        create_timestamp_group(state, group, table)
    else:
        update_timestamp_group(state, group, table)


def create_timestamp_job(state: DbState, job_name: str) -> None:
    query = (
        f"INSERT INTO \"{SCHEMA}\".last_sync_jobs "
        f"(job_name,sync_date) VALUES ('{job_name}',getdate())"
    )
    state.cursor.execute(query)


def update_timestamp_job(state: DbState, job_name: str) -> None:
    query = (
        f"UPDATE \"{SCHEMA}\".last_sync_jobs "
        f"set sync_date=getdate() WHERE job_name='{job_name}'"
    )
    state.cursor.execute(query)


def create_or_update_job(state: DbState, job_name: str) -> None:
    query = (
        f"SELECT * FROM \"{SCHEMA}\".last_sync_jobs "
        f"WHERE job_name='{job_name}'"
    )
    state.cursor.execute(query)
    result = state.cursor.fetchall()
    if not result:
        create_timestamp_job(state, job_name)
    else:
        update_timestamp_job(state, job_name)
