# Local libraries
import sys

# Third party libraries
import click

# Local libraries
from core.flavors import (
    generic,
)


@click.group(name='entrypoint')
def entrypoint() -> None:
    """Main comand line group."""


@entrypoint.command(
    'flavor',
)
@click.argument(
    'flavor_name',
    type=click.Choice(['generic']),
    default='generic'
)
def flavor_management(flavor_name: str) -> None:
    success: bool = True
    if 'generic' in flavor_name:
        success = generic()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    entrypoint()
