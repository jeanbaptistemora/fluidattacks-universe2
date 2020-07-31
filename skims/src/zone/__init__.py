# Standard library
from enum import Enum
from typing import (
    Any,
    Dict,
    Callable,
)

# Third party libraries
from ruamel import yaml

# Local libraries
from utils.ctx import (
    get_artifact,
)


class LocalesEnum(Enum):
    EN: str = 'EN'
    ES: str = 'ES'


class _State():
    # pylint: disable=too-few-public-methods
    value: LocalesEnum = LocalesEnum.EN


def load_translations(path: str) -> Dict[str, Dict[LocalesEnum, str]]:
    with open(path) as handle:
        translations: Dict[str, Dict[LocalesEnum, str]] = {
            key: {
                locale: data[locale.value.lower()]
                for locale in LocalesEnum
            }
            for key, data in yaml.safe_load(handle).items()  # type: ignore
        }

    return translations


TRANSLATIONS: Dict[str, Dict[LocalesEnum, str]] = load_translations(
    get_artifact('static/translations.yaml'),
)


def lazy_t(key: str) -> Callable[[], str]:
    return lambda: t(key)


def set_locale(locale: LocalesEnum) -> None:
    _State.value = locale


def t(key: str, **kwargs: Any) -> str:  # pylint: disable=invalid-name
    return TRANSLATIONS[key][_State.value].format(**kwargs)
