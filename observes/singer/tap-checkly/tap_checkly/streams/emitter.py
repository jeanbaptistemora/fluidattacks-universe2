from returns.curry import (
    partial,
)
from returns.io import (
    IO,
)
from singer_io.singer2 import (
    SingerRecord,
)
from singer_io.singer2.emitter import (
    SingerEmitter,
)
from singer_io.singer2.json import (
    JsonEmitter,
    JsonObj,
)
from tap_checkly.api import (
    ApiPage,
)
from tap_checkly.streams.objs import (
    SupportedStreams,
)
from typing import (
    Iterator,
    List,
)

emitter = SingerEmitter(JsonEmitter())


def _json_list_srecords(
    stream: SupportedStreams, items: List[JsonObj]
) -> Iterator[SingerRecord]:
    return iter(
        map(
            lambda item: SingerRecord(
                stream=stream.value.lower(), record=item
            ),
            items,
        )
    )


def emit_records(
    stream: SupportedStreams,
    records: List[JsonObj],
) -> None:
    s_records = _json_list_srecords(stream, records)
    for record in s_records:
        emitter.emit(record)


def emit_page(stream: SupportedStreams, page: ApiPage) -> None:
    emit_records(stream, page.data)


def emit_iopage(stream: SupportedStreams, page: IO[ApiPage]) -> None:
    page.map(partial(emit_page, stream))
