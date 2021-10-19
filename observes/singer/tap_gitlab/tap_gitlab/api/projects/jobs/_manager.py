from dataclasses import (
    dataclass,
)
from returns.io import (
    IO,
)
from tap_gitlab.api.projects.jobs.objs import (
    JobId,
)
from tap_gitlab.api.raw_client import (
    PageClient,
)


@dataclass(frozen=True)
class JobManager:
    client: PageClient

    def cancel(self, job: JobId) -> IO[None]:
        url = f"/projects/{job.proj}/jobs/{job.item_id}/cancel"
        return self.client.get(url, {}).map(lambda _: None)
