import psycopg2 as postgres
import psycopg2.extensions as postgres_extensions
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
)

PGCONN = Any
PGCURR = Any
SCHEMA = "repos-s3-sync"


class DbState(NamedTuple):
    connection: PGCONN
    cursor: PGCURR


def make_access_point(auth: Dict[str, str]) -> DbState:
    dbcon: PGCONN = postgres.connect(
        dbname=auth["dbname"],
        user=auth["user"],
        password=auth["password"],
        host=auth["host"],
        port=auth["port"],
    )
    dbcon.set_session(readonly=False)
    dbcon.set_isolation_level(postgres_extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    dbcur: PGCURR = dbcon.cursor()

    return DbState(connection=dbcon, cursor=dbcur)


def drop_access_point(state: DbState) -> None:
    state.cursor.close()
    state.connection.close()


def _create_timestamp_group(state: DbState, group: str, table: str) -> None:
    query = (
        f'INSERT INTO "{SCHEMA}".{table} '
        f"(group_name,sync_date) VALUES ('{group}',getdate())"
    )
    state.cursor.execute(query)


def _update_timestamp_group(state: DbState, group: str, table: str) -> None:
    query = (
        f'UPDATE "{SCHEMA}".{table} '
        f"set sync_date=getdate() WHERE group_name='{group}'"
    )
    state.cursor.execute(query)


def compound_job_update(state: DbState, group: str, table: str) -> None:
    query = f'SELECT * FROM "{SCHEMA}".{table} ' f"WHERE group_name='{group}'"
    state.cursor.execute(query)
    result = state.cursor.fetchall()
    if not result:
        _create_timestamp_group(state, group, table)
    else:
        _update_timestamp_group(state, group, table)


def _create_timestamp_job(state: DbState, job_name: str) -> None:
    query = (
        f'INSERT INTO "{SCHEMA}".last_sync_jobs '
        f"(job_name,sync_date) VALUES ('{job_name}',getdate())"
    )
    state.cursor.execute(query)


def _update_timestamp_job(state: DbState, job_name: str) -> None:
    query = (
        f'UPDATE "{SCHEMA}".last_sync_jobs '
        f"set sync_date=getdate() WHERE job_name='{job_name}'"
    )
    state.cursor.execute(query)


def _get_single_job(state: DbState, job_name: str) -> List[Any]:
    query = (
        f'SELECT * FROM "{SCHEMA}".last_sync_jobs '
        f"WHERE job_name='{job_name}'"
    )
    state.cursor.execute(query)
    result = state.cursor.fetchall()
    return result


def single_job_update(state: DbState, job_name: str) -> None:
    if not _get_single_job(state, job_name):
        _create_timestamp_job(state, job_name)
    else:
        _update_timestamp_job(state, job_name)
