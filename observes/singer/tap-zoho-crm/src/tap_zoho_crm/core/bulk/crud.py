import logging
from tap_zoho_crm.api import (
    ApiClient,
)
from tap_zoho_crm.api.bulk import (
    BulkData,
    BulkJob,
    ModuleName,
)
from tap_zoho_crm.db import (
    Client as DbClient,
)
from typing import (
    FrozenSet,
    Tuple,
)

LOG = logging.getLogger(__name__)


def create_bulk_job(
    api_client: ApiClient, db_client: DbClient, module: ModuleName, page: int
) -> None:
    """Creates bulk job on crm and stores it on DB"""
    job: BulkJob = api_client.bulk.create_bulk_read_job(module, page)
    db_client.save_bulk_job(job)


def update_all(api_client: ApiClient, db_client: DbClient) -> None:
    """
    Get the updated status of the jobs (from crm) and update them in the DB
    """
    jobs: FrozenSet[BulkJob] = db_client.get_bulk_jobs()
    updated_jobs: FrozenSet[BulkJob] = frozenset(
        map(lambda job: api_client.bulk.get_bulk_job(job.id), jobs)
    )
    current_status = frozenset(map(lambda j: (j.id, j.state), jobs))
    updated_status = frozenset(map(lambda j: (j.id, j.state), updated_jobs))

    need_update: FrozenSet[Tuple[str, str]] = updated_status - current_status
    need_update_ids: FrozenSet[str] = frozenset([id for id, s in need_update])
    LOG.info("Updating %s jobs status", len(need_update))
    list(
        map(
            db_client.update_bulk_job,
            frozenset(
                filter(lambda job: job.id in need_update_ids, updated_jobs)
            ),
        )
    )


def get_bulk_data(
    api_client: ApiClient, jobs_id: FrozenSet[str]
) -> FrozenSet[BulkData]:
    return frozenset(map(api_client.bulk.download_result, jobs_id))
