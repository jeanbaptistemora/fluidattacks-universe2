from dataclasses import (
    dataclass,
)
import logging
from returns.io import (
    IO,
)
from tap_gitlab.api.projects.jobs.objs import (
    JobId,
)
from tap_gitlab.api.raw_client import (
    PageClient,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class JobManager:
    client: PageClient

    def cancel(self, job: JobId) -> IO[None]:
        url = f"/projects/{job.proj}/jobs/{job.item_id}/cancel"
        LOG.info("Cancelling job: %s", job)
        return self.client.get(url, {}).map(lambda _: None)
