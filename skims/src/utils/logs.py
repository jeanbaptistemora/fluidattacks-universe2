# Standard library
import logging
from typing import (
    Any,
)

# Private constants
_LOGGER_FORMAT: str = '[%(levelname)s] %(message)s'

_LOGGER_FORMATTER: logging.Formatter = logging.Formatter(_LOGGER_FORMAT)

_LOGGER_HANDLER: logging.Handler = logging.StreamHandler()
_LOGGER_HANDLER.setLevel(logging.INFO)
_LOGGER_HANDLER.setFormatter(_LOGGER_FORMATTER)

_LOGGER: logging.Logger = logging.getLogger('Skims')
_LOGGER.setLevel(logging.INFO)
_LOGGER.addHandler(_LOGGER_HANDLER)


def set_level_blocking(level: int = logging.INFO) -> None:
    _LOGGER.setLevel(level)
    _LOGGER_HANDLER.setLevel(level)


def log_blocking(level: str, msg: str, *args: Any) -> None:
    getattr(_LOGGER, level)(msg, *args)
