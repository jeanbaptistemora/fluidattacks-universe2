# Standard library
import os
from multiprocessing import (
    Manager,
)
from multiprocessing.managers import (
    SyncManager,
)
from os import (
    environ,
)
from typing import (
    Any,
)

# Local libraries
from utils.model import (
    LocalesEnum,
    SkimsConfig,
    SkimsPathConfig,
)

# Constants
MANAGER: SyncManager = Manager()
CTX: Any = MANAGER.Namespace()


def _get_artifact(env_var: str) -> str:
    if value := environ.get(env_var):
        return value

    raise ValueError(f'Expected environment variable: {env_var}')


def create_test_context(debug: bool = True) -> None:
    CTX.debug = debug
    CTX.config = SkimsConfig(
        group=None,
        language=LocalesEnum.EN,
        namespace='test',
        output=None,
        path=SkimsPathConfig(include=(), exclude=()),
        start_dir=os.getcwd(),
        timeout=None,
        working_dir=os.getcwd(),
    )


# Side effects
CIPHER_SUITES_PATH: str = _get_artifact('SKIMS_CIPHER_SUITES_PATH')
FLUID_WATERMARK = _get_artifact('SKIMS_FLUID_WATERMARK')
PARSER_ANTLR: str = _get_artifact('SKIMS_PARSER_ANTLR')
PARSER_BABEL: str = _get_artifact('SKIMS_PARSER_BABEL')
ROBOTO_FONT = _get_artifact('SKIMS_ROBOTO_FONT')
STATIC = _get_artifact('SKIMS_STATIC')
TREE_SITTER_JAVA = _get_artifact('SKIMS_TREE_SITTER_JAVA')
VENDOR = _get_artifact('SKIMS_VENDOR')
