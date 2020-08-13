# Standard library
import logging
import sys
from typing import (
    Any,
)

# Third party libraries
from aioextensions import (
    unblock,
)

# Private constants
_FORMAT: str = '[%(levelname)s] %(message)s'

_LOGGER_FORMATTER: logging.Formatter = logging.Formatter(_FORMAT)

_LOGGER_HANDLER: logging.Handler = logging.StreamHandler(sys.stderr)
_LOGGER_HANDLER.setLevel(logging.INFO)
_LOGGER_HANDLER.setFormatter(_LOGGER_FORMATTER)

_LOGGER: logging.Logger = logging.getLogger('Skims')
_LOGGER.setLevel(logging.INFO)
_LOGGER.addHandler(_LOGGER_HANDLER)


def set_level(level: int) -> None:
    _LOGGER.setLevel(level)
    _LOGGER_HANDLER.setLevel(level)


async def log(level: str, msg: str, *args: Any) -> None:
    await unblock(getattr(_LOGGER, level), msg, *args)


async def log_exception(level: str, exception: BaseException) -> None:
    exc_type: str = type(exception).__name__
    exc_msg: str = str(exception)
    await log(level, 'Exception: %s, %s', exc_type, exc_msg)
