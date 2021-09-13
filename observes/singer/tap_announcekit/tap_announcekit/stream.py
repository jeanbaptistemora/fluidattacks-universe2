from dataclasses import (
    dataclass,
)
from returns.io import (
    IO,
)
from singer_io.singer2 import (
    SingerRecord,
    SingerSchema,
)
from singer_io.singer2.emitter import (
    SingerEmitter,
)
from typing import (
    Iterator,
)


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
            self.emitter.emit_record(item)
        return IO(None)

    def emit(self) -> IO[None]:
        return self.stream.records.bind(self._emit)
