from dataclasses import (
    dataclass,
)
from purity.v1 import (
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

_ID = TypeVar("_ID")
_D = TypeVar("_D")


@dataclass(frozen=True)
class StreamGetter(SupportsKind2["StreamGetter[_ID, _D]", _ID, _D]):
    _get: Patch[Callable[[_ID], IO[_D]]]
    _get_iter: Patch[Callable[[PureIter[_ID]], PureIter[IO[_D]]]]

    def __init__(
        self,
        get: Callable[[_ID], IO[_D]],
        get_iter: Callable[[PureIter[_ID]], PureIter[IO[_D]]],
    ) -> None:
        object.__setattr__(self, "_get", Patch(get))
        object.__setattr__(self, "_get_iter", Patch(get_iter))

    def get(self, item: _ID) -> IO[_D]:
        return self._get.unwrap(item)

    def get_iter(self, items: PureIter[_ID]) -> PureIter[IO[_D]]:
        return self._get_iter.unwrap(items)


@dataclass(frozen=True)
class Stream:
    schema: SingerSchema
    records: PureIter[IO[SingerRecord]]


@dataclass(frozen=True)
class StreamEmitter:
    emitter: SingerEmitter
    stream: Stream

    def _emit(self, item: SingerRecord) -> IO[None]:
        self.stream.schema.schema.validate(DictFactory.from_json(item.record))
        return self.emitter.emit_record(item)

    def emit(self) -> IO[None]:
        self.emitter.emit_schema(self.stream.schema)
        return PureIter.consume(
            self.stream.records.map_each(lambda s: s.bind(self._emit))
        )
