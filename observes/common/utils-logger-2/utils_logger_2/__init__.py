from . import (
    handlers,
    logger,
)
from .env import (
    current_app_env,
)
from .levels import (
    LoggingLvl,
)
import bugsnag
from fa_purity import (
    Cmd,
)
import sys

__version__ = "1.0.1"


def set_main_log(
    name: str,
    conf: handlers.BugsnagConf,
    debug: bool,
    show_time: bool,
) -> Cmd[None]:
    _bug_handler = handlers.bug_handler(conf, LoggingLvl.ERROR)
    _log_handler = handlers.logger_handler(debug, show_time, sys.stderr)
    _handlers = (_log_handler, _bug_handler)
    env = current_app_env()
    display_env = logger.get_logger(name).bind(
        lambda log: env.bind(lambda e: log.info("%s@%s", (name, e.value)))
    )
    return (
        logger.set_logger(
            name, LoggingLvl.DEBUG if debug else LoggingLvl.INFO, _handlers
        )
        + display_env
    )


def start_session() -> Cmd[None]:
    def _action() -> None:
        bugsnag.start_session()  # type: ignore[no-untyped-call]

    return Cmd.from_cmd(_action)
