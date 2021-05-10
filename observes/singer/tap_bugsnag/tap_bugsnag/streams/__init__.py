# Standard libraries
from itertools import chain
from typing import (
    Iterator,
    TypeVar,
)

# Third party libraries
from returns.unsafe import unsafe_perform_io
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
    ErrorsPage,
    OrgId,
    ProjId,
    ProjectsPage,
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


_Data = TypeVar("_Data")


def _fold(items: Iterator[IO[Iterator[_Data]]]) -> IO[Iterator[_Data]]:
    def rm_io(items: IO[Iterator[_Data]]) -> Iterator[_Data]:
        return unsafe_perform_io(items)

    raw = map(rm_io, items)
    return IO(chain.from_iterable(raw))


def _get_projs(
    api: ApiClient, orgs: Iterator[OrgId]
) -> IO[Iterator[ProjectsPage]]:
    return _fold(iter(map(lambda org: api.org(org).list_projects(ALL), orgs)))


def _get_projs_id(
    api: ApiClient, orgs: Iterator[OrgId]
) -> IO[Iterator[ProjId]]:
    return _fold(iter(map(lambda org: api.org(org).list_projs_id(ALL), orgs)))


def _get_errors(
    api: ApiClient, projs: Iterator[ProjId]
) -> IO[Iterator[ErrorsPage]]:
    return _fold(
        iter(map(lambda proj: api.proj(proj).list_errors(ALL), projs))
    )


def all_orgs(api: ApiClient) -> None:
    _stream_data(SupportedStreams.ORGS, api.user.list_orgs(ALL))


def all_projects(api: ApiClient) -> None:
    orgs_io = api.user.list_orgs_id(ALL)
    _stream_data(
        SupportedStreams.ERRORS, orgs_io.bind(partial(_get_projs, api))
    )


def all_errors(api: ApiClient) -> None:
    orgs_io = api.user.list_orgs_id(ALL)
    _stream_data(
        SupportedStreams.ERRORS,
        orgs_io.bind(partial(_get_projs_id, api)).bind(
            partial(_get_errors, api)
        ),
    )


__all__ = [
    "SupportedStreams",
]
