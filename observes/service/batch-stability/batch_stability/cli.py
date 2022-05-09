import batch_stability
from batch_stability import (
    default_queues,
)
import click


@click.command()
@click.argument("base-name", type=str)
@click.option("--last-hours", type=int, default=24)
def report_cancelled(base_name: str, last_hours: int) -> None:
    batch_stability.report_cancelled(default_queues(base_name), last_hours)


@click.command()
@click.argument("base-name", type=str)
@click.option("--last-hours", type=int, default=1)
def report_failures(base_name: str, last_hours: int) -> None:
    batch_stability.report_failures(default_queues(base_name), last_hours)


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(report_cancelled)
main.add_command(report_failures)
