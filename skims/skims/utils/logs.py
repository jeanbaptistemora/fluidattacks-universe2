from aioextensions import (
    in_thread,
)
import bugsnag
import logging
import sys
from typing import (
    Any,
)
from utils.bugs import (
    META as BUGS_META,
)

# Private constants
_FORMAT: str = "[%(levelname)s] %(message)s"

_LOGGER_FORMATTER: logging.Formatter = logging.Formatter(_FORMAT)

_LOGGER_HANDLER: logging.StreamHandler = logging.StreamHandler()
_LOGGER: logging.Logger = logging.getLogger("Skims")

_LOGGER_REMOTE_HANDLER = bugsnag.handlers.BugsnagHandler()
_LOGGER_REMOTE: logging.Logger = logging.getLogger("Skims.stability")


def configure() -> None:
    _LOGGER_HANDLER.setStream(sys.stdout)
    _LOGGER_HANDLER.setLevel(logging.INFO)
    _LOGGER_HANDLER.setFormatter(_LOGGER_FORMATTER)

    _LOGGER.setLevel(logging.INFO)
    _LOGGER.addHandler(_LOGGER_HANDLER)

    _LOGGER_REMOTE_HANDLER.setLevel(logging.ERROR)

    _LOGGER_REMOTE.setLevel(logging.ERROR)
    _LOGGER_REMOTE.addHandler(_LOGGER_REMOTE_HANDLER)


def set_level(level: int) -> None:
    _LOGGER.setLevel(level)
    _LOGGER_HANDLER.setLevel(level)


def log_blocking(level: str, msg: str, *args: Any, **kwargs: Any) -> None:
    getattr(_LOGGER, level)(msg, *args, **kwargs)


async def log(level: str, msg: str, *args: Any, **kwargs: Any) -> None:
    await in_thread(log_blocking, level, msg, *args, **kwargs)


def log_exception_blocking(
    level: str,
    exception: BaseException,
    **meta_data: str,
) -> None:
    exc_type: str = type(exception).__name__
    exc_msg: str = str(exception)
    log_blocking(level, "Exception: %s, %s, %s", exc_type, exc_msg, meta_data)


async def log_exception(
    level: str,
    exception: BaseException,
    **meta_data: str,
) -> None:
    await in_thread(log_exception_blocking, level, exception, **meta_data)


def log_to_remote_blocking(
    *,
    msg: str,
    severity: str,  # info, error, warning
    **meta_data: str,
) -> None:
    meta_data.update(BUGS_META)
    bugsnag.notify(
        Exception(msg), meta_data=dict(meta_data), severity=severity
    )


async def log_to_remote(
    *,
    msg: str,
    severity: str,  # info, error, warning
    **meta_data: str,
) -> None:
    await in_thread(
        log_to_remote_blocking,
        msg,
        severity=severity,
        **meta_data,
    )


# Side effects
configure()
