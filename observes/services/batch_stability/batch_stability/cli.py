# Third party libraries
import click

# Local libraries
from batch_stability import report_default_queues


@click.command()
@click.argument("base-name", type=str)
@click.option("--last-hours", type=int, default=1)
def default_queues(base_name: str, last_hours: int) -> None:
    report_default_queues(base_name, last_hours)


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(default_queues)
