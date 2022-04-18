from collections import (
    deque,
)
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from dateutil.parser import (  # type: ignore
    isoparse,
)
import logging
from paginator.pages import (
    PageId,
)
from returns.curry import (
    partial,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from singer_io.common import (
    JSON,
)
from tap_gitlab.api.auth import (
    Credentials,
)
from tap_gitlab.api.client import (
    ApiClient,
)
from tap_gitlab.api.projects import (
    ProjectApi,
)
from tap_gitlab.api.projects.ids import (
    ProjectId,
)
from tap_gitlab.api.projects.jobs import (
    JobManager,
)
from tap_gitlab.api.projects.jobs.objs import (
    JobId,
)
from tap_gitlab.api.projects.jobs.page import (
    JobsPage,
    Scope,
)

LOG = logging.getLogger(__name__)
NOW = datetime.now(timezone.utc)
# how old a job should be for considering it stuck
THRESHOLD = timedelta(days=1)


def _json_to_job(proj: ProjectId, raw: JSON) -> Maybe[JobId]:
    diff = NOW - isoparse(raw["created_at"])
    job = JobId(proj, str(raw["id"]))
    LOG.debug("%s with diff: %s", job, diff)
    if diff > THRESHOLD:
        return Maybe.from_value(job)
    return Maybe.empty


def _clean_stuck_jobs(data: JobsPage, manager: JobManager) -> IO[None]:
    matched_jobs = (
        m
        for m in map(
            lambda m: m.value_or(None),
            map(partial(_json_to_job, data.proj), data.data),
        )
        if m is not None
    )
    cancel_actions = map(manager.cancel, matched_jobs)
    deque(cancel_actions, maxlen=0)
    return IO(None)


def clean_stuck_jobs(api: ProjectApi, manager: JobManager) -> IO[None]:
    pages = api.jobs([Scope.created, Scope.pending, Scope.running]).list_all(
        PageId(1, 100)
    )
    pages.map(
        lambda p: [_clean_stuck_jobs(j, manager) for j in deque(p, maxlen=10)]
    )
    return IO(None)


def clean(creds: Credentials, proj: str, dry_run: bool) -> IO[None]:
    if dry_run:
        LOG.info("Dry run enabled!")
    client = ApiClient(creds)
    manager = JobManager(client.client, dry_run)
    proj_api = client.project(ProjectId.from_name(proj))
    return clean_stuck_jobs(proj_api, manager)
