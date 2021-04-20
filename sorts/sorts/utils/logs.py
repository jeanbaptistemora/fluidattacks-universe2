# Standard libraries
import logging
import sys
from typing import (
    Any,
)

# Third-party libraries
import bugsnag
from mixpanel import Mixpanel

# Local libraries
from sorts.constants import (
    LOGGER,
    LOGGER_HANDLER,
    LOGGER_REMOTE,
    LOGGER_REMOTE_HANDLER,
    MIXPANEL_API_TOKEN_SORTS,
)
from sorts.utils.bugs import META as BUGS_META


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
    LOGGER_HANDLER.setStream(sys.stdout)
    LOGGER_HANDLER.setLevel(logging.INFO)
    LOGGER_HANDLER.setFormatter(CustomFormatter())

    LOGGER.setLevel(logging.INFO)
    LOGGER.addHandler(LOGGER_HANDLER)

    LOGGER_REMOTE_HANDLER.setLevel(logging.ERROR)

    LOGGER_REMOTE.setLevel(logging.ERROR)
    LOGGER_REMOTE.addHandler(LOGGER_REMOTE_HANDLER)


def set_level(level: int) -> None:
    LOGGER.setLevel(level)
    LOGGER_HANDLER.setLevel(level)


def log(level: str, msg: str, *args: Any) -> None:
    getattr(LOGGER, level)(msg, *args)


def log_to_remote_info(msg: str, **meta_data: str) -> None:
    log_to_remote(Exception(msg), severity='info', **meta_data)


def log_exception(
    level: str,
    exception: BaseException,
    **meta_data: str,
) -> None:
    exc_type: str = type(exception).__name__
    exc_msg: str = str(exception)
    log(level, 'Exception: %s, %s, %s', exc_type, exc_msg, meta_data)
    if level in ('warning', 'error', 'critical'):
        log_to_remote(exception, severity=level, **meta_data)


def log_to_remote(
    exception: BaseException,
    severity: str,
    **meta_data: str
) -> None:
    meta_data.update(BUGS_META.get() or {})
    bugsnag.notify(exception, meta_data=meta_data, severity=severity)


# Side effects
configure()


def mixpanel_track(email: str, event_name: str, **extra: str) -> None:
    Mixpanel(MIXPANEL_API_TOKEN_SORTS).track(email, event_name, {**extra})
