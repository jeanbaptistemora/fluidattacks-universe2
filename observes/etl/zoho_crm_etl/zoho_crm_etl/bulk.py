# Standard libraries
from typing import (
    Callable,
    FrozenSet,
    NamedTuple,
)
# Third party libraries
# Local libraries
from zoho_crm_etl import utils
from zoho_crm_etl.api import ApiClient, BulkJob, ModuleName
from zoho_crm_etl.db import Client as DbClient


LOG = utils.get_log(__name__)


class BulkUtils(NamedTuple):
    create: Callable[[ModuleName, int], None]
    update_all: Callable[[], None]
    get_all: Callable[[], FrozenSet[BulkJob]]


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
    need_update: FrozenSet[BulkJob] = updated_jobs - jobs
    LOG.info('Updating %s jobs status', len(need_update))
    map(db_client.update_bulk_job, need_update)


def new_bulk_utils(
    api_client: ApiClient,
    db_client: DbClient
) -> BulkUtils:
    """Generator of `BulkUtils` with constant clients"""
    def create_bulk(module: ModuleName, page: int) -> None:
        create_bulk_job(api_client, db_client, module, page)

    def update_bulks() -> None:
        update_all(api_client, db_client)

    return BulkUtils(
        create=create_bulk,
        update_all=update_bulks,
        get_all=db_client.get_bulk_jobs,
    )
