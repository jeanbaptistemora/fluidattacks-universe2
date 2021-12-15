# pylint: skip-file

import click
from datetime import (
    datetime,
)
from jobs_scheduler.conf import (
    Jobs,
    SCHEDULE,
)
from jobs_scheduler.cron_2 import (
    match,
)
from jobs_scheduler.run import (
    run_job as execute_job,
)
import logging
import os
import pytz  # type: ignore
from returns.io import (
    IO,
)
from typing import (
    Optional,
)

LOG = logging.getLogger(__name__)
tz = pytz.timezone("America/Bogota")
NOW = datetime.now(tz)


@click.command()
@click.option("--month", type=int, default=None)
@click.option("--day", type=int, default=None)
@click.option("--hour", type=int, default=None)
@click.option("--dry-run", is_flag=True)
def run_schedule(
    month: Optional[int],
    day: Optional[int],
    hour: Optional[int],
    dry_run: bool,
) -> IO[None]:
    _now = datetime(
        NOW.year,
        month if month else NOW.month,
        day if day else NOW.day,
        hour if hour else NOW.hour,
        NOW.minute,
        NOW.second,
        NOW.microsecond,
        NOW.tzinfo,
    )
    LOG.info("Now: %s", _now)
    for cron, jobs in SCHEDULE.items():
        LOG.debug("Evaluating %s.", cron)
        if match.match_cron(cron, _now):
            for job in jobs:
                execute_job(job, dry_run)
    return IO(None)


@click.command()
@click.argument("job", type=str)
@click.option("--dry-run", is_flag=True)
def run_job(job: str, dry_run: bool) -> IO[None]:
    execute_job(Jobs[job], dry_run)
    return IO(None)


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(run_schedule)
main.add_command(run_job)
