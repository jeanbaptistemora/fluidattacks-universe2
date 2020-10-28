# Standard libraries
import logging
import sys
from typing import (
    Any,
)

# Private constantss
_LOGGER_HANDLER: logging.StreamHandler = logging.StreamHandler()
_LOGGER: logging.Logger = logging.getLogger('Sorts')


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


# Side effects
configure()
