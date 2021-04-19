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
    stream: str,
    items: Iterator[JSON]
) -> Iterator[SingerRecord]:
    return iter(map(
        lambda item: SingerRecord(
            stream=stream,
            record=item
        ),
        items
    ))


def emit_records(records: Iterator[SingerRecord]) -> None:
    for record in records:
        factory.emit(record)


def emit_page(stream: SupportedStreams, page: ApiPage) -> None:
    records: IO[Iterator[SingerRecord]] = page.data.map(
        partial(_json_list_srecords, stream.value.lower())
    )
    records.map(emit_records)
