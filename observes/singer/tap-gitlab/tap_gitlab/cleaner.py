# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from datetime import (
    datetime,
    timedelta,
    timezone,
)
from fa_purity import (
    Cmd,
)
from fa_purity.stream.transform import (
    consume,
)
import logging
from tap_gitlab.api2.job import (
    Job,
    JobObj,
    JobStatus,
)
from tap_gitlab.api2.project.jobs import (
    JobClient,
)

LOG = logging.getLogger(__name__)
NOW = datetime.now(timezone.utc)


def clean_stuck_jobs(
    client: JobClient, start_page: int, threshold: timedelta, dry_run: bool
) -> Cmd[None]:
    # threshold: how old a job should be for considering it stuck
    def is_stuck(job: Job) -> bool:
        diff = NOW - job.dates.created_at
        return diff > threshold

    status = frozenset(
        [JobStatus.created, JobStatus.pending, JobStatus.running]
    )
    stuck_jobs = client.job_stream(start_page, 100, status).filter(
        lambda j: is_stuck(j.job)
    )

    def cancel_cmd(job: JobObj) -> Cmd[None]:
        diff = NOW - job.job.dates.created_at
        if dry_run:
            return Cmd.from_cmd(
                lambda: LOG.info(
                    "%s will be cancelled. diff=%s", job.job_id, diff
                )
            )
        return client.cancel(job.job_id)

    return stuck_jobs.map(lambda j: cancel_cmd(j)).transform(
        lambda s: consume(s)
    )
