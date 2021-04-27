# Standard libraries
from typing import (
    Iterator,
)

# Third party libraries
from returns.curry import (
    partial,
)
from returns.io import (
    IO,
)

# Local libraries
from singer_io import (
    factory,
)
from singer_io.singer import (
    SingerRecord,
)
from tap_delighted.api import (
    ApiPage,
)
from tap_delighted.common import (
    JSON,
)
from tap_delighted.streams.objs import (
    SupportedStreams,
)


def _json_list_srecords(
    stream: SupportedStreams, items: Iterator[JSON]
) -> Iterator[SingerRecord]:
    return iter(
        SingerRecord(stream=stream.value.lower(), record=item)
        for item in items
    )


def emit_records(
    stream: SupportedStreams,
    records: Iterator[JSON],
) -> None:
    s_records = _json_list_srecords(stream, records)
    for record in s_records:
        factory.emit(record)


def emit_page(stream: SupportedStreams, page: ApiPage) -> None:
    emit_records(stream, page.data)


def emit_iopage(stream: SupportedStreams, page: IO[ApiPage]) -> None:
    page.map(partial(emit_page, stream))
