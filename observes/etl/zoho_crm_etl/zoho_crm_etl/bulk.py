# Standard libraries
from typing import (
    Callable,
    FrozenSet,
    NamedTuple,
    Tuple,
)
# Third party libraries
# Local libraries
from zoho_crm_etl import utils
from zoho_crm_etl.api import (
    ApiClient,
    BulkData,
    BulkJob,
    ModuleName,
)
from zoho_crm_etl.db import Client as DbClient


LOG = utils.get_log(__name__)


class BulkUtils(NamedTuple):
    create: Callable[[ModuleName, int], None]
    update_all: Callable[[], None]
    get_all: Callable[[], FrozenSet[BulkJob]]
    extract_data: Callable[[FrozenSet[str]], FrozenSet[BulkData]]


def create_bulk_job(
    api_client: ApiClient,
    db_client: DbClient,
    module: ModuleName,
    page: int
) -> None:
    """Creates bulk job on crm and stores it on DB"""
    job: BulkJob = api_client.create_bulk_read_job(module, page)
    db_client.save_bulk_job(job)


def update_all(
    api_client: ApiClient,
    db_client: DbClient
) -> None:
    """
    Get the updated status of the jobs (from crm) and update them in the DB
    """
    jobs: FrozenSet[BulkJob] = db_client.get_bulk_jobs()
    updated_jobs: FrozenSet[BulkJob] = frozenset(
        map(lambda job: api_client.get_bulk_job(job.id), jobs)
    )
    current_status = frozenset(map(lambda j: (j.id, j.state), jobs))
    updated_status = frozenset(map(lambda j: (j.id, j.state), updated_jobs))

    need_update: FrozenSet[Tuple[str, str]] = updated_status - current_status
    need_update_ids: FrozenSet[str] = frozenset([id for id, s in need_update])
    LOG.info('Updating %s jobs status', len(need_update))
    list(
        map(
            db_client.update_bulk_job,
            frozenset(filter(lambda job: job.id in need_update_ids, jobs))
        )
    )


def get_bulk_data(
    api_client: ApiClient,
    jobs_id: FrozenSet[str]
) -> FrozenSet[BulkData]:
    return frozenset(map(api_client.download_result, jobs_id))


def new_bulk_utils(
    api_client: ApiClient,
    db_client: DbClient
) -> BulkUtils:
    """Generator of `BulkUtils` with constant clients"""
    def create_bulk(module: ModuleName, page: int) -> None:
        create_bulk_job(api_client, db_client, module, page)

    def update_bulks() -> None:
        update_all(api_client, db_client)

    def extract(jobs_id: FrozenSet[str]) -> FrozenSet[BulkData]:
        return get_bulk_data(api_client, jobs_id)

    return BulkUtils(
        create=create_bulk,
        update_all=update_bulks,
        get_all=db_client.get_bulk_jobs,
        extract_data=extract
    )
