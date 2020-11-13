# Standard library
from asyncio import (
    all_tasks,
    create_task,
    sleep,
    Task,
    wait_for,
)
import csv
import logging
from os import (
    chdir,
    getcwd,
)
from os.path import (
    abspath,
)
import sys
from typing import (
    Dict,
    Optional,
)

# Third party imports
from aioextensions import (
    collect,
)

# Local imports
from config import (
    load,
)
from core.persist import (
    persist,
)
from lib_path.analyze import (
    analyze as analyze_paths,
)
from state.ephemeral import (
    EphemeralStore,
    get_ephemeral_store,
    reset as reset_ephemeral_state,
)
from utils.hardware import (
    get_max_memory_usage,
)
from utils.logs import (
    log,
    set_level,
)
from utils.model import (
    FindingEnum,
    SkimsConfig,
)
from zone import (
    set_locale,
    t,
)


async def monitor() -> None:
    while await sleep(10.0, result=True):
        tasks: int = len(all_tasks())
        await log('info', 'Still running, %s tasks pending to finish', tasks)


async def adjust_working_dir(config: SkimsConfig) -> None:
    """Move the skims working directory to the one the user wants.

    :param config: Skims configuration object
    :type config: SkimsConfig
    """
    await log('info', 'Startup working dir is: %s', getcwd())
    if config.chdir is not None:
        newcwd: str = abspath(config.chdir)
        await log('info', 'Moving working dir to: %s', newcwd)
        chdir(newcwd)


async def execute_skims(config: SkimsConfig, token: Optional[str]) -> bool:
    """Execute skims according to the provided config.

    :param config: Skims configuration object
    :type config: SkimsConfig
    :param token: Integrates API token
    :type token: str
    :raises MemoryError: If not enough memory can be allocated by the runtime
    :raises SystemExit: If any critical error occurs
    :return: A boolean indicating success
    :rtype: bool
    """
    success: bool = True

    stores: Dict[FindingEnum, EphemeralStore] = {
        finding: get_ephemeral_store() for finding in FindingEnum
    }

    await wait_for(
        collect((
            analyze_paths(
                paths_to_exclude=(
                    config.path.exclude if config.path else ()
                ),
                paths_to_include=(
                    config.path.include if config.path else ()
                ),
                stores=stores,
            ),
        )),
        config.timeout,
    )

    if config.output:
        await notify_findings_as_csv(stores, config.output)
    else:
        await notify_findings_as_snippets(stores)

    if config.group and token:
        msg = 'Results will be synced to group: %s'
        await log('info', msg, config.group)

        success = await persist(
            group=config.group,
            stores=stores,
            token=token,
        )
    else:
        success = True
        await log('info', ' '.join((
            'In case you want to persist results to Integrates',
            'please make sure you set the --token and --group flag in the CLI',
        )))

    return success


async def notify_findings_as_snippets(
    stores: Dict[FindingEnum, EphemeralStore],
) -> None:
    """Print user-friendly messages about the results found."""
    for store in stores.values():
        async for result in store.iterate():
            if result.skims_metadata:
                await log(
                    'info', '{title}: {what}\n\n{snippet}\n'.format(
                        title=t(result.finding.value.title),
                        what=result.what,
                        snippet=result.skims_metadata.snippet,
                    ))


async def notify_findings_as_csv(
    stores: Dict[FindingEnum, EphemeralStore],
    output: str,
) -> None:
    headers = ('cwe', 'title', 'what', 'where')
    rows = [
        {
            'cwe': ' + '.join(sorted(result.skims_metadata.cwe)),
            'title': t(result.finding.value.title),
            'what': result.what,
            'where': result.where,
        }
        for store in stores.values()
        async for result in store.iterate()
        if result.skims_metadata
    ]

    with open(output, 'w') as file:
        writer = csv.DictWriter(file, headers, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(sorted(rows, key=str))

    await log('info', 'An output file has been written: %s', abspath(output))


async def main(
    config: str,
    debug: bool,
    group: Optional[str],
    token: Optional[str],
) -> bool:
    # Increase the level of recursion because some functions must iterate
    # through very large trees
    sys.setrecursionlimit(10000)

    monitor_task: Task[None] = create_task(monitor())

    if debug:
        set_level(logging.DEBUG)

    try:
        config_obj: SkimsConfig = await load(group, config)
        set_locale(config_obj.language)
        await reset_ephemeral_state()
        await adjust_working_dir(config_obj)
        return await execute_skims(config_obj, token)
    finally:
        await reset_ephemeral_state()
        await log('info', 'Max memory usage: %s GB', get_max_memory_usage())
        monitor_task.cancel()
