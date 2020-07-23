# Standard library
from itertools import chain
import logging
from typing import (
    Tuple,
)

# Local imports
from apis.integrates.graphql import (
    session,
)
from core.lib import (
    path_0038,
)
from model import (
    Vulnerability,
)
from utils.aio import (
    materialize,
)
from utils.fs import (
    recurse,
)
from utils.logs import (
    log,
    set_level,
)


async def skim_paths(paths: Tuple[str, ...]) -> Tuple[Vulnerability, ...]:
    files: Tuple[str, ...] = tuple(set(*(
        await materialize(map(recurse, paths))
    )))

    results: Tuple[Vulnerability, ...] = tuple(chain(*(
        await materialize(
            getattr(module, 'run')(file=file)
            for module in (
                path_0038,
            )
            for file in files
        )
    )))

    return results


async def persist(
    *,
    token: str,
) -> bool:
    success: bool = True

    async with session(api_token=token):
        pass

    return success


async def main(
    debug: bool,
    group: str,
    paths: Tuple[str, ...],
    token: str,
) -> bool:
    if debug:
        set_level(logging.DEBUG)

    success: bool = True

    results: Tuple[Vulnerability, ...] = tuple(*(await materialize((
        skim_paths(paths),
        # skimmers for other sources (--url, etc) go here
    ))))

    await materialize(log('info', '%s', result) for result in results)

    if all((group, token)):
        await log('info', 'Results will be synced to group: %s', group)

        success = await persist(token=token)
    else:
        await log('info', ' '.join((
            'In case you want to persist results to Integrates',
            'please make sure you set both the --group and --token flags',
        )))

    return success
