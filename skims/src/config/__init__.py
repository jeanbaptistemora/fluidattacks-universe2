# Standard library
from contextlib import (
    suppress,
)
from enum import (
    Enum,
)
from operator import (
    attrgetter,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
)

# Third party libraries
import hcl

# Local libraries
from utils.aio import (
    unblock_cpu,
)
from utils.fs import (
    get_file_content,
)
from utils.model import (
    LanguagesEnum,
    SkimsConfig,
    SkimsPathConfig,
)


class ConfigError(Exception):
    pass


def field_enum_required(*, field: str, value: Any, enum: Type[Enum]) -> Enum:
    if value:
        with suppress(AttributeError, TypeError, ValueError):
            return enum(value.upper())

        allowed_values: List[str] = list(map(
            attrgetter('value'),
            enum.__members__.values(),
        ))

        raise ConfigError(f'Field: {field}, must be one of: {allowed_values}')

    raise ConfigError(f'Field: {field} is required')


def load_path(resource_skims: Dict[str, Any]) -> Optional[SkimsPathConfig]:
    config: Optional[Any] = resource_skims.get('path', None)

    if isinstance(config, dict):
        for field in ('include', 'exclude'):
            if field not in config:
                raise ConfigError(f'Field: path.{field}, must be specified')

            if not isinstance(config[field], list):
                raise ConfigError(f'Field: path.{field}, must be a list')

        config = SkimsPathConfig(
            exclude=tuple(config['exclude']),
            include=tuple(config['include']),
        )
    elif config is None:
        pass
    else:
        raise ConfigError('Field: path, must be specified only once')

    return config


async def load(path: str) -> Tuple[SkimsConfig, ...]:
    configs: List[SkimsConfig] = []

    path_content: str = await get_file_content(path, encoding='utf-8')

    raw_config: Dict[str, Any] = await unblock_cpu(hcl.loads, path_content)
    raw_config_resources = raw_config.get('resource', {})
    raw_config_resources_skims = raw_config_resources.get('skims', {})

    for group, config in raw_config_resources_skims.items():
        configs.append(
            SkimsConfig(
                group=group,
                language=LanguagesEnum(
                    field_enum_required(
                        field='language',
                        value=config.get('language'),
                        enum=LanguagesEnum,
                    ),
                ),
                path=load_path(config),
            ),
        )

    return tuple(configs)
