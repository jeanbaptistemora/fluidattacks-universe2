import json
from singer_io import (
    factory,
)
from singer_io.singer import (
    SingerHandler,
    SingerMessage,
    SingerRecord,
    SingerSchema,
    SingerState,
)
from typing import (
    Any,
    Dict,
    NamedTuple,
    Optional,
)


def mock_schema() -> Dict[str, Any]:
    return {
        "type": "SCHEMA",
        "stream": "users",
        "schema": {
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "updated_at": {"type": "string", "format": "date-time"},
            }
        },
        "key_properties": ["id"],
        "bookmark_properties": ["updated_at"],
    }


def mock_record() -> Dict[str, Any]:
    return {
        "type": "RECORD",
        "stream": "users",
        "record": {"id": 2, "name": "Mike"},
    }


def mock_state() -> Dict[str, Any]:
    return {"type": "STATE", "value": {"users": 2, "locations": 1}}


def test_deserialize_schema() -> None:
    raw_json = mock_schema()
    schema = factory.deserialize(json.dumps(raw_json))
    expected = SingerSchema(
        stream=raw_json["stream"],
        schema=raw_json["schema"],
        key_properties=frozenset(raw_json["key_properties"]),
        bookmark_properties=frozenset(raw_json["bookmark_properties"]),
    )
    assert schema == expected


def test_deserialize_record() -> None:
    raw_json = mock_record()
    schema = factory.deserialize(json.dumps(raw_json))
    expected = SingerRecord(
        stream=raw_json["stream"], record=raw_json["record"]
    )
    assert schema == expected


def test_deserialize_state() -> None:
    raw_json = mock_state()
    schema = factory.deserialize(json.dumps(raw_json))
    expected = SingerState(value=raw_json["value"])
    assert schema == expected


def test_singer_handler() -> None:
    raw_srecord = json.dumps(mock_record())
    raw_sschema = json.dumps(mock_schema())
    srecord = factory.deserialize(raw_srecord)
    sschema = factory.deserialize(raw_sschema)

    class TestState(NamedTuple):
        singer: Optional[SingerMessage] = None
        num: int = 0

    def handle1(singer: SingerRecord, state: TestState) -> TestState:
        return TestState(singer, state.num + 1)

    def handle2(singer: SingerSchema, state: TestState) -> TestState:
        return TestState(singer, state.num + 2)

    handler: SingerHandler[TestState] = factory.singer_handler(
        handle2, handle1, None
    )
    state = TestState()
    assert handler(raw_srecord, state) == TestState(srecord, 1)
    assert handler(raw_sschema, state) == TestState(sschema, 2)
