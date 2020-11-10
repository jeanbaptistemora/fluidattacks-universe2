# Standard libraries
import json
# Third party libraries
# Local libraries
from target_redshift_2.singer import (
    SingerFactory,
    SingerRecord,
    SingerRecordFactory,
    SingerSchema,
    SingerSchemaFactory,
)


def mock_schema():
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


def test_SingerSchemaFactory():
    factory = SingerSchemaFactory()
    raw_json = mock_schema()
    schema = factory.deserialize(json.dumps(raw_json))
    expected = SingerSchema(
        stream='users',
        schema=raw_json['schema'],
        key_properties=set(raw_json['key_properties']),
        bookmark_properties=set(raw_json['bookmark_properties']),
    )
    assert schema == expected


def test_SingerRecordFactory():
    factory = SingerRecordFactory()
    raw_json = {
        "type": "RECORD",
        "stream": "users",
        "record": {"id": 2, "name": "Mike"}
    }
    schema = factory.deserialize(json.dumps(raw_json))
    expected = SingerRecord(
        stream='users',
        record=raw_json['record']
    )
    assert schema == expected


def test_SingerFactory():
    factory = SingerFactory()
    raw_json_record = {
        "type": "RECORD",
        "stream": "users",
        "record": {"id": 2, "name": "Mike"}
    }
    raw_json_schema = mock_schema()
    result_schema = factory.deserialize(json.dumps(raw_json_schema))
    result_record = factory.deserialize(json.dumps(raw_json_record))

    assert isinstance(result_schema, SingerSchema)
    assert isinstance(result_record, SingerRecord)

    expected_schema = SingerSchema(
        stream='users',
        schema=raw_json_schema['schema'],
        key_properties=set(raw_json_schema['key_properties']),
        bookmark_properties=set(raw_json_schema['bookmark_properties']),
    )
    expected_record = SingerRecord(
        stream='users',
        record=raw_json_record['record']
    )
    assert result_record == expected_record
    assert result_schema == expected_schema
