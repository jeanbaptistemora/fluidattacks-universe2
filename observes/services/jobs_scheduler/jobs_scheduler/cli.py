# pylint: skip-file

import click
from datetime import (
    datetime,
)
from jobs_scheduler.conf import (
    SCHEDULE,
)
from jobs_scheduler.cron_2 import (
    match,
)
from jobs_scheduler.run import (
    run_command,
)
import logging
import pytz  # type: ignore
from returns.io import (
    IO,
)

LOG = logging.getLogger(__name__)
tz = pytz.timezone("America/Bogota")
NOW = datetime.now(tz)


@click.command()
def run_schedule() -> IO[None]:
    LOG.info("Now: %s", NOW)
    for cron, jobs in SCHEDULE.items():
        LOG.debug("Evaluating %s.", cron)
        if match.match_cron(cron, NOW):
            for job in jobs:
                run_command(job.replace(".", "-").split())
    return IO(None)


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(run_schedule)
