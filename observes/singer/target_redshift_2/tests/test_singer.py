# Standard libraries
import json
# Third party libraries
# Local libraries
from target_redshift_2.singer import SingerSchema, SingerSchemaFactory


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
