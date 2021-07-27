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
    SingerRecord,
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
            "stream": JsonValue(record.stream),
            "record": JsonValue(record.record),
            "time_extracted": JsonValue(time_str.value_or(None)),
        }
        return self.emitter.emit(json_obj)
