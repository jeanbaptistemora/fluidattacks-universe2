# Standard libraries
from typing import (
    Any,
    Set,
    Tuple,
)
# Third party libraries
# Local libraries
from postgres_client.cursor import (
    Cursor,
    DynamicSQLargs,
)
from zoho_crm_etl.api import BulkJob


def get_bulk_jobs(cursor: Cursor, db_schema: str) -> Set[BulkJob]:
    statement = 'SELECT * FROM {schema_name}.bulk_jobs'
    exe_action = cursor.execute(
        statement,
        DynamicSQLargs(identifiers={'schema_name': db_schema})
    )
    exe_action.act()
    fetch_action = cursor.fetchall()
    results = fetch_action.act()

    def tuple_to_bulkjob(element: Tuple[Any, ...]) -> BulkJob:
        return BulkJob(
            operation=element[0],
            created_by=element[1],
            created_time=element[2],
            state=element[3],
            id=element[4],
            result=element[5]
        )

    return set(map(tuple_to_bulkjob, results))


def save_bulk_job_state(cursor: Cursor, job: BulkJob, db_schema: str):
    statement = """
        INSERT INTO {schema_name}.bulk_jobs VALUES (
            %(operation)s,
            %(created_by)s,
            %(created_time)s,
            %(state)s,
            %(id)s
        )
    """
    exe_action = cursor.execute(
        statement,
        DynamicSQLargs(
            values=dict(job._asdict()),
            identifiers={'schema_name': db_schema}
        )
    )
    exe_action.act()
