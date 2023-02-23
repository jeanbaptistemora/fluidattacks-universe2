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


class ValidationException(DynamoDbBaseException):
    pass


def handle_error(*, error: ClientError) -> None:
    code: str = error.response["Error"]["Code"]
    custom_exception: Exception | None = getattr(
        sys.modules[__name__], code, None
    )

    if custom_exception:
        raise custom_exception from error

    LOGGER.exception(error)
    raise UnavailabilityError()
