# Third party libraries
import confuse

# Local libraries
from utils.aio import (
    unblock_cpu,
)
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
            'group': confuse.String(pattern=r'^[a-z0-9]+$'),
            'language': confuse.Choice(LocalesEnum),
            'path': confuse.Template({
                'exclude': confuse.Sequence(confuse.Filename(cwd='')),
                'include': confuse.Sequence(confuse.Filename(cwd='')),
            }),
        }),
    )

    try:
        config_path = config.pop('path', None)

        skims_config: SkimsConfig = SkimsConfig(
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
    skims_config: SkimsConfig = await unblock_cpu(_load, path)

    await log('debug', '%s', skims_config)

    return skims_config
