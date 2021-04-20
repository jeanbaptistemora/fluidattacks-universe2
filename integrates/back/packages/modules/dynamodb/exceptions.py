# Standard
import logging
import logging.config
import sys
from typing import Optional

# Third party
from botocore.exceptions import ClientError

# Local
from back.settings import LOGGING


# Constants
logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


class ConditionalCheckFailedException(Exception):
    pass


class UnavailabilityError(Exception):
    def __init__(self) -> None:
        msg = 'Service unavalible, please retry'
        super(UnavailabilityError, self).__init__(msg)


def handle_error(*, error: ClientError) -> None:
    code: str = error.response['Error']['Code']
    custom_exception: Optional[Exception] = getattr(
        sys.modules[__name__],
        code,
        None
    )

    if custom_exception:
        raise custom_exception

    LOGGER.exception(error)
    raise UnavailabilityError()
