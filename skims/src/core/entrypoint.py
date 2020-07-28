# Standard library
import logging
from typing import (
    Tuple,
)

# Local imports
from core.persist import (
    persist,
)
from lib_path import (
    analyze as analyze_paths,
)
from utils.aio import (
    materialize,
)
from utils.logs import (
    log,
    set_level,
)
from utils.model import (
    Vulnerability,
)


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
        analyze_paths(paths),
        # skimmers for other sources (--url, etc) go here
    ))))

    await materialize(
        log(
            'info', '%s: %s @ %s\n\n%s\n',
            result.finding.value,
            result.what,
            result.where,
            result.skims_metadata.snippet,
        )
        for result in results
        if result.skims_metadata
    )

    if all((group, token)):
        await log('info', 'Results will be synced to group: %s', group)

        success = await persist(group=group, results=results, token=token)
    else:
        await log('info', ' '.join((
            'In case you want to persist results to Integrates',
            'please make sure you set both the --group and --token flags',
        )))

    return success
