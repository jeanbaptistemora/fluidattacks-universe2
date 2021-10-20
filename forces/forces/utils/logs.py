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
import sys
import tempfile
from typing import (
    Any,
    IO,
)

# Private constants
LOG_FILE: ContextVar[IO[Any]] = ContextVar(
    "log_file", default=tempfile.NamedTemporaryFile()
)

_FORMAT: str = "# [%(levelname)s] %(message)s"
logging.basicConfig(filename=LOG_FILE.get().name, format=_FORMAT)

_LOGGER_FORMATTER: logging.Formatter = logging.Formatter(_FORMAT)

_LOGGER_HANDLER: logging.Handler = logging.StreamHandler(sys.stderr)
_LOGGER_HANDLER.setLevel(logging.INFO)
_LOGGER_HANDLER.setFormatter(_LOGGER_FORMATTER)

_LOGGER: logging.Logger = logging.getLogger("forces")
_LOGGER.setLevel(logging.INFO)
_LOGGER.addHandler(_LOGGER_HANDLER)


def blocking_log(level: str, msg: str, *args: Any) -> None:
    getattr(_LOGGER, level)(msg, *args)


async def log(level: str, msg: str, *args: Any) -> None:
    await in_thread(getattr(_LOGGER, level), msg, *args)


async def log_to_remote(
    exception: BaseException, **meta_data: str
) -> None:  # pragma: no cover
    meta_data.update(BUGS_META.get() or {})
    await in_thread(bugsnag.notify, exception, meta_data=meta_data)
