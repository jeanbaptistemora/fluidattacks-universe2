# Standard library
from asyncio import (
    all_tasks,
    create_task,
    get_event_loop,
    sleep,
    Task,
)
from itertools import (
    chain,
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
    Tuple,
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
from utils.logs import (
    log,
    set_level,
)
from utils.model import (
    SkimsConfig,
    Vulnerability,
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


async def notify_findings(
    config_obj: SkimsConfig,
    results: Tuple[Vulnerability, ...],
) -> None:

    async def dump(
        kind: VulnerabilityKindEnum,
        snippet: str,
        title: str,
        what: str,
        where: str,
    ) -> None:
        where = t(f'words.{kind.value[:-1]}') + ' ' + where

        if config_obj.console_snippets:
            await log('info', '%s: %s\n\n%s\n', title, what, snippet)
        else:
            await log('info', '%s: %s, %s', title, what, where)

    await collect(
        dump(
            kind=result.kind,
            snippet=result.skims_metadata.snippet,
            title=t(result.finding.value.title),
            what=result.what,
            where=result.where,
        )
        for result in results
        if result.skims_metadata
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
    except ConfigError as exc:
        await log('critical', '%s', exc)
        success = False
    else:
        try:
            await log('info', 'Startup working dir is: %s', getcwd())
            if config_obj.chdir is not None:
                newcwd: str = abspath(config_obj.chdir)
                await log('info', 'Moving working dir to: %s', newcwd)
                chdir(newcwd)

            set_locale(config_obj.language)

            results: Tuple[Vulnerability, ...] = tuple(chain.from_iterable(
                await collect((
                    analyze_paths(
                        paths_to_exclude=(
                            config_obj.path.exclude if config_obj.path else ()
                        ),
                        paths_to_include=(
                            config_obj.path.include if config_obj.path else ()
                        ),
                    ),
                ))
            ))

            await notify_findings(config_obj, results)

            if config_obj.group and token:
                msg = 'Results will be synced to group: %s'
                await log('info', msg, config_obj.group)

                success = await persist(
                    group=config_obj.group,
                    results=results,
                    token=token,
                )
            else:
                await log('info', ' '.join((
                    'In case you want to persist results to Integrates',
                    'please make sure you set the --token flag in the CLI',
                    'and the "group" key in the config file'
                )))
        except MemoryError:
            await log('critical', 'Not enough memory could be allocated')
            success = False
        except SystemExit:
            success = False

    monitor_task.cancel()

    return success
