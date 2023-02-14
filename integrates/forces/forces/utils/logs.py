# pylint: disable=consider-using-with
from aioextensions import (
    in_thread,
)
import bugsnag
from collections.abc import (
    Set,
)
from contextvars import (
    ContextVar,
)
from enum import (
    StrEnum,
)
from forces.utils.bugs import (
    META as BUGS_META,
)
import logging
from rich.console import (
    Console,
)
from rich.logging import (
    RichHandler,
)
from rich.table import (
    Table,
)
from rich.text import (
    Text,
)
import tempfile
from typing import (
    Any,
    IO,
)


class LogInterface(StrEnum):
    ALL = "ALL"
    CONSOLE = "CONSOLE"
    LOGGER = "LOGGER"


# Private constants, text mode required for Rich logging
LOG_FILE: ContextVar[IO[Any]] = ContextVar(
    "log_file", default=tempfile.NamedTemporaryFile(mode="w+t")
)
# Console interface to show logs and special spinner symbols on stdout
CONSOLE_INTERFACE = Console(
    log_path=False, log_time=False, markup=True, width=80
)
# Logging interface to get around the Rich library writing limitations
LOGGING_INTERFACE = Console(
    force_terminal=True,
    file=LOG_FILE.get(),
    log_path=False,
    log_time=False,
    markup=True,
    width=80,
)

_FORMAT: str = "%(message)s"
logging.basicConfig(format=_FORMAT)

_LOGGER_FORMATTER: logging.Formatter = logging.Formatter(_FORMAT)

_LOGGER: logging.Logger = logging.getLogger("forces")
_LOGGER.setLevel(logging.INFO)
_LOGGER.propagate = False


def set_up_handlers(interfaces: Set[Console]) -> None:
    """Configures and sets up logging handlers for the main logger object"""
    for interface in interfaces:
        handler: logging.Handler = RichHandler(
            show_time=False, markup=True, show_path=False, console=interface
        )
        handler.setFormatter(_LOGGER_FORMATTER)
        _LOGGER.addHandler(handler)


# A rich console can only write to either stdout or the provided file, not both
set_up_handlers({CONSOLE_INTERFACE, LOGGING_INTERFACE})


def blocking_log(level: str, msg: str, *args: object) -> None:
    getattr(_LOGGER, level)(msg, *args)


async def log(level: str, msg: str, *args: object) -> None:
    await in_thread(getattr(_LOGGER, level), msg, *args)


def rich_log(
    rich_msg: Table | Text | str, log_to: LogInterface = LogInterface.ALL
) -> None:
    """Writes to the specified console interfaces to have either stdout and log
    output"""
    if log_to in [LogInterface.ALL, LogInterface.CONSOLE]:
        CONSOLE_INTERFACE.log(rich_msg)
    if log_to in [LogInterface.ALL, LogInterface.LOGGER]:
        LOGGING_INTERFACE.log(rich_msg)


def log_banner(banner: str) -> None:
    """Special method to log the banner to be shown in ARM logs"""
    LOGGING_INTERFACE.rule(banner)


async def log_to_remote(
    exception: BaseException, **meta_data: str
) -> None:  # pragma: no cover
    meta_data.update(BUGS_META.get() or {})
    await in_thread(bugsnag.notify, exception, meta_data=meta_data)
