# Standard library
import logging
import sys

# Private constants
_FORMAT: str = '[%(levelname)s] %(message)s'

_LOGGER_FORMATTER: logging.Formatter = logging.Formatter(_FORMAT)

_LOGGER_HANDLER: logging.Handler = logging.StreamHandler(sys.stderr)
_LOGGER_HANDLER.setFormatter(_LOGGER_FORMATTER)

LOGGER: logging.Logger = logging.getLogger('Streamer')
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(_LOGGER_HANDLER)
