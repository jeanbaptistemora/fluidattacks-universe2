import click
from core import (
    run,
)
import sys


@click.command()
@click.argument("config_path", type=click.Path(exists=True), nargs=1)
def reviews(config_path: str) -> None:
    success: bool = run(config_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    reviews(
        prog_name="reviews",
    )
