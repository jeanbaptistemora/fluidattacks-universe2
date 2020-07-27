# Local libraries
import asyncio
import sys
from typing import (
    Tuple,
)

# Third party libraries
import click

# Local libraries
from core.entrypoint import (
    main,
)


@click.command(
    help='Deterministic vulnerability life-cycle reporting and closing tool.',
)
@click.option(
    '--debug',
    help='Enable debug mode.',
    is_flag=True,
)
@click.option(
    '--group',
    help='Integrates group where Skims will operate.',
)
@click.option(
    '--path',
    help=' '.join([
        'File or directory to analyze. Can be set many times.',
        'Directories are analyzed recursively.',
    ]),
    is_flag=False,
    multiple=True,
    type=click.Path(
        allow_dash=False,
        dir_okay=True,
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
    ),
)
@click.option(
    '--token',
    envvar='INTEGRATES_API_TOKEN',
    help='Integrates API token.',
    show_envvar=True,
)
def dispatch(
    debug: bool,
    group: str,
    path: Tuple[str, ...],
    token: str,
) -> None:
    success: bool = asyncio.run(
        main(
            debug=debug,
            group=group,
            paths=path,
            token=token,
        ),
        debug=debug,
    )

    sys.exit(0 if success else 1)
