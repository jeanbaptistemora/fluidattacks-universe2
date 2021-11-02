from dataclasses import (
    dataclass,
)
import logging
from purity.v1 import (
    Flattener,
    FrozenList,
    Patch,
    PureIter,
    Transform,
)
from purity.v1.pure_iter.factory import (
    from_flist,
)
from purity.v1.pure_iter.transform.io import (
    chain,
    consume,
)
from returns.curry import (
    partial,
)
from returns.io import (
    IO,
)
from returns.primitives.hkt import (
    SupportsKind1,
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
    _emit_io_streams: Transform[PureIter[IO[StreamData]], IO[None]]

    def emit(self, stream: Stream[_R]) -> IO[None]:
        return self._emit.unwrap(stream)

    def emit_io_streams(self, streams: PureIter[IO[StreamData]]) -> IO[None]:
        return self._emit_io_streams(streams)


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

    def _emit(self, stream: Stream[_R], schema: bool) -> IO[None]:
        if schema:
            self._emit_schema(stream.schema)
        emits_io = stream.records.map(
            partial(self._emit_record, stream.schema)
        )
        return consume(emits_io)

    def _emit_io_streams(self, streams: PureIter[IO[StreamData]]) -> IO[None]:
        first_emitted = False
        for io_stream in streams:
            io_stream.map(partial(self._emit, schema=not first_emitted))
            first_emitted = True
        return IO(None)

    def new_emitter(self) -> StreamEmitter:
        return StreamEmitter(
            Patch(partial(self._emit, schema=True)),
            Transform(self._emit_io_streams),
        )


@dataclass(frozen=True)
class StreamFactory:
    @staticmethod
    def new_stream(
        encoder: SingerEncoder[_D],
        get: Transform[_ID, IO[_D]],
        ids: PureIter[_ID],
    ) -> PureIter[IO[StreamData]]:
        result = (
            ids.map(get)
            .chunked(10)
            .map(
                lambda items: Flattener.list_io(tuple(items)).map(
                    lambda p: Stream(
                        encoder.schema,
                        from_flist(p).map(encoder.to_singer),
                    )
                )
            )
        )
        return result

    @staticmethod
    def multi_stream(
        encoder: SingerEncoder[_D],
        get: Transform[_ID, IO[FrozenList[_D]]],
        ids: PureIter[_ID],
    ) -> StreamIO:
        # pylint: disable=unnecessary-lambda
        # for correct type checking lambda is necessary
        items = ids.map(get)
        records = items.map(
            lambda p: p.map(
                lambda items: tuple(encoder.to_singer(i) for i in items)
            ).map(lambda i: from_flist(i))
        )
        return Stream(encoder.schema, chain(records))
