import logging
from typing import Union

import bugsnag
from django.conf import settings


logging.config.dictConfig(settings.LOGGING)
LOGGER = logging.getLogger("log")


def log(message: Union[str, Exception], level: str, **kwargs) -> None:
    extra = kwargs.get('extra', {})
    if settings.DEBUG:
        getattr(LOGGER, level, 'info')(f'{message}: {extra}')
    else:
        bugsnag.notify(
            message if isinstance(message, Exception) else Exception(message),
            severity=level,
            meta_data={'extra': extra},
        )
