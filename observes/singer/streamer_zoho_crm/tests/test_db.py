# Standard libraries
import getpass
# Third party libraries
import pytest
from pytest_postgresql import factories
# Local libraries
from postgres_client import client
from postgres_client.client import Client
from postgres_client.cursor import (
    DynamicSQLargs,
)
from streamer_zoho_crm import db
from streamer_zoho_crm.temp_api import BulkJob, ModuleName

postgresql_my_proc = factories.postgresql_proc(
    port=None, unixsocketdir='/var/run/postgresql')
postgresql_my = factories.postgresql('postgresql_my_proc')


def setup_db(db_client: Client) -> None:
    schema = 'super-schema'
    create_schema = db_client.cursor.execute(
        'CREATE SCHEMA {schema_name}',
        DynamicSQLargs(identifiers={'schema_name': schema})
    )
    create_table = db_client.cursor.execute(
        """
            CREATE TABLE {schema_name}.bulk_jobs (
                operation VARCHAR,
                created_by VARCHAR,
                created_time VARCHAR,
                state VARCHAR,
                id VARCHAR,
                module VARCHAR,
                page INTEGER,
                result VARCHAR DEFAULT NULL
            );
        """,
        DynamicSQLargs(
            identifiers={'schema_name': schema}
        )
    )
    create_schema.act()
    create_table.act()
    db_client.connection.commit()


@pytest.mark.xfail(
    getpass.getuser() == 'root',
    reason="can not run with root")  # type: ignore
def test_save_load_bulk_job_integrated(postgresql):
    # Arrange
    db_client = client.new_test_client(postgresql)
    setup_db(db_client)
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
    db.save_bulk_job(db_client, test_job, schema)
    db_client.connection.commit()
    jobs = db.get_bulk_jobs(db_client, schema)
    # Assert
    assert test_job in jobs


@pytest.mark.xfail(
    getpass.getuser() == 'root',
    reason="can not run with root")  # type: ignore
def test_update_bulk_job_integrated(postgresql):
    # Arrange
    db_client = client.new_test_client(postgresql)
    setup_db(db_client)
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
    updated_job = BulkJob(
        operation='operation1',
        created_by='{"author": master"}',
        created_time='{"time": "2020-01-01 00:00"}',
        state='done',
        id='a1234bc',
        module=ModuleName.PRICE_BOOKS,
        page=1,
        result=None
    )
    schema = 'super-schema'
    # Act
    db.save_bulk_job(db_client, test_job, schema)
    db_client.connection.commit()
    db.update_bulk_job(db_client, updated_job, schema)
    db_client.connection.commit()
    jobs = db.get_bulk_jobs(db_client, schema)
    # Assert
    expected = updated_job
    assert test_job not in jobs
    assert expected in jobs
