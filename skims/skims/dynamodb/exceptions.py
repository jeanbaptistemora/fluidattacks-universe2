# pylint: disable=super-with-arguments
from botocore.exceptions import (
    ClientError,
)
import sys
from utils.logs import (
    log_blocking,
)


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
        raise custom_exception

    log_blocking("error", "%s", error)
    raise UnavailabilityError()
