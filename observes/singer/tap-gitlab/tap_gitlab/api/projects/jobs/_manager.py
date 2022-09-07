# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
    dry_run: bool

    def cancel(self, job: JobId) -> IO[None]:
        url = f"/projects/{job.proj}/jobs/{job.item_id}/cancel"
        if not self.dry_run:
            LOG.info("Canceling job: %s", job)
            return self.client.get(url, {}).map(lambda _: None)
        LOG.info("%s will be canceled", job)
        return IO(None)
