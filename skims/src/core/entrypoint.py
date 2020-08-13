# Standard library
from asyncio import (
    all_tasks,
    create_task,
    get_event_loop,
    sleep,
    Task,
)
import logging
from os import (
    chdir,
    getcwd,
)
from os.path import (
    abspath,
)
from typing import (
    Dict,
)

# Third party imports
from aioextensions import (
    collect,
)
from confuse import (
    ConfigError,
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
from utils.logs import (
    log,
    log_exception,
    set_level,
)
from utils.model import (
    FindingEnum,
    SkimsConfig,
    VulnerabilityKindEnum,
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


async def execute_skims(config: SkimsConfig, token: str) -> bool:
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

    await collect((
        analyze_paths(
            paths_to_exclude=(
                config.path.exclude if config.path else ()
            ),
            paths_to_include=(
                config.path.include if config.path else ()
            ),
            stores=stores,
        ),
    ))

    await notify_findings(config, stores)

    if config.group and token:
        msg = 'Results will be synced to group: %s'
        await log('info', msg, config.group)

        success = await persist(
            group=config.group,
            results=tuple([
                result
                for store in stores.values()
                async for result in store.iterate()
            ]),
            token=token,
        )
    else:
        success = True
        await log('info', ' '.join((
            'In case you want to persist results to Integrates',
            'please make sure you set the --token flag in the CLI',
            'and the "group" key in the config file'
        )))

    return success


async def notify_findings(
    config: SkimsConfig,
    stores: Dict[FindingEnum, EphemeralStore],
) -> None:
    """Print user-friendly messages about the results found.

    :param config: Skims configuration object
    :type config: SkimsConfig
    :param stores: Results to be shown
    :type stores: Dict[FindingEnum, EphemeralStore]
    """

    async def dump(
        kind: VulnerabilityKindEnum,
        snippet: str,
        title: str,
        what: str,
        where: str,
    ) -> None:
        where = t(f'words.{kind.value[:-1]}') + ' ' + where

        if config.console_snippets:
            await log('info', '%s: %s\n\n%s\n', title, what, snippet)
        else:
            await log('info', '%s: %s, %s', title, what, where)

    for store in stores.values():
        async for result in store.iterate():
            if result.skims_metadata:
                await dump(
                    kind=result.kind,
                    snippet=result.skims_metadata.snippet,
                    title=t(result.finding.value.title),
                    what=result.what,
                    where=result.where,
                )


async def main(
    config: str,
    debug: bool,
    token: str,
) -> bool:
    monitor_task: Task[None] = create_task(monitor())

    if debug:
        get_event_loop().set_debug(True)
        set_level(logging.DEBUG)

    success: bool = True

    try:
        config_obj: SkimsConfig = await load(config)
        set_locale(config_obj.language)
        await reset_ephemeral_state()
        await adjust_working_dir(config_obj)
        success = await execute_skims(config_obj, token)
    except ConfigError as exc:
        await log('critical', '%s', exc)
        success = False
    except MemoryError:
        await log('critical', 'Not enough memory could be allocated')
        success = False
    except SystemExit as exc:
        await log_exception('critical', exc)
        success = False

    monitor_task.cancel()

    return success
