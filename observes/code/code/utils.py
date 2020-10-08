# Standard library
import logging
from typing import (
    Any,
)

# Third party libraries
from aioextensions import (
    in_thread,
)

# Logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)
LOG.addHandler(logging.StreamHandler())
LOG.handlers[0].setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))


def log_sync(level: str, msg: str, *args: Any) -> None:
    getattr(LOG, level)(msg, *args)


async def log(level: str, msg: str, *args: Any) -> None:
    await in_thread(log_sync, level, msg, *args)
