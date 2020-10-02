# Standard libraries
import logging
import sys
from typing import (
    Any,
)

# Third party libraries
from aioextensions import (
    in_thread,
)

# Private constants
_FORMAT: str = '[%(levelname)s] %(message)s'

_LOGGER_FORMATTER: logging.Formatter = logging.Formatter(_FORMAT)

_LOGGER_HANDLER: logging.StreamHandler = logging.StreamHandler()
_LOGGER: logging.Logger = logging.getLogger('Sorts')


def configure() -> None:
    _LOGGER_HANDLER.setStream(sys.stdout)
    _LOGGER_HANDLER.setLevel(logging.INFO)
    _LOGGER_HANDLER.setFormatter(_LOGGER_FORMATTER)

    _LOGGER.setLevel(logging.INFO)
    _LOGGER.addHandler(_LOGGER_HANDLER)


def set_level(level: int) -> None:
    _LOGGER.setLevel(level)
    _LOGGER_HANDLER.setLevel(level)


def blocking_log(level: str, msg: str, *args: Any) -> None:
    getattr(_LOGGER, level)(msg, *args)


async def log(level: str, msg: str, *args: Any) -> None:
    await in_thread(blocking_log, level, msg, *args)


async def log_exception(
    level: str,
    exception: BaseException,
    **meta_data: str,
) -> None:
    exc_type: str = type(exception).__name__
    exc_msg: str = str(exception)
    await log(level, 'Exception: %s, %s, %s', exc_type, exc_msg, meta_data)


# Side effects
configure()
