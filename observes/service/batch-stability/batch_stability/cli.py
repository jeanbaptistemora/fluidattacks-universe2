from batch_stability import (
    jobs,
)
from batch_stability.jobs import (
    Product,
)
import click
from typing import (
    NoReturn,
)

product_choice = click.Choice([i.value for i in Product], case_sensitive=False)


@click.command()  # type: ignore[misc]
@click.argument("product", type=product_choice)
@click.option("--last-hours", type=int, default=24)
@click.option("--dry-run", is_flag=True)
def report_cancelled(product: str, last_hours: int, dry_run: bool) -> NoReturn:
    jobs.report_cancelled(Product(product), last_hours, dry_run).compute()


@click.command()  # type: ignore[misc]
@click.argument("product", type=product_choice)
@click.option("--last-hours", type=int, default=1)
@click.option("--dry-run", is_flag=True)
def report_failures(product: str, last_hours: int, dry_run: bool) -> NoReturn:
    jobs.report_failures(Product(product), last_hours, dry_run).compute()


@click.group()  # type: ignore[misc]
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(report_cancelled)
main.add_command(report_failures)
