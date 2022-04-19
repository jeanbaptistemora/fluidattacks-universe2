from os import (
    environ,
)
import psycopg2 as postgres
import psycopg2.extensions as postgres_extensions
from toolbox import (
    utils,
)
from typing import (
    Any,
    NamedTuple,
)

PGCONN = Any
PGCURR = Any
SCHEMA = "repos-s3-sync"


class DbState(NamedTuple):
    connection: PGCONN
    cursor: PGCURR


def make_access_point() -> DbState:
    encrypted_db_creds = [
        "REDSHIFT_DATABASE",
        "REDSHIFT_USER",
        "REDSHIFT_PASSWORD",
        "REDSHIFT_HOST",
        "REDSHIFT_PORT",
    ]
    decrypted_db_creds = []
    for encrypted_cred in encrypted_db_creds:
        decrypted_cred = utils.generic.get_sops_secret(
            encrypted_cred,
            environ["MELTS_SECRETS"],
            "continuous-admin",
        )
        decrypted_db_creds.append(decrypted_cred)
    dbcon: PGCONN = postgres.connect(
        dbname=decrypted_db_creds[0],
        user=decrypted_db_creds[1],
        password=decrypted_db_creds[2],
        host=decrypted_db_creds[3],
        port=decrypted_db_creds[4],
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


def confirm_synced_group(state: DbState, group: str, table: str) -> None:
    query = f'SELECT * FROM "{SCHEMA}".{table} ' f"WHERE group_name='{group}'"
    state.cursor.execute(query)
    result = state.cursor.fetchall()
    if not result:
        _create_timestamp_group(state, group, table)
    else:
        _update_timestamp_group(state, group, table)


def update_last_sync_date(table: str, group: str) -> None:
    db_state = make_access_point()
    try:
        confirm_synced_group(db_state, group, table)
    finally:
        drop_access_point(db_state)
