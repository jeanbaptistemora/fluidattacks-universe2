# Standard library
from typing import (
    Any,
    Dict,
)

# Third party libraries
from ruamel import yaml

# Local libraries
from utils.ctx import (
    get_artifact,
    NAMESPACE,
)
from utils.model import (
    LocalesEnum,
)


def load_translations(path: str) -> Dict[str, Dict[str, str]]:
    with open(path) as handle:
        translations: Dict[str, Dict[str, str]] = {
            key: {
                locale_code: data[locale_code.lower()]
                for locale in LocalesEnum
                for locale_code in [locale.value]
            }
            for key, data in yaml.safe_load(handle).items()  # type: ignore
        }

    return translations


TRANSLATIONS: Dict[str, Dict[str, str]] = load_translations(
    get_artifact('static/translations.yaml'),
)


def set_locale(locale: LocalesEnum) -> None:
    NAMESPACE.current_locale = locale.value


def t(key: str, **kwargs: Any) -> str:  # pylint: disable=invalid-name
    return TRANSLATIONS[key][NAMESPACE.current_locale].format(**kwargs)
