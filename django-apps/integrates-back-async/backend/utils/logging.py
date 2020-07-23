import logging
from typing import Union

import bugsnag
from django.conf import settings


LOGGER = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class SpecificLevelFilter(logging.Filter):
    def __init__(self, level):
        self.level = level
        super(SpecificLevelFilter, self).__init__()

    def filter(self, record):
        return record.levelno == self.level


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
