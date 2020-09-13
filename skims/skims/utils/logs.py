# Standard library
import logging
import sys
from typing import (
    Any,
)

# Third party libraries
from aioextensions import (
    in_thread,
)
import bugsnag

# Local libraries
from utils.bugs import (
    META as BUGS_META,
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

_LOGGER_REMOTE_HANDLER = bugsnag.handlers.BugsnagHandler()
_LOGGER_REMOTE_HANDLER.setLevel(logging.ERROR)

_LOGGER_REMOTE: logging.Logger = logging.getLogger('Skims.stability')
_LOGGER_REMOTE.setLevel(logging.ERROR)
_LOGGER_REMOTE.addHandler(_LOGGER_REMOTE_HANDLER)  # Sorry sir event-loop


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
    if level in ('warning', 'error', 'critical'):
        await log_to_remote(exception, **meta_data)


async def log_to_remote(exception: BaseException, **meta_data: str) -> None:
    meta_data.update(BUGS_META.get() or {})
    await in_thread(bugsnag.notify, exception, meta_data=meta_data)
