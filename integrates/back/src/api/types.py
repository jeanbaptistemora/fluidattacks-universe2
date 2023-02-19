from custom_exceptions import (
    CustomBaseException,
)
from dynamodb.exceptions import (
    DynamoDbBaseException,
)
from typing import (
    Any,
    NamedTuple,
)

APP_EXCEPTIONS = (CustomBaseException, DynamoDbBaseException)


class Operation(NamedTuple):
    name: str
    query: str
    variables: dict[str, Any]
