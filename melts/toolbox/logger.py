# Standar imports
import logging
import sys

# Local imports
from toolbox import constants

# Constants
_FORMAT: str = '[%(levelname)s] %(message)s'
_LOGGER_FORMATTER: logging.Formatter = logging.Formatter(_FORMAT)
_LOGGER_HANDLER: logging.Handler = logging.StreamHandler(sys.stderr)

if constants.LOGGER_DEBUG:
    _LOGGER_HANDLER.setLevel(logging.DEBUG)
else:
    _LOGGER_HANDLER.setLevel(logging.INFO)

_LOGGER_HANDLER.setFormatter(_LOGGER_FORMATTER)
LOGGER: logging.Logger = logging.getLogger('forces')
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(_LOGGER_HANDLER)
