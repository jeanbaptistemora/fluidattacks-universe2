
# Standard libraries
import getpass
from typing import Any, Iterable, Optional
# Third party libraries
import pytest
from pytest_postgresql import factories
# Local libraries
from postgres_client import cursor as cursor_module
from postgres_client.cursor import (
    Cursor,
    CursorExeAction,
    CursorFetchAction,
    DynamicSQLargs,
    FetchAction,
)
from zoho_crm_etl import db
from zoho_crm_etl.api import BulkJob, ModuleName

postgresql_my_proc = factories.postgresql_proc(
    port=None, unixsocketdir='/var/run/postgresql')
postgresql_my = factories.postgresql('postgresql_my_proc')


def setup_cursor(postgresql: Any) -> Cursor:
    cur = postgresql.cursor()
    purifier = cursor_module.sql_id_purifier_builder()

    def mock_close() -> None:
        cur.close()
        postgresql.close()

    def mock_execute(
        statement: str, args: Optional[DynamicSQLargs] = None
    ) -> CursorExeAction:
        def act() -> None:
            safe_stm = purifier(statement, args)
            stm_values = args.values if args else {}
            cur.execute(safe_stm, stm_values)
            postgresql.commit()
        return CursorExeAction(
            act=act, statement=statement
        )

    def mock_fetchall() -> CursorFetchAction:
        def act() -> Iterable[Any]:
            return iter(cur.fetchall())
        return CursorFetchAction(
            act=act, fetch_type=FetchAction.ALL
        )

    def mock_fetchone() -> CursorFetchAction:
        def act() -> Iterable[Any]:
            return iter(cur.fetchone())
        return CursorFetchAction(
            act=act, fetch_type=FetchAction.ONE
        )

    return Cursor(
        execute=mock_execute,
        fetchall=mock_fetchall,
        fetchone=mock_fetchone,
        close=mock_close
    )


def setup_db(cursor: Cursor) -> None:
    create_schema = cursor.execute('CREATE SCHEMA \"super-schema\"')
    create_table = cursor.execute("""
        CREATE TABLE \"super-schema\".bulk_jobs (
            operation VARCHAR,
            created_by VARCHAR,
            created_time VARCHAR,
            state VARCHAR,
            id VARCHAR,
            module VARCHAR,
            page INTEGER,
            result VARCHAR DEFAULT NULL
        );
    """)
    create_schema.act()
    create_table.act()


@pytest.mark.xfail(
    getpass.getuser() == 'root',
    reason="can not run with root")  # type: ignore
def test_save_load_bulk_job_integrated(  # pylint: disable=redefined-outer-name
    postgresql_my  # is a fixture
):
    # Arrange
    cursor = setup_cursor(postgresql_my)
    setup_db(cursor)
    test_job = BulkJob(
        operation='operation1',
        created_by='{"author": master"}',
        created_time='{"time": "2020-01-01 00:00"}',
        state='procesing',
        id='a1234bc',
        module=ModuleName.PRICE_BOOKS,
        page=1,
        result=None
    )
    schema = 'super-schema'
    # Act
    db.save_bulk_job_state(cursor, test_job, schema)
    jobs = db.get_bulk_jobs(cursor, schema)
    # Assert
    assert test_job in jobs
