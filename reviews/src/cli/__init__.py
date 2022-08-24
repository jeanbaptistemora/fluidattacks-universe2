import click
from core import (
    run_tests,
)
import sys
from utils.logs import (
    log,
)


@click.command()
@click.option(
    "--legacy/--no-legacy", default=True, help="Run in legacy or new mode"
)
@click.argument("config_path", type=click.Path(exists=True), nargs=1)
def reviews(legacy: bool, config_path: str) -> None:
    success: bool = False
    if legacy:
        success = run_tests(config_path)
    else:
        success = True
        log("info", "Work in progress")
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter, unexpected-keyword-arg
    reviews(
        prog_name="reviews",
    )
