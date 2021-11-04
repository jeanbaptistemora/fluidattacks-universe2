from multiprocessing import (
    Manager,
)
from multiprocessing.managers import (
    SyncManager,
)
import os
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

# Constants
MANAGER: SyncManager = Manager()
CTX: Any = MANAGER.Namespace()
STATE_FOLDER: str = expanduser("~/.skims")
STATE_FOLDER_DEBUG: str = os.path.join(STATE_FOLDER, "debug")


def _get_artifact(env_var: str) -> str:
    if value := environ.get(env_var):
        return value

    raise ValueError(f"Expected environment variable: {env_var}")


# Side effects
CIPHER_SUITES_PATH: str = _get_artifact("SKIMS_CIPHER_SUITES_PATH")
CRITERIA_REQUIREMENTS: str = _get_artifact("SKIMS_CRITERIA_REQUIREMENTS")
CRITERIA_VULNERABILITIES: str = _get_artifact("SKIMS_CRITERIA_VULNERABILITIES")
FLUID_WATERMARK = _get_artifact("SKIMS_FLUID_WATERMARK")
ROBOTO_FONT = _get_artifact("SKIMS_ROBOTO_FONT")
STATIC = _get_artifact("SKIMS_STATIC")
TOOLS_SEMVER_MATCH = _get_artifact("SKIMS_TOOLS_SEMVER_MATCH")
TREE_SITTER_PARSERS = _get_artifact("SKIMS_TREE_SITTER_PARSERS")
VENDOR = _get_artifact("SKIMS_VENDOR")

makedirs(STATE_FOLDER, mode=0o700, exist_ok=True)
makedirs(STATE_FOLDER_DEBUG, mode=0o700, exist_ok=True)
