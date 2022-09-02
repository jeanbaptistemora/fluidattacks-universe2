from boto3.dynamodb.types import (
    TypeDeserializer,
)
from dynamodb.types import (
    EventName,
    Record,
)
from typing import (
    Any,
)


def deserialize_dynamodb_json(item: dict[str, Any]) -> dict[str, Any]:
    """Deserializes a DynamoDB JSON into a python dictionary"""
    deserializer = TypeDeserializer()

    return {
        key: deserializer.deserialize(value) for key, value in item.items()
    }


def format_record(record: dict[str, Any]) -> Record:
    """
    Formats the record into a NamedTuple

    https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_streams_Record.html
    """
    return Record(
        event_name=EventName[record["eventName"]],
        item=(
            deserialize_dynamodb_json(record["dynamodb"]["NewImage"])
            if "NewImage" in record["dynamodb"]
            else None
        ),
        pk=record["dynamodb"]["Keys"]["pk"]["S"],
        sequence_number=record["dynamodb"]["SequenceNumber"],
        sk=record["dynamodb"]["Keys"]["sk"]["S"],
    )
