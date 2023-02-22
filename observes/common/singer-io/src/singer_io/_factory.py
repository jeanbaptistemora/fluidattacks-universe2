import json
from json.encoder import (
    JSONEncoder,
)
from singer_io.singer import (
    InvalidType,
    MissingKeys,
    SingerRecord,
    SingerSchema,
    SingerState,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
)


def deserialize_schema(raw_singer_schema: str) -> SingerSchema:
    """Generate `SingerSchema` from json string"""
    raw_json: Dict[str, Any] = json.loads(raw_singer_schema)
    required_keys = frozenset({"type", "stream", "schema", "key_properties"})
    invalid: bool = any(map(lambda x: x not in raw_json, required_keys))
    if invalid:
        raise MissingKeys("Can not generate `SingerSchema` object")

    if raw_json["type"] == "SCHEMA":
        bookmark_properties: Optional[List[str]] = raw_json.get(
            "bookmark_properties", None
        )
        return SingerSchema(
            stream=raw_json["stream"],
            schema=raw_json["schema"],
            key_properties=frozenset(raw_json["key_properties"]),
            bookmark_properties=frozenset(bookmark_properties)
            if bookmark_properties
            else None,
        )
    raise InvalidType(f'Expected "SCHEMA" not "{raw_json["type"]}"')


def deserialize_record(raw_singer_record: str) -> SingerRecord:
    """Generate `SingerRecord` from json string"""
    raw_json: Dict[str, Any] = json.loads(raw_singer_record)
    required_keys = frozenset({"type", "stream", "record"})
    invalid: bool = any(map(lambda x: x not in raw_json, required_keys))
    if invalid:
        raise MissingKeys("Can not generate `SingerRecord` object")
    if raw_json["type"] == "RECORD":
        return SingerRecord(
            stream=raw_json["stream"],
            record=raw_json["record"],
            time_extracted=raw_json.get("time_extracted", None),
        )
    raise InvalidType(f'Expected "RECORD" not "{raw_json["type"]}"')


def deserialize_state(raw_singer_state: str) -> SingerState:
    """Generate `SingerState` from json string"""
    raw_json: Dict[str, Any] = json.loads(raw_singer_state)
    required_keys = frozenset({"type", "value"})
    invalid: bool = any(map(lambda x: x not in raw_json, required_keys))
    if invalid:
        raise MissingKeys("Can not generate `SingerState` object")
    if raw_json["type"] == "STATE":
        return SingerState(value=raw_json["value"])
    raise InvalidType(f'Expected "STATE" not "{raw_json["type"]}"')


class CustomJsonEncoder(JSONEncoder):
    def default(self: JSONEncoder, o: Any) -> Any:
        if isinstance(o, frozenset):
            return list(o)
        return JSONEncoder.default(self, o)
