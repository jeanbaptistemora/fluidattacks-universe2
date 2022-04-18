import getpass
from postgres_client import (
    client,
)
from postgres_client.client import (
    Client,
)
from postgres_client.query import (
    Query,
    SqlArgs,
)
import pytest
from tap_zoho_crm import (
    db,
)
from tap_zoho_crm.api.bulk import (
    BulkJob,
    ModuleName,
)


def setup_db(db_client: Client) -> None:
    schema = "super-schema"
    db_client.cursor.execute_query(
        Query(
            "CREATE SCHEMA {schema_name}",
            SqlArgs(identifiers={"schema_name": schema}),
        )
    )
    db_client.cursor.execute_query(
        Query(
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
            SqlArgs(identifiers={"schema_name": schema}),
        )
    )
    db_client.connection.commit()


def test_bulk_job() -> BulkJob:
    return BulkJob(
        operation="operation1",
        created_by='{"author": master"}',
        created_time='{"time": "2020-01-01 00:00"}',
        state="procesing",
        id="a1234bc",
        module=ModuleName.PRICE_BOOKS,
        page=1,
        result=None,
    )


@pytest.mark.xfail(
    getpass.getuser() == "root", reason="can not run with root"
)  # type: ignore
def test_save_load_bulk_job_integrated(postgresql):
    # Arrange
    db_client = client.new_test_client(postgresql)
    setup_db(db_client)
    test_job = test_bulk_job()
    schema = "super-schema"
    # Act
    db.save_bulk_job(db_client, test_job, schema)
    db_client.connection.commit()
    jobs = db.get_bulk_jobs(db_client, schema)
    # Assert
    assert test_job in jobs


@pytest.mark.xfail(
    getpass.getuser() == "root", reason="can not run with root"
)  # type: ignore
def test_update_bulk_job_integrated(postgresql):
    # Arrange
    db_client = client.new_test_client(postgresql)
    setup_db(db_client)
    test_job = test_bulk_job()
    updated_job = BulkJob(
        operation=test_job.operation,
        created_by=test_job.created_by,
        created_time=test_job.created_time,
        state="done",
        id=test_job.id,
        module=test_job.module,
        page=test_job.page,
        result=test_job.result,
    )
    schema = "super-schema"
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
