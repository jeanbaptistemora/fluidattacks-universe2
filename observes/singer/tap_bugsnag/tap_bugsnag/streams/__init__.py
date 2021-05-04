# Standard libraries
from typing import (
    Iterator,
)

# Third party libraries
from returns.curry import partial
from returns.io import IO

# Local libraries
from paginator import (
    AllPages,
)
from singer_io import factory
from singer_io.singer import SingerRecord
from tap_bugsnag.api import ApiClient, ApiPage
from tap_bugsnag.streams.objs import SupportedStreams


ALL = AllPages()


def _to_singer(
    stream: SupportedStreams, page: ApiPage
) -> Iterator[SingerRecord]:
    return iter(
        map(lambda item: SingerRecord(stream.value.lower(), item), page.data)
    )


def _emit_pages(stream: SupportedStreams, pages: Iterator[ApiPage]) -> None:
    for page in pages:
        for item in _to_singer(stream, page):
            factory.emit(item)


def _stream_data(
    stream: SupportedStreams,
    pages: IO[Iterator[ApiPage]],
) -> None:
    pages.map(partial(_emit_pages, stream))


def all_orgs(api: ApiClient) -> None:
    _stream_data(SupportedStreams.ORGS, api.orgs.list_orgs(ALL))


__all__ = [
    "SupportedStreams",
]
