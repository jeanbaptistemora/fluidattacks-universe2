# Standard library
import logging
import sys
import tempfile
from typing import (
    Any,
    IO,
)
from contextvars import ContextVar

# Third libraries
import bugsnag

# Local libraries
from forces.utils.aio import (
    unblock,
)

# Private constants
LOG_FILE: ContextVar[IO[Any]] = ContextVar(
    'log_file', default=tempfile.NamedTemporaryFile())

_FORMAT: str = '# [%(levelname)s] %(message)s'
logging.basicConfig(filename=LOG_FILE.get().name,
                    format=_FORMAT)

_LOGGER_FORMATTER: logging.Formatter = logging.Formatter(_FORMAT)

_LOGGER_HANDLER: logging.Handler = logging.StreamHandler(sys.stderr)
_LOGGER_HANDLER.setLevel(logging.INFO)
_LOGGER_HANDLER.setFormatter(_LOGGER_FORMATTER)

_LOGGER: logging.Logger = logging.getLogger('forces')
_LOGGER.setLevel(logging.INFO)
_LOGGER.addHandler(_LOGGER_HANDLER)


def set_level(level: int) -> None:
    _LOGGER.setLevel(level)
    _LOGGER_HANDLER.setLevel(level)


async def log(level: str, msg: str, *args: Any) -> None:
    await unblock(getattr(_LOGGER, level), msg, *args)


async def log_to_remote(exception: BaseException) -> None:
    await unblock(bugsnag.notify, exception)
