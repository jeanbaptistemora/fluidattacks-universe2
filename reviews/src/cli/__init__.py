# Local libraries
import sys

# Third party libraries
import click
from dynaconf import Dynaconf

# Local libraries
from config import load
from core import run_tests


@click.command()
@click.argument(
    'config_path',
    type=click.Path(exists=True)
)
def reviews(config_path: str) -> None:
    success: bool = True
    config: Dynaconf = load(config_path)
    success = run_tests(config)

    sys.exit(0 if success else 1)
