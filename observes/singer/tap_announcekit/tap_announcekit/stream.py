from dataclasses import (
    dataclass,
)
import logging
from purity.v1 import (
    Patch,
    PureIter,
)
from returns.curry import (
    partial,
)
from returns.io import (
    IO,
)
from returns.primitives.hkt import (
    SupportsKind1,
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
    JsonObj,
)
from typing import (
    Callable,
    NoReturn,
    TypeVar,
)

LOG = logging.getLogger(__name__)
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


_R = TypeVar("_R", SingerRecord, IO[SingerRecord])


@dataclass(frozen=True)
class Stream(SupportsKind1["Stream[_R]", _R]):
    schema: SingerSchema
    records: PureIter[_R]


StreamIO = Stream[IO[SingerRecord]]
StreamData = Stream[SingerRecord]


def _raise_and_inform(item: JsonObj, error: Exception) -> NoReturn:
    LOG.error("Invalid json: %s", item)
    raise error


@dataclass(frozen=True)
class StreamEmitter(SupportsKind1["StreamEmitter[_R]", _R]):
    emitter: SingerEmitter
    stream: Stream[_R]

    def _validate_record(self, item: SingerRecord) -> SingerRecord:
        jschema = self.stream.schema.schema
        raw_record = DictFactory.from_json(item.record)
        jschema.validate(raw_record).alt(
            partial(_raise_and_inform, item.record)
        )
        return item

    def _emit_record(self, item: _R) -> IO[None]:
        if isinstance(item, SingerRecord):
            return self.emitter.emit_record(self._validate_record(item))
        return item.map(self._validate_record).bind(self.emitter.emit_record)

    def _emit_schema(self, item: SingerSchema) -> IO[None]:
        return self.emitter.emit_schema(item)

    def emit(self) -> IO[None]:
        self._emit_schema(self.stream.schema)
        emits_io = self.stream.records.map_each(self._emit_record)
        return PureIter.consume(emits_io)
