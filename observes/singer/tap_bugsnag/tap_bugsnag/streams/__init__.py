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
from tap_bugsnag.api import (
    ApiClient,
    ApiPage,
    OrgId,
)
from tap_bugsnag.streams.objs import SupportedStreams


ALL = AllPages()


def _to_singer(
    stream: SupportedStreams, page: ApiPage
) -> Iterator[SingerRecord]:
    return (SingerRecord(stream.value.lower(), item) for item in page.data)


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
    _stream_data(SupportedStreams.ORGS, api.user.list_orgs(ALL))


def all_projects(api: ApiClient) -> None:
    orgs = api.user.list_orgs_id(ALL)

    def _stream(orgs: Iterator[OrgId]) -> None:
        for org in orgs:
            _stream_data(
                SupportedStreams.PROJECTS, api.org(org).list_projects(ALL)
            )

    orgs.map(_stream)


__all__ = [
    "SupportedStreams",
]
