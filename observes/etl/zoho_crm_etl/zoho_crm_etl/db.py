# Standard libraries
from typing import (
    Any,
    Callable,
    NamedTuple,
    Set,
    Tuple,
)
# Third party libraries
# Local libraries
from postgres_client import connection, client
from postgres_client.client import Client as DbClient
from postgres_client.connection import ConnectionID, DbConnection
from postgres_client.cursor import (
    DynamicSQLargs,
)
from zoho_crm_etl.api import BulkJob, ModuleName


class Client(NamedTuple):
    get_bulk_jobs: Callable[[str], Set[BulkJob]]
    save_bulk_job: Callable[[BulkJob, str], None]


def get_bulk_jobs(db_client: DbClient, db_schema: str) -> Set[BulkJob]:
    statement = 'SELECT * FROM {schema_name}.bulk_jobs'
    exe_action = db_client.execute(
        statement,
        DynamicSQLargs(identifiers={'schema_name': db_schema})
    )
    exe_action.act()
    fetch_action = db_client.fetchall()
    results = fetch_action.act()

    def tuple_to_bulkjob(element: Tuple[Any, ...]) -> BulkJob:
        return BulkJob(
            operation=element[0],
            created_by=element[1],
            created_time=element[2],
            state=element[3],
            id=element[4],
            module=ModuleName(element[5]),
            page=element[6],
            result=element[7]
        )

    return set(map(tuple_to_bulkjob, results))


def save_bulk_job_state(
    db_client: DbClient, job: BulkJob, db_schema: str
) -> None:
    statement = """
        INSERT INTO {schema_name}.bulk_jobs VALUES (
            %(operation)s,
            %(created_by)s,
            %(created_time)s,
            %(state)s,
            %(id)s,
            %(module)s,
            %(page)s
        )
    """
    job_dict = dict(job._asdict())
    job_dict['module'] = job_dict['module'].value
    exe_action = db_client.execute(
        statement,
        DynamicSQLargs(
            values=job_dict,
            identifiers={'schema_name': db_schema}
        )
    )
    exe_action.act()


def new_client(db_auth: ConnectionID) -> Client:
    db_connection: DbConnection = connection.make_access_point(db_auth)
    db_client: DbClient = client.new_client(db_connection)

    def get_jobs(schema: str) -> Set[BulkJob]:
        return get_bulk_jobs(db_client, schema)

    def save_job(job: BulkJob, schema: str) -> None:
        save_bulk_job_state(db_client, job, schema)

    return Client(
        get_bulk_jobs=get_jobs,
        save_bulk_job=save_job
    )
