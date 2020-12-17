# Standard library
import os
from typing import (
    Optional,
)

# Third party libraries
import confuse

# Local libraries
from utils.model import (
    LocalesEnum,
    SkimsConfig,
    SkimsPathConfig,
)
from utils.logs import (
    blocking_log,
)


def load(group: Optional[str], path: str) -> SkimsConfig:
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
                'namespace': confuse.String(),
            }),
            'timeout': confuse.Number(),
            'working_dir': confuse.String(),
        }),
    )

    try:
        config_path = config.pop('path')

        if output := config.pop('output', None):
            output = os.path.abspath(output)

        skims_config: SkimsConfig = SkimsConfig(
            group=group,
            language=LocalesEnum(config.pop('language', 'EN')),
            namespace=config.pop('namespace'),
            output=output,
            path=SkimsPathConfig(
                exclude=config_path.pop('exclude', ()),
                include=config_path.pop('include', ()),
            ),
            timeout=config.pop('timeout', None),
            working_dir=os.path.abspath(config.pop('working_dir', '.')),
        )
    except KeyError as exc:
        raise confuse.ConfigError(f'Key: {exc.args[0]} is required')
    else:
        if config:
            unrecognized_keys: str = ', '.join(config)
            raise confuse.ConfigError(
                f'Some keys were not recognized: {unrecognized_keys}',
            )

    blocking_log('debug', '%s', skims_config)

    return skims_config
