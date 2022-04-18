from postgres_client import (
    client,
)
from postgres_client.client import (
    Client as DbClient,
)
from postgres_client.connection import (
    Credentials as DbCredentials,
    DatabaseID,
)
from postgres_client.query import (
    Query,
    SqlArgs,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from tap_zoho_crm.api.bulk import (
    BulkJob,
    ModuleName,
)
from typing import (
    Any,
    Callable,
    FrozenSet,
    List,
    NamedTuple,
    Tuple,
)

SCHEMA = "zoho_crm"


class Client(NamedTuple):
    get_bulk_jobs: Callable[[], FrozenSet[BulkJob]]
    save_bulk_job: Callable[[BulkJob], None]
    update_bulk_job: Callable[[BulkJob], None]
    close: Callable[[], None]


def get_bulk_jobs(db_client: DbClient, db_schema: str) -> FrozenSet[BulkJob]:
    # TODO: must return an impure IO type
    statement = "SELECT * FROM {schema_name}.bulk_jobs"
    query = Query(statement, SqlArgs(identifiers={"schema_name": db_schema}))
    db_client.cursor.execute_query(query)
    results = unsafe_perform_io(db_client.cursor.fetch_all())

    def tuple_to_bulkjob(element: Tuple[Any, ...]) -> BulkJob:
        return BulkJob(
            operation=element[0],
            created_by=element[1],
            created_time=element[2],
            state=element[3],
            id=element[4],
            module=ModuleName(element[5]),
            page=element[6],
            result=element[7],
        )

    return frozenset(map(tuple_to_bulkjob, results))


def save_bulk_job(db_client: DbClient, job: BulkJob, db_schema: str) -> None:
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
    job_dict["module"] = job_dict["module"].value
    query = Query(
        statement,
        SqlArgs(values=job_dict, identifiers={"schema_name": db_schema}),
    )
    db_client.cursor.execute_query(query)


def update_bulk_job(db_client: DbClient, job: BulkJob, db_schema: str) -> None:
    statement = """
        UPDATE {schema_name}.bulk_jobs SET
            state = %(state)s
        WHERE id = %(id)s
    """
    job_dict = dict(job._asdict())
    query = Query(
        statement,
        SqlArgs(values=job_dict, identifiers={"schema_name": db_schema}),
    )
    db_client.cursor.execute_query(query)


def init_db(db_id: DatabaseID, db_creds: DbCredentials) -> None:
    db_client: DbClient = client.new_client(db_id, db_creds)
    create_schema = f"""
        CREATE SCHEMA IF NOT EXISTS {SCHEMA};
    """
    create_table = f"""
        CREATE TABLE IF NOT EXISTS {SCHEMA}.bulk_jobs (
            operation VARCHAR,
            created_by VARCHAR,
            created_time VARCHAR,
            state VARCHAR,
            id VARCHAR,
            module VARCHAR,
            page INTEGER,
            result VARCHAR DEFAULT NULL
        );
    """
    queries: List[Query] = [
        Query(query) for query in [create_schema, create_table]
    ]
    try:
        db_client.cursor.execute_queries(queries)
    finally:
        db_client.close()


def new_client(
    db_id: DatabaseID, db_creds: DbCredentials, db_schema: str = SCHEMA
) -> Client:
    db_client: DbClient = client.new_client(db_id, db_creds)

    def get_jobs() -> FrozenSet[BulkJob]:
        return get_bulk_jobs(db_client, db_schema)

    def save_job(job: BulkJob) -> None:
        save_bulk_job(db_client, job, db_schema)

    def update_job(job: BulkJob) -> None:
        update_bulk_job(db_client, job, db_schema)

    return Client(
        get_bulk_jobs=get_jobs,
        save_bulk_job=save_job,
        update_bulk_job=update_job,
        close=db_client.close,
    )
