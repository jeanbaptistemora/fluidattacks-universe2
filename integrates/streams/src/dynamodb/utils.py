from boto3 import (
    Session,
)
from boto3.dynamodb.types import (
    TypeDeserializer,
)
from typing import (
    Any,
)

SESSION = Session()


def deserialize_dynamodb_json(item: dict[str, Any]) -> dict[str, Any]:
    """Deserializes a DynamoDB JSON into a python dictionary"""
    deserializer = TypeDeserializer()

    return {
        key: deserializer.deserialize(value) for key, value in item.items()
    }
