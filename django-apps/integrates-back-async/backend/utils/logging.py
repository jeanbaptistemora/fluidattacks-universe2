import logging

import rollbar
from django.conf import settings

from backend.utils import aio


logging.config.dictConfig(settings.LOGGING)
LOGGER = logging.getLogger("log")


async def log(message: str, level: str, **kwargs) -> None:
    request = kwargs.get('request')
    payload_data = kwargs.get('payload_data', {})
    extra_data = kwargs.get('extra_data', {})
    if settings.DEBUG:
        getattr(LOGGER, level, 'info')(
            f'{message}: payload_data: {payload_data}: '
            f'extra_data: {extra_data}'
        )
    else:
        await aio.ensure_io_bound(
            rollbar.report_message,
            message,
            level,
            request=request,
            payload_data=payload_data,
            extra_data=extra_data
        )
