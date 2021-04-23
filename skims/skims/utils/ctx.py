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
    makedirs,
)
from os.path import (
    expanduser,
)
from typing import (
    Any,
)

# Local libraries
from model import (
    core_model,
)

# Constants
MANAGER: SyncManager = Manager()
CTX: Any = MANAGER.Namespace()
STATE_FOLDER: str = expanduser("~/.skims")
STATE_FOLDER_DEBUG: str = os.path.join(STATE_FOLDER, "debug")


def _get_artifact(env_var: str) -> str:
    if value := environ.get(env_var):
        return value

    raise ValueError(f"Expected environment variable: {env_var}")


def create_test_context(debug: bool = True) -> None:
    CTX.debug = debug
    CTX.config = core_model.SkimsConfig(
        checks=set(core_model.FindingEnum),
        group=None,
        language=core_model.LocalesEnum.EN,
        namespace="test",
        output=None,
        http=core_model.SkimsHttpConfig(
            include=(),
        ),
        path=core_model.SkimsPathConfig(
            include=(),
            exclude=(),
            lib_path=True,
            lib_root=True,
        ),
        start_dir=os.getcwd(),
        timeout=None,
        working_dir=os.getcwd(),
    )


# Environment vars that change the execution
SHOULD_UPDATE_TESTS: bool = "SKIMS_SHOULD_UPDATE_TESTS" in os.environ

# Side effects
CIPHER_SUITES_PATH: str = _get_artifact("SKIMS_CIPHER_SUITES_PATH")
FLUID_WATERMARK = _get_artifact("SKIMS_FLUID_WATERMARK")
PARSER_ANTLR: str = _get_artifact("SKIMS_PARSER_ANTLR")
PARSER_BABEL: str = _get_artifact("SKIMS_PARSER_BABEL")
ROBOTO_FONT = _get_artifact("SKIMS_ROBOTO_FONT")
STATIC = _get_artifact("SKIMS_STATIC")
TREE_SITTER_JAVA = _get_artifact("SKIMS_TREE_SITTER_JAVA")
TREE_SITTER_TSX = _get_artifact("SKIMS_TREE_SITTER_TSX")
VENDOR = _get_artifact("SKIMS_VENDOR")

makedirs(STATE_FOLDER, mode=0o700, exist_ok=True)
makedirs(STATE_FOLDER_DEBUG, mode=0o700, exist_ok=True)
