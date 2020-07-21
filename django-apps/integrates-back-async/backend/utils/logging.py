import logging
from typing import Union

import bugsnag
from django.conf import settings

from backend.utils import aio


logging.config.dictConfig(settings.LOGGING)
LOGGER = logging.getLogger("log")


async def log(message: Union[str, Exception], level: str, **kwargs) -> None:
    extra = kwargs.get('extra', {})
    if settings.DEBUG:
        getattr(LOGGER, level, 'info')(f'{message}: {extra}')
    else:
        await aio.ensure_io_bound(
            bugsnag.notify,
            message if isinstance(message, Exception) else Exception(message),
            severity=level,
            meta_data={'extra': extra},
        )
