# Standard library
from multiprocessing import (
    Manager,
)
from multiprocessing.managers import (
    SyncManager,
)
from os import (
    environ,
)
from os.path import (
    abspath,
    dirname,
    exists,
    join,
)
from typing import (
    Any,
    Optional,
)

# Constants
MANAGER: SyncManager = Manager()
CTX: Any = MANAGER.Namespace()
ROOT: str = abspath(dirname(dirname(dirname(__file__))))


def get_artifact(path: str, default: Optional[str] = None) -> str:
    for attempt in [
        abspath(join(ROOT, path)),
        abspath(join(ROOT, 'site-packages', path)),
    ]:
        if exists(attempt):
            return attempt

    if default:
        if value := environ.get(default):
            return value

    raise FileNotFoundError(path)


def read_artifact(path: str) -> bytes:
    with open(get_artifact(path), mode='rb') as file:
        return file.read()


# Side effects
CIPHER_SUITES_PATH: str = get_artifact(
    'static/cryptography/cipher_suites.csv',
    default='SKIMS_CIPHER_SUITES_PATH',
)
FLUID_WATERMARK = get_artifact(
    'static/img/logo_fluid_attacks_854x329.png',
    default='SKIMS_FLUID_WATERMARK',
)
PARSER_ANTLR: str = get_artifact(
    'static/parsers/antlr/build/install/parse/bin/parse',
    default='SKIMS_PARSER_ANTLR',
)
PARSER_BABEL: str = get_artifact(
    'static/parsers/babel',
    default='SKIMS_PARSER_BABEL',
)
ROBOTO_FONT = get_artifact(
    'vendor/fonts/roboto_mono_from_google/regular.ttf',
    default='SKIMS_ROBOTO_FONT',
)
STATIC = get_artifact('static', default='SKIMS_STATIC')
VENDOR = get_artifact('vendor', default='SKIMS_VENDOR')
