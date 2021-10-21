from dataclasses import (
    dataclass,
)
import logging
from purity.v1 import (
    Patch,
    PureIter,
    Transform,
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
class SingerEncoder(SupportsKind1["SingerEncoder[_D]", _D]):
    schema: SingerSchema
    to_singer: Transform[_D, SingerRecord]


@dataclass(frozen=True)
class Stream(SupportsKind1["Stream[_R]", _R]):
    schema: SingerSchema
    records: PureIter[_R]


StreamIO = Stream[IO[SingerRecord]]
StreamData = Stream[SingerRecord]


@dataclass(frozen=True)
class StreamEmitter:
    _emit: Patch[Callable[[Stream[_R]], IO[None]]]

    def emit(self, stream: Stream[_R]) -> IO[None]:
        return self._emit.unwrap(stream)


@dataclass(frozen=True)
class StreamEmitterFactory:
    s_emitter: SingerEmitter

    @staticmethod
    def _raise_and_inform(item: JsonObj, error: Exception) -> NoReturn:
        LOG.error("Invalid json: %s", item)
        raise error

    def _validate_record(
        self, schema: SingerSchema, item: SingerRecord
    ) -> SingerRecord:
        jschema = schema.schema
        raw_record = DictFactory.from_json(item.record)
        jschema.validate(raw_record).alt(
            partial(self._raise_and_inform, item.record)
        )
        return item

    def _emit_record(self, schema: SingerSchema, item: _R) -> IO[None]:
        validate = partial(self._validate_record, schema)
        if isinstance(item, SingerRecord):
            return self.s_emitter.emit_record(validate(item))
        return item.map(validate).bind(self.s_emitter.emit_record)

    def _emit_schema(self, item: SingerSchema) -> IO[None]:
        return self.s_emitter.emit_schema(item)

    def _emit(self, stream: Stream[_R]) -> IO[None]:
        self._emit_schema(stream.schema)
        emits_io = stream.records.map_each(
            partial(self._emit_record, stream.schema)
        )
        return PureIter.consume(emits_io)

    def new_emitter(self) -> StreamEmitter:
        return StreamEmitter(Patch(self._emit))


@dataclass(frozen=True)
class StreamFactory:
    @staticmethod
    def new_stream(
        encoder: SingerEncoder[_D],
        get: Transform[_ID, IO[_D]],
        ids: PureIter[_ID],
    ) -> StreamIO:
        items = ids.map_each(get)
        records = items.map_each(lambda p: p.map(encoder.to_singer))
        return Stream(encoder.schema, records)
