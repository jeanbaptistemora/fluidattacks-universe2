# Standard libraries
from typing import (
    Iterator,
)

# Third party libraries
from returns.curry import (
    partial,
)

# Local libraries
from singer_io import (
    factory,
)
from singer_io.singer import (
    SingerRecord,
)
from tap_checkly.api import (
    ApiPage,
)
from tap_checkly.common import (
    JSON,
)
from tap_checkly.streams.objs import (
    SupportedStreams,
)


def _json_list_srecords(
    stream: SupportedStreams,
    items: Iterator[JSON]
) -> Iterator[SingerRecord]:
    return iter(map(
        lambda item: SingerRecord(
            stream=stream.value.lower(),
            record=item
        ),
        items
    ))


def emit_records(
    stream: SupportedStreams,
    records: Iterator[JSON],
) -> None:
    s_records = _json_list_srecords(stream, records)
    for record in s_records:
        factory.emit(record)


def emit_page(stream: SupportedStreams, page: ApiPage) -> None:
    page.data.map(
        partial(emit_records, stream)
    )
