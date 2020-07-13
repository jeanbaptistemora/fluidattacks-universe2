import logging
from typing import Dict

import rollbar
from django.conf import settings

from backend.utils import aio


logging.config.dictConfig(settings.LOGGING)
LOGGER = logging.getLogger("log")


async def log(message: str, level: str, payload_data: Dict[str, str] = None,
              extra_data: Dict[str, str] = None) -> None:
    payload_data = payload_data or {}
    extra_data = extra_data or {}
    if settings.DEBUG:
        getattr(LOGGER, level, 'info')(message)
    await aio.ensure_io_bound(rollbar.report_message, message, level,
                              payload_data=payload_data, extra_data=extra_data)
