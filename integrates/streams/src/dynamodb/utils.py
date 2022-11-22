# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from boto3.dynamodb.types import (
    TypeDeserializer,
)
from dynamodb.types import (
    Item,
    Record,
    StreamEvent,
)
from opensearchpy import (
    JSONSerializer,
)
from typing import (
    Any,
)


class SetEncoder(JSONSerializer):
    def default(self, data: Any) -> JSONSerializer:
        if isinstance(data, set):
            return list(data)  # type: ignore
        return JSONSerializer.default(self, data)


def deserialize_dynamodb_json(item: Item) -> Item:
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
        event_name=StreamEvent[record["eventName"]],
        new_image=(
            deserialize_dynamodb_json(record["dynamodb"]["NewImage"])
            if "NewImage" in record["dynamodb"]
            else None
        ),
        old_image=(
            deserialize_dynamodb_json(record["dynamodb"]["OldImage"])
            if "OldImage" in record["dynamodb"]
            else None
        ),
        pk=record["dynamodb"]["Keys"]["pk"]["S"],
        sequence_number=record["dynamodb"]["SequenceNumber"],
        sk=record["dynamodb"]["Keys"]["sk"]["S"],
    )
