# Local libraries
import asyncio
import sys
from typing import (
    Tuple,
)

# Third party libraries
import click

# Local libraries
from core.skimers.path import (
    skim as skim_path,
)


@click.command()
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
def dispatch(path: Tuple[str, ...]) -> None:
    sys.exit(0 if asyncio.run(run(paths=path)) else 1)


async def run(*, paths: Tuple[str, ...]) -> bool:
    return all(
        await asyncio.gather(
            *tuple(map(skim_path, paths)),
        )
    )


if __name__ == '__main__':
    # Disabling next line because @click modifies the function signature
    #   yet pylint is not able to see this modification
    dispatch()  # pylint: disable=no-value-for-parameter
