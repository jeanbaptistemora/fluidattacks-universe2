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

DataIdType = TypeVar("DataIdType")
DataType = TypeVar("DataType")


@dataclass(frozen=True)
class StreamGetter(SupportsKind2["StreamGetter", DataIdType, DataType]):
    _get: Patch[Callable[[DataIdType], IO[DataType]]]
    _get_iter: Patch[Callable[[PureIter[DataIdType]], IOiter[DataType]]]

    def __init__(
        self,
        get: Callable[[DataIdType], IO[DataType]],
        get_iter: Callable[[PureIter[DataIdType]], IOiter[DataType]],
    ) -> None:
        object.__setattr__(self, "_get", Patch(get))
        object.__setattr__(self, "_get_iter", Patch(get_iter))

    def get(self, item: DataIdType) -> IO[DataType]:
        return self._get.unwrap(item)

    def get_iter(self, items: PureIter[DataIdType]) -> IOiter[DataType]:
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
