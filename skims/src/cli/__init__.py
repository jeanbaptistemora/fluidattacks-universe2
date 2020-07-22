# Local libraries
import asyncio
import logging
import sys
from typing import (
    Tuple,
)

# Third party libraries
import click

# Local libraries
from apis.integrates.graphql import (
    session,
)
from core.run import (
    skim_paths,
)
from core.model import (
    SkimResult,
)
from utils.logs import (
    log,
    set_level,
)
from utils.aio import (
    materialize,
)


@click.group()
@click.option(
    '--debug',
    help='Enable debug mode.',
    is_flag=True,
)
def dispatch(
    debug: bool,
) -> None:
    if debug:
        set_level(logging.DEBUG)


@dispatch.command(
    'run',
    help='Find deterministic vulnerabilities and prints a state to stdout.',
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
def dispatch_run(
    path: Tuple[str, ...],
) -> None:
    sys.exit(0 if asyncio.run(run(paths=path)) else 1)


@dispatch.command(
    'sync',
    help='Read the state from stdin and ensure it is mirrored to Integrates.',
)
@click.option(
    '--group',
    help='Integrates group where Skims will operate.',
)
@click.option(
    '--token',
    envvar='INTEGRATES_API_TOKEN',
    help='Integrates API token.',
    show_envvar=True,
)
def dispatch_sync(
    group: str,
    token: str,
) -> None:
    for argument in [
        'token',
        'group',
    ]:
        if not locals()[argument]:
            click.echo(f'Option: --{argument} is mandatory.')
            sys.exit(1)

    sys.exit(0 if asyncio.run(sync(group=group, token=token)) else 1)


async def run(*, paths: Tuple[str, ...]) -> bool:
    await log('debug', 'run(paths=%s)', paths)

    results: Tuple[SkimResult, ...] = tuple(*(await materialize((
        skim_paths(paths),
    ))))

    await materialize(log('info', '%s', result) for result in results)

    return True


async def sync(*, group: str, token: str) -> bool:
    await log('debug', 'sync(group=%s,token=%s)', group, token)

    async with session(
        api_token=token,
    ):
        pass

    return True


if __name__ == '__main__':
    # Disabling next line because @click modifies the function signature
    #   yet pylint is not able to see this modification
    dispatch()  # pylint: disable=no-value-for-parameter
