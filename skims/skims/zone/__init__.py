from glob import (
    iglob,
)
from model import (
    core_model,
)
from ruamel import (
    yaml,
)
from typing import (
    Any,
    Dict,
    Optional,
)
from utils.ctx import (
    CTX,
    STATIC,
)


def load_translations() -> Dict[str, Dict[str, str]]:
    """Load the translations data from the static folder.

    :raises KeyError: On duplicated translations
    :return: A dictionary mapping keys to a dictionary mapping languages to
        translations
    :rtype: Dict[str, Dict[str, str]]
    """
    translations: Dict[str, Dict[str, str]] = {}
    translations_folder: str = f"{STATIC}/translations"
    for path in iglob(f"{translations_folder}/**/*.yaml", recursive=True):
        with open(path) as handle:
            for key, data in yaml.safe_load(handle).items():
                if key in translations:
                    raise KeyError(f"Found a duplicated translation: {key}")

                translations[key] = {
                    locale_code: data[locale_code.lower()]
                    for locale in core_model.LocalesEnum
                    for locale_code in [locale.value]
                }

    return translations


TRANSLATIONS: Dict[str, Dict[str, str]] = load_translations()

IGNORED_CHARS = str.maketrans(
    "",
    "",
    "".join(
        {
            "+",
            "^",
            "*",
            "~",
        }
    ),
)


def t(  # pylint: disable=invalid-name
    key: str,
    *args: Any,
    locale: Optional[core_model.LocalesEnum] = None,
    **kwargs: Any,
) -> str:
    return (
        TRANSLATIONS[key][(locale or CTX.config.language).value]
        .format(*args, **kwargs)
        .translate(IGNORED_CHARS)
    )
