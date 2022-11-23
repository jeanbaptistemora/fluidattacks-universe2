from singer_io.singer2.json import (
    JsonObj,
)
from singer_io.singer2.json_schema import (
    JsonSchema,
)
from singer_io.singer2.time import (
    DateTime,
)
from typing import (
    FrozenSet,
    NamedTuple,
    Optional,
    Union,
)


class SingerSchema(NamedTuple):
    stream: str
    schema: JsonSchema
    key_properties: FrozenSet[str]
    bookmark_properties: Optional[FrozenSet[str]] = None


class SingerRecord(NamedTuple):
    stream: str
    record: JsonObj
    time_extracted: Optional[DateTime] = None


class SingerState(NamedTuple):
    value: JsonObj


SingerMessage = Union[SingerRecord, SingerSchema, SingerState]
