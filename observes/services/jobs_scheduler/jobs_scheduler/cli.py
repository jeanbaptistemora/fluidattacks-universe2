import click
from datetime import (
    datetime,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.cmd.transform import (
    serial_merge,
)
from fa_purity.utils import (
    raise_exception,
)
from jobs_scheduler.conf import (
    Jobs,
    new_job,
    SCHEDULE,
)
from jobs_scheduler.cron import (
    match,
)
from jobs_scheduler.run import (
    run_job as execute_job,
)
import logging
import pytz
from typing import (
    List,
    NoReturn,
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
) -> NoReturn:
    _now = datetime(
        NOW.year,
        month if month is not None else NOW.month,
        day if day is not None else NOW.day,
        hour if hour is not None else NOW.hour,
        NOW.minute,
        NOW.second,
        NOW.microsecond,
        NOW.tzinfo,
    )
    LOG.info("hour: %s", hour)
    LOG.info("Now: %s", _now)
    exe_jobs: List[Cmd[None]] = []
    for cron, jobs in SCHEDULE.items():
        LOG.debug("Evaluating %s.", cron)
        if match.match_cron(cron, _now):
            exe_jobs.extend(execute_job(job, dry_run) for job in jobs)
    serial_merge(tuple(exe_jobs)).compute()


@click.command()
@click.argument(
    "job", type=click.Choice([i.name for i in Jobs], case_sensitive=False)
)
@click.option("--dry-run", is_flag=True)
def run_job(job: str, dry_run: bool) -> NoReturn:
    execute_job(new_job(job).alt(raise_exception).unwrap(), dry_run).compute()


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(run_schedule)
main.add_command(run_job)
