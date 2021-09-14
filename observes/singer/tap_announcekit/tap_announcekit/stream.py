from dataclasses import (
    dataclass,
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
    Iterator,
    TypeVar,
)

DataIdType = TypeVar("DataIdType")
DataType = TypeVar("DataType")


@dataclass(frozen=True)
class StreamGetter(SupportsKind2["StreamGetter", DataIdType, DataType]):
    _get: Patch[Callable[[DataIdType], IO[DataType]]]
    _get_iter: Patch[
        Callable[[IO[Iterator[DataIdType]]], IO[Iterator[DataType]]]
    ]

    def __init__(
        self,
        get: Callable[[DataIdType], IO[DataType]],
        get_iter: Callable[[IO[Iterator[DataIdType]]], IO[Iterator[DataType]]],
    ) -> None:
        object.__setattr__(self, "_get", Patch(get))
        object.__setattr__(self, "_get_iter", Patch(get_iter))

    def get(self, item: DataIdType) -> IO[DataType]:
        return self._get.unwrap(item)

    def get_iter(
        self, items: IO[Iterator[DataIdType]]
    ) -> IO[Iterator[DataType]]:
        return self._get_iter.unwrap(items)


@dataclass(frozen=True)
class Stream:
    schema: SingerSchema
    records: IO[Iterator[SingerRecord]]


@dataclass(frozen=True)
class StreamEmitter:
    emitter: SingerEmitter
    stream: Stream

    def _emit(self, items: Iterator[SingerRecord]) -> IO[None]:
        self.emitter.emit_schema(self.stream.schema)
        for item in items:
            self.stream.schema.schema.validate(
                DictFactory.from_json(item.record)
            )
            self.emitter.emit_record(item)
        return IO(None)

    def emit(self) -> IO[None]:
        return self.stream.records.bind(self._emit)
