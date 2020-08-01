# Standard libraries
import sys

# Third party libraries
import click

# Local libraries
from core.entrypoint import (
    main,
)
from utils.aio import (
    block,
)


@click.command(
    help='Deterministic vulnerability life-cycle reporting and closing tool.',
)
@click.argument(
    'config',
    type=click.Path(
        allow_dash=False,
        dir_okay=False,
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
    ),
)
@click.option(
    '--debug',
    help='Enable debug mode.',
    is_flag=True,
)
@click.option(
    '--token',
    envvar='INTEGRATES_API_TOKEN',
    help='Integrates API token.',
    show_envvar=True,
)
def dispatch(
    config: str,
    debug: bool,
    token: str,
) -> None:
    success: bool = block(
        main,
        config=config,
        debug=debug,
        token=token,
    )

    sys.exit(0 if success else 1)
