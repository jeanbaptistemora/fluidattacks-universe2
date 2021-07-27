# pylint: skip-file
from dataclasses import (
    dataclass,
)
import json
from returns.io import (
    IO,
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
    JsonEmitter,
    JsonObj,
    JsonValue,
)
import sys
from typing import (
    IO as IO_FILE,
)


@dataclass(frozen=True)
class SingerEmitter:
    emitter: JsonEmitter

    def emit_record(self, record: SingerRecord) -> IO[None]:
        time_str = Maybe.from_optional(record.time_extracted).map(
            lambda date: date.to_utc_str()
        )
        json_obj: JsonObj = {
            "type": JsonValue("RECORD"),
            "stream": JsonValue(record.stream),
            "record": JsonValue(record.record),
            "time_extracted": JsonValue(time_str.value_or(None)),
        }
        return self.emitter.emit(json_obj)

    def emit_schema(self, schema: SingerSchema) -> IO[None]:
        bookmark_properties = Maybe.from_optional(
            schema.bookmark_properties
        ).map(lambda fset: [JsonValue(item) for item in fset])
        json_obj: JsonObj = {
            "type": JsonValue("SCHEMA"),
            "stream": JsonValue(schema.stream),
            "schema": JsonValue(schema.schema.to_json()),
            "key_properties": JsonValue(
                [JsonValue(item) for item in schema.key_properties]
            ),
            "bookmark_properties": JsonValue(
                bookmark_properties.value_or(None)
            ),
        }
        return self.emitter.emit(json_obj)

    def emit_state(self, state: SingerState) -> IO[None]:
        json_obj: JsonObj = {
            "type": JsonValue("STATE"),
            "value": JsonValue(state.value),
        }
        return self.emitter.emit(json_obj)

    def emit(self, singer: SingerMessage) -> IO[None]:
        if isinstance(singer, SingerRecord):
            return self.emit_record(singer)
        if isinstance(singer, SingerSchema):
            return self.emit_schema(singer)
        return self.emit_state(singer)
