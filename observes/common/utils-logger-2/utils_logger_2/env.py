from enum import (
    Enum,
)
from fa_purity import (
    Cmd,
)
from os import (
    environ,
)


class Envs(Enum):
    PROD = "production"
    DEV = "development"


def current_app_env() -> Cmd[Envs]:
    def _action() -> Envs:
        return Envs(environ.get("OBSERVES_ENV", "production"))

    return Cmd.from_cmd(_action)


def observes_debug() -> Cmd[bool]:
    def _action() -> bool:
        _debug = environ.get("OBSERVES_DEBUG", "")
        return _debug.lower() == "true"

    return Cmd.from_cmd(_action)


def notifier_key() -> Cmd[str]:
    def _action() -> str:
        return environ.get("bugsnag_notifier_key", "")

    return Cmd.from_cmd(_action)
