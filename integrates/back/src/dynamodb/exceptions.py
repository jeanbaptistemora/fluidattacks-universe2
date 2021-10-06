# pylint: disable=super-with-arguments
from botocore.exceptions import (
    ClientError,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
import sys
from typing import (
    Optional,
)

# Constants
logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


class DynamoDbBaseException(Exception):
    pass


class ConditionalCheckFailedException(DynamoDbBaseException):
    pass


class UnavailabilityError(DynamoDbBaseException):
    def __init__(self) -> None:
        msg = "Service unavailable, please retry"
        super(UnavailabilityError, self).__init__(msg)


def handle_error(*, error: ClientError) -> None:
    code: str = error.response["Error"]["Code"]
    custom_exception: Optional[Exception] = getattr(
        sys.modules[__name__], code, None
    )

    if custom_exception:
        raise custom_exception

    LOGGER.exception(error)
    raise UnavailabilityError()
