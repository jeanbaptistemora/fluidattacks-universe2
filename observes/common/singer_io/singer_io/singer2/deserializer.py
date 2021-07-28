# pylint: skip-file

from dataclasses import (
    dataclass,
)
from returns.maybe import (
    Maybe,
)
from singer_io.singer2._objs import (
    SingerMessage,
    SingerRecord,
    SingerSchema,
    SingerState,
)
from singer_io.singer2.json import (
    DictFactory,
    JsonFactory,
    JsonObj,
)
from singer_io.singer2.json_schema import (
    JsonSchemaFactory,
)
from singer_io.singer2.time import (
    TimeFactory,
)
from typing import (
    Any,
    Dict,
    IO as IO_FILE,
    Iterator,
)


class MissingKeys(Exception):
    pass


class InvalidType(Exception):
    pass


@dataclass(frozen=True)
class SingerDeserializer:
    @classmethod
    def build_schema(
        cls, raw_dict: Dict[str, Any], raw_json: JsonObj
    ) -> SingerSchema:
        required_keys = frozenset(
            {"type", "stream", "schema", "key_properties"}
        )
        invalid: bool = any(map(lambda x: x not in raw_json, required_keys))
        if invalid:
            raise MissingKeys("Can not generate `SingerSchema` object")
        parsed_type = raw_json["type"].to_primitive(str)
        if parsed_type == "SCHEMA":
            bookmark_properties = (
                Maybe.from_optional(raw_json.get("bookmark_properties", None))
                .map(lambda item: item.to_list_of(str))
                .map(lambda item: frozenset(item))
            )
            return SingerSchema(
                stream=raw_json["stream"].to_primitive(str),
                schema=JsonSchemaFactory.from_dict(raw_dict["schema"]),
                key_properties=frozenset(
                    raw_json["key_properties"].to_list_of(str)
                ),
                bookmark_properties=bookmark_properties.value_or(None),
            )
        raise InvalidType(f'Expected "SCHEMA" not "{parsed_type}"')

    @classmethod
    def build_record(cls, raw_json: JsonObj) -> SingerRecord:
        required_keys = frozenset({"type", "stream", "record"})
        invalid: bool = any(map(lambda x: x not in raw_json, required_keys))
        if invalid:
            raise MissingKeys("Can not generate `SingerRecord` object")
        parsed_type = raw_json["type"].to_primitive(str)
        time_extracted = (
            Maybe.from_optional(raw_json.get("time_extracted", None))
            .map(lambda item: item.to_primitive(str))
            .map(TimeFactory.parse)
        )
        if parsed_type == "RECORD":
            return SingerRecord(
                stream=raw_json["stream"].to_primitive(str),
                record=raw_json["record"].to_json(),
                time_extracted=time_extracted.value_or(None),
            )
        raise InvalidType(f'Expected "RECORD" not "{parsed_type}"')

    @classmethod
    def build_state(cls, raw_json: JsonObj) -> SingerState:
        required_keys = frozenset({"type", "value"})
        invalid: bool = any(map(lambda x: x not in raw_json, required_keys))
        if invalid:
            raise MissingKeys("Can not generate `SingerState` object")
        parsed_type = raw_json["type"].to_primitive(str)
        if parsed_type == "STATE":
            return SingerState(value=raw_json["value"].to_json())
        raise InvalidType(f'Expected "STATE" not "{parsed_type}"')

    @classmethod
    def deserialize(cls, raw_singer: str) -> SingerMessage:
        raw_dict = DictFactory.loads(raw_singer)
        raw_json = JsonFactory.from_dict(raw_dict)
        parsed_type = raw_json["type"].to_primitive(str)
        if parsed_type == "RECORD":
            return cls.build_record(raw_json)
        if parsed_type == "SCHEMA":
            return cls.build_schema(raw_dict, raw_json)
        if parsed_type == "STATE":
            return cls.build_state(raw_json)
        raise InvalidType(f"Unknown type '{parsed_type}'")

    @classmethod
    def from_file(cls, file: IO_FILE[str]) -> Iterator[SingerMessage]:
        line = file.readline()
        while line:
            yield cls.deserialize(line)
            line = file.readline()
