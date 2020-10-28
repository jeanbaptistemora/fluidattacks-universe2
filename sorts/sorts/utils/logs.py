# Standard libraries
import logging
import sys
from typing import (
    Any,
)

# Third-party libraries
import bugsnag

# Local libraries
from utils.bugs import META as BUGS_META


# Private constantss
_LOGGER_HANDLER: logging.StreamHandler = logging.StreamHandler()
_LOGGER: logging.Logger = logging.getLogger('Sorts')

_LOGGER_REMOTE_HANDLER = bugsnag.handlers.BugsnagHandler()
_LOGGER_REMOTE: logging.Logger = logging.getLogger('Sorts.stability')


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors"""

    grey: str = "\x1b[38;1m"
    yellow: str = "\x1b[33;1m"
    red: str = "\x1b[31;1m"
    bold_red: str = "\x1b[31;1m"
    reset: str = "\x1b[0m"
    msg_format: str = "[%(levelname)s] - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + msg_format + reset,
        logging.INFO: grey + msg_format + reset,
        logging.WARNING: yellow + msg_format + reset,
        logging.ERROR: red + msg_format + reset,
        logging.CRITICAL: bold_red + msg_format + reset
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def configure() -> None:
    _LOGGER_HANDLER.setStream(sys.stdout)
    _LOGGER_HANDLER.setLevel(logging.INFO)
    _LOGGER_HANDLER.setFormatter(CustomFormatter())

    _LOGGER.setLevel(logging.INFO)
    _LOGGER.addHandler(_LOGGER_HANDLER)

    _LOGGER_REMOTE_HANDLER.setLevel(logging.ERROR)

    _LOGGER_REMOTE.setLevel(logging.ERROR)
    _LOGGER_REMOTE.addHandler(_LOGGER_REMOTE_HANDLER)


def set_level(level: int) -> None:
    _LOGGER.setLevel(level)
    _LOGGER_HANDLER.setLevel(level)


def log(level: str, msg: str, *args: Any) -> None:
    getattr(_LOGGER, level)(msg, *args)


def log_exception(
    level: str,
    exception: BaseException,
    **meta_data: str,
) -> None:
    exc_type: str = type(exception).__name__
    exc_msg: str = str(exception)
    log(level, 'Exception: %s, %s, %s', exc_type, exc_msg, meta_data)
    if level in ('warning', 'error', 'critical'):
        log_to_remote(exception, **meta_data)


def log_to_remote(exception: BaseException, **meta_data: str) -> None:
    meta_data.update(BUGS_META.get() or {})
    bugsnag.notify(exception, meta_data=meta_data)


# Side effects
configure()
