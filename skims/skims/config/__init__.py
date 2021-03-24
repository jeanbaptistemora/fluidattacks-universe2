# Standard library
import os
from typing import (
    Any,
    Optional,
)

# Third party libraries
import confuse

# Local libraries
from model import (
    core_model,
)
from utils.logs import (
    log_blocking,
)


def load_path_lib_root(config_path: Any) -> core_model.SkimsConfigPathLibroot:
    if 'lib_root' in config_path:
        model = core_model.SkimsConfigPathLibroot(
            findings={
                getattr(core_model.FindingEnum, finding)
                for finding in config_path.pop('lib_root')
            },
        )
    else:
        model = core_model.SkimsConfigPathLibroot()

    return model


def load(group: Optional[str], path: str) -> core_model.SkimsConfig:
    template = confuse.Configuration('skims', read=False)
    template.set_file(path)
    template.read(user=False, defaults=False)

    config = template.get(
        confuse.Template({
            'language': confuse.Choice(core_model.LocalesEnum),
            'namespace': confuse.String(),
            'output': confuse.String(),
            'path': confuse.Template({
                'exclude': confuse.Sequence(confuse.String()),
                'include': confuse.Sequence(confuse.String()),
                'lib_path': confuse.OneOf([True, False], default=True),
                'lib_root': confuse.Sequence(confuse.String()),
            }),
            'timeout': confuse.Number(),
            'working_dir': confuse.String(),
        }),
    )

    try:
        config_path = config.pop('path')

        if output := config.pop('output', None):
            output = os.path.abspath(output)

        skims_config = core_model.SkimsConfig(
            group=group,
            language=core_model.LocalesEnum(config.pop('language', 'EN')),
            namespace=config.pop('namespace'),
            output=output,
            path=core_model.SkimsPathConfig(
                exclude=config_path.pop('exclude', ()),
                include=config_path.pop('include', ()),
                lib_path=config_path.pop('lib_path', True),
                lib_root=load_path_lib_root(config_path),
            ),
            start_dir=os.getcwd(),
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

    log_blocking('debug', '%s', skims_config)

    return skims_config
