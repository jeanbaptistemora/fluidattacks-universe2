from dataclasses import (
    dataclass,
)
from purity.v1 import (
    IOiter,
    PureIter,
)
from returns.io import (
    IO,
)
from returns.primitives.hkt import (
    SupportsKind2,
)
from singer_io.singer2 import (
    SingerRecord,
    SingerSchema,
)
from singer_io.singer2.emitter import (
    SingerEmitter,
)
from singer_io.singer2.json import (
    DictFactory,
)
from tap_announcekit.utils import (
    Patch,
)
from typing import (
    Callable,
    TypeVar,
)

_DataIdType = TypeVar("_DataIdType")
_DataType = TypeVar("_DataType")


@dataclass(frozen=True)
class StreamGetter(
    SupportsKind2[
        "StreamGetter[_DataIdType, _DataType]", _DataIdType, _DataType
    ]
):
    _get: Patch[Callable[[_DataIdType], IO[_DataType]]]
    _get_iter: Patch[Callable[[PureIter[_DataIdType]], IOiter[_DataType]]]

    def __init__(
        self,
        get: Callable[[_DataIdType], IO[_DataType]],
        get_iter: Callable[[PureIter[_DataIdType]], IOiter[_DataType]],
    ) -> None:
        object.__setattr__(self, "_get", Patch(get))
        object.__setattr__(self, "_get_iter", Patch(get_iter))

    def get(self, item: _DataIdType) -> IO[_DataType]:
        return self._get.unwrap(item)

    def get_iter(self, items: PureIter[_DataIdType]) -> IOiter[_DataType]:
        return self._get_iter.unwrap(items)


@dataclass(frozen=True)
class Stream:
    schema: SingerSchema
    records: IOiter[SingerRecord]


@dataclass(frozen=True)
class StreamEmitter:
    emitter: SingerEmitter
    stream: Stream

    def _emit(self, item: SingerRecord) -> IO[None]:
        self.stream.schema.schema.validate(DictFactory.from_json(item.record))
        return self.emitter.emit_record(item)

    def emit(self) -> IO[None]:
        self.emitter.emit_schema(self.stream.schema)
        return self.stream.records.bind_each(self._emit).consume()
