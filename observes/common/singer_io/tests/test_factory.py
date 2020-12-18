# Standard libraries
import json
from typing import Any, Dict
# Third party libraries
# Local libraries
from singer_io import factory
from singer_io.singer import (
    SingerRecord,
    SingerSchema,
)


def mock_schema() -> Dict[str, Any]:
    return {
        "type": "SCHEMA",
        "stream": "users",
        "schema": {
            "properties": {
                "id": {
                    "type": "integer"
                },
                "name": {
                    "type": "string"
                },
                "updated_at": {
                    "type": "string",
                    "format": "date-time"
                }
            }
        },
        "key_properties": ["id"],
        "bookmark_properties": ["updated_at"]
    }


def mock_record() -> Dict[str, Any]:
    return {
        "type": "RECORD",
        "stream": "users",
        "record": {"id": 2, "name": "Mike"}
    }


def test_deserialize_schema() -> None:
    raw_json = mock_schema()
    schema = factory.deserialize(json.dumps(raw_json))
    expected = SingerSchema(
        stream=raw_json['stream'],
        schema=raw_json['schema'],
        key_properties=frozenset(raw_json['key_properties']),
        bookmark_properties=frozenset(raw_json['bookmark_properties']),
    )
    assert schema == expected


def test_deserialize_record() -> None:
    raw_json = mock_record()
    schema = factory.deserialize(json.dumps(raw_json))
    expected = SingerRecord(
        stream=raw_json['stream'],
        record=raw_json['record']
    )
    assert schema == expected
