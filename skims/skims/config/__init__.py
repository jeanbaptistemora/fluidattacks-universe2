# Standard library
import os
from typing import (
    Optional,
)

# Third party libraries
import confuse

# Third party libraries
from aioextensions import (
    in_process,
)

# Local libraries
from utils.model import (
    LocalesEnum,
    SkimsConfig,
    SkimsPathConfig,
)
from utils.logs import (
    log,
)


def _load(group: Optional[str], path: str) -> SkimsConfig:
    template = confuse.Configuration('skims', read=False)
    template.set_file(path)
    template.read(user=False, defaults=False)

    config = template.get(
        confuse.Template({
            'language': confuse.Choice(LocalesEnum),
            'output': confuse.String(),
            'path': confuse.Template({
                'exclude': confuse.Sequence(confuse.String()),
                'include': confuse.Sequence(confuse.String()),
            }),
            'timeout': confuse.Number(),
            'working_dir': confuse.String(),
        }),
    )

    try:
        config_path = config.pop('path', None)

        if output := config.pop('output', None):
            output = os.path.abspath(output)

        skims_config: SkimsConfig = SkimsConfig(
            group=group,
            language=LocalesEnum(config.pop('language', 'EN')),
            output=output,
            path=SkimsPathConfig(
                exclude=config_path.pop('exclude', []),
                include=config_path.pop('include'),
            ) if config_path else None,
            timeout=config.pop('timeout', None),
            working_dir=config.pop('working_dir', None),
        )
    except KeyError as exc:
        raise confuse.ConfigError(f'Key: {exc.args[0]} is required')
    else:
        if config:
            unrecognized_keys: str = ', '.join(config)
            raise confuse.ConfigError(
                f'Some keys were not recognized: {unrecognized_keys}',
            )

    return skims_config


async def load(group: Optional[str], path: str) -> SkimsConfig:
    skims_config: SkimsConfig = await in_process(_load, group, path)

    await log('debug', '%s', skims_config)

    return skims_config
