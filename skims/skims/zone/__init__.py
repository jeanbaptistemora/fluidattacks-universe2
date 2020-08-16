# Standard library
from glob import (
    iglob,
)
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


def load_translations() -> Dict[str, Dict[str, str]]:
    """Load the translations data from the static folder.

    :raises KeyError: On duplicated translations
    :return: A dictionary mapping keys to a dictionary mapping languages to
        translations
    :rtype: Dict[str, Dict[str, str]]
    """
    translations: Dict[str, Dict[str, str]] = {}
    translations_folder: str = get_artifact('static/translations')
    for path in iglob(f'{translations_folder}/**/*.yaml', recursive=True):
        with open(path) as handle:
            for key, data in yaml.safe_load(handle).items():  # type: ignore
                if key in translations:
                    raise KeyError(f'Found a duplicated translation: {key}')

                translations[key] = {
                    locale_code: data[locale_code.lower()]
                    for locale in LocalesEnum
                    for locale_code in [locale.value]
                }

    return translations


TRANSLATIONS: Dict[str, Dict[str, str]] = load_translations()


def set_locale(locale: LocalesEnum) -> None:
    NAMESPACE.current_locale = locale.value


def t(key: str, **kwargs: Any) -> str:  # pylint: disable=invalid-name
    return TRANSLATIONS[key][NAMESPACE.current_locale].format(**kwargs)
