from batch_stability import (
    report,
)
from batch_stability.jobs import (
    observes_jobs,
)
import click
from fa_purity.stream.transform import (
    consume,
)
from typing import (
    NoReturn,
)


@click.command()  # type: ignore[misc]
@click.argument("queue", type=str)
@click.option("--last-hours", type=int, default=24)
@click.option("--dry-run", is_flag=True)
def report_cancelled(queue: str, last_hours: int, dry_run: bool) -> NoReturn:
    jobs = observes_jobs(queue, last_hours)
    cmds = report.cancelled_jobs(jobs).map(lambda i: report.report(i, dry_run))
    cmds_2 = report.unstarted_jobs(jobs).map(
        lambda i: report.report(i, dry_run)
    )
    (consume(cmds) + consume(cmds_2)).compute()


@click.command()  # type: ignore[misc]
@click.argument("queue", type=str)
@click.option("--last-hours", type=int, default=1)
@click.option("--dry-run", is_flag=True)
def report_failures(queue: str, last_hours: int, dry_run: bool) -> NoReturn:
    jobs = observes_jobs(queue, last_hours)
    cmds = report.failed_jobs(jobs).map(lambda i: report.report(i, dry_run))
    consume(cmds).compute()


@click.group()  # type: ignore[misc]
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(report_cancelled)
main.add_command(report_failures)
