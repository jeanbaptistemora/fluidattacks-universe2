# Standard library
import logging
from typing import (
    Tuple,
)

# Third party imports
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
from utils.aio import (
    materialize,
)
from utils.logs import (
    log,
    set_level,
)
from utils.model import (
    SkimsConfig,
    Vulnerability,
)
from zone import (
    set_locale,
    t,
)


async def main(
    config: str,
    debug: bool,
    token: str,
) -> bool:
    if debug:
        set_level(logging.DEBUG)

    success: bool = True

    try:
        config_obj: SkimsConfig = await load(config)
    except ConfigError as exc:
        await log('critical', '%s', exc)
        success = False
    else:
        try:
            set_locale(config_obj.language)

            results: Tuple[Vulnerability, ...] = tuple(*await materialize((
                analyze_paths(
                    paths_to_exclude=(
                        config_obj.path.exclude if config_obj.path else ()
                    ),
                    paths_to_include=(
                        config_obj.path.include if config_obj.path else ()
                    ),
                ),
            )))

            await materialize(
                log(
                    'info', '%s: %s\n\n%s\n',
                    t(result.finding.value.title),
                    result.what,
                    result.skims_metadata.snippet,
                )
                for result in results
                if result.skims_metadata
            )

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
        except SystemExit:
            success = False

    return success
