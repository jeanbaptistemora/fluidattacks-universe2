# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import logging
import sys
from typing import (
    Any,
)

# Private constants
_FORMAT: str = "[%(levelname)s] %(message)s"

_LOGGER_FORMATTER: logging.Formatter = logging.Formatter(_FORMAT)

_LOGGER_HANDLER: logging.Handler = logging.StreamHandler(sys.stderr)
_LOGGER_HANDLER.setLevel(logging.INFO)
_LOGGER_HANDLER.setFormatter(_LOGGER_FORMATTER)

_LOGGER: logging.Logger = logging.getLogger("Reviews")
_LOGGER.setLevel(logging.INFO)
_LOGGER.addHandler(_LOGGER_HANDLER)


def set_level(level: int) -> None:
    _LOGGER.setLevel(level)
    _LOGGER_HANDLER.setLevel(level)


def log(level: str, msg: str, *args: Any) -> None:
    getattr(_LOGGER, level)(msg, *args)
