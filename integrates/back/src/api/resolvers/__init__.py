from custom_exceptions import (
    CustomBaseException,
)
from dynamodb.exceptions import (
    DynamoDbBaseException,
)

APP_BASE_EXCEPTIONS = (CustomBaseException, DynamoDbBaseException)
