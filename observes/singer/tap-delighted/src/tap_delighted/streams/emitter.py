from returns.io import (
    IO,
)
from singer_io.singer2 import (
    SingerEmitter,
    SingerRecord,
)
from singer_io.singer2.json import (
    JsonObj,
)
from tap_delighted.api import (
    ApiPage,
)
from tap_delighted.streams.objs import (
    SupportedStreams,
)
from typing import (
    Iterator,
)

emitter = SingerEmitter()


def emit_records(
    stream: SupportedStreams,
    records: Iterator[JsonObj],
) -> IO[None]:
    s_records = (
        SingerRecord(stream=stream.value.lower(), record=item)
        for item in records
    )
    for record in s_records:
        emitter.emit(record)
    return IO(None)


def emit_iopage(stream: SupportedStreams, page: IO[ApiPage]) -> IO[None]:
    page.map(lambda p: emit_records(stream, p.data))
    return IO(None)
