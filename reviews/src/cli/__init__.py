# Local libraries
import sys

# Third party libraries
import click

# Local libraries
from core import run_tests


@click.command()
@click.argument(
    'config_path',
    type=click.Path(exists=True)
)
def reviews(config_path: str) -> None:
    success: bool = True
    success = run_tests(config_path)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter, unexpected-keyword-arg
    reviews(
        prog_name='reviews',
    )
