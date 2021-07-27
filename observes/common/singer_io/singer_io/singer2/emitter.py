# pylint: skip-file
from dataclasses import (
    dataclass,
)
import json
from json.encoder import (
    JSONEncoder,
)
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
    JsonObj,
    JsonValue,
)
import sys
from typing import (
    Any,
    IO as IO_FILE,
)


class CustomJsonEncoder(JSONEncoder):
    def default(self: JSONEncoder, o: Any) -> Any:
        if isinstance(o, JsonValue):
            return o.unfold()
        return JSONEncoder.default(self, o)


@dataclass(frozen=True)
class SingerEmitter:
    target: IO_FILE[str] = sys.stdout

    def emit_record(self, record: SingerRecord) -> IO[None]:
        time_str = Maybe.from_optional(record.time_extracted).map(
            lambda date: date.to_utc_str()
        )
        json_obj: JsonObj = {
            "stream": JsonValue(record.stream),
            "record": JsonValue(record.record),
            "time_extracted": JsonValue(time_str.value_or(None)),
        }
        json.dump(json_obj, self.target, cls=CustomJsonEncoder)
        return IO(None)
