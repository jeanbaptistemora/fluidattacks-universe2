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


def _load(path: str) -> SkimsConfig:
    template = confuse.Configuration('skims', read=False)
    template.set_file(path)
    template.read(user=False, defaults=False)

    config = template.get(
        confuse.Template({
            'chdir': confuse.String(),
            'console_snippets': confuse.Choice((True, False)),
            'group': confuse.String(pattern=r'^[a-z0-9]+$'),
            'language': confuse.Choice(LocalesEnum),
            'path': confuse.Template({
                'exclude': confuse.Sequence(confuse.String()),
                'include': confuse.Sequence(confuse.String()),
            }),
        }),
    )

    try:
        config_path = config.pop('path', None)

        skims_config: SkimsConfig = SkimsConfig(
            chdir=config.pop('chdir', None),
            console_snippets=config.pop('console_snippets', True),
            group=config.pop('group', None),
            language=LocalesEnum(config.pop('language')),
            path=SkimsPathConfig(
                exclude=config_path.pop('exclude'),
                include=config_path.pop('include'),
            ) if config_path else None,
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


async def load(path: str) -> SkimsConfig:
    skims_config: SkimsConfig = await in_process(_load, path)

    await log('debug', '%s', skims_config)

    return skims_config
