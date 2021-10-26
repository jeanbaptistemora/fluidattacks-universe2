# pylint: disable=consider-using-with
from aioextensions import (
    in_thread,
)
import bugsnag
from contextvars import (
    ContextVar,
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
import tempfile
from typing import (
    Any,
    IO,
)

# Private constants
LOG_FILE: ContextVar[IO[Any]] = ContextVar(
    "log_file", default=tempfile.NamedTemporaryFile()
)
# Console interface to show some special spinner symbols and logs
CONSOLE = Console(log_path=False, log_time=False, markup=True)

_FORMAT: str = "%(message)s"
logging.basicConfig(filename=LOG_FILE.get().name, format=_FORMAT)

_LOGGER_FORMATTER: logging.Formatter = logging.Formatter(_FORMAT)

_LOGGER_HANDLER: logging.Handler = RichHandler(
    show_time=False, markup=True, show_path=False
)
_LOGGER_HANDLER.setFormatter(_LOGGER_FORMATTER)

_LOGGER: logging.Logger = logging.getLogger("forces")
_LOGGER.setLevel(logging.INFO)
_LOGGER.addHandler(_LOGGER_HANDLER)


def blocking_log(level: str, msg: str, *args: Any) -> None:
    getattr(_LOGGER, level)(msg, *args)


async def log(level: str, msg: str, *args: Any) -> None:
    await in_thread(getattr(_LOGGER, level), msg, *args)


def spinner_log(msg: str, add_footer: bool = True) -> None:
    """Helper logger for spinner messages"""
    footer: str = ": [green]Complete[/]" if add_footer else ""
    CONSOLE.log(f"[blue]INFO[/]\t {msg}{footer}")


async def log_to_remote(
    exception: BaseException, **meta_data: str
) -> None:  # pragma: no cover
    meta_data.update(BUGS_META.get() or {})
    await in_thread(bugsnag.notify, exception, meta_data=meta_data)
