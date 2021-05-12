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
    OrgsApi,
    ProjectsApi,
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


def all_collaborators(api: ApiClient) -> None:
    orgs_io = api.user.list_orgs_id(ALL)
    client = api.user.client
    _stream_data(
        SupportedStreams.COLLABORATORS,
        orgs_io.bind(partial(OrgsApi.list_orgs_collaborators, client)),
    )


def all_projects(api: ApiClient) -> None:
    orgs_io = api.user.list_orgs_id(ALL)
    client = api.user.client
    _stream_data(
        SupportedStreams.ERRORS,
        orgs_io.bind(partial(OrgsApi.list_orgs_projs, client)),
    )


def all_errors(api: ApiClient) -> None:
    orgs_io = api.user.list_orgs_id(ALL)
    client = api.user.client
    _stream_data(
        SupportedStreams.ERRORS,
        orgs_io.bind(partial(OrgsApi.list_orgs_projs_id, client)).bind(
            partial(ProjectsApi.list_projs_errors, client)
        ),
    )


def all_events(api: ApiClient) -> None:
    orgs_io = api.user.list_orgs_id(ALL)
    client = api.user.client
    _stream_data(
        SupportedStreams.EVENTS,
        orgs_io.bind(partial(OrgsApi.list_orgs_projs_id, client)).bind(
            partial(ProjectsApi.list_projs_events, client)
        ),
    )


def all_releases(api: ApiClient) -> None:
    orgs_io = api.user.list_orgs_id(ALL)
    client = api.user.client
    _stream_data(
        SupportedStreams.RELEASES,
        orgs_io.bind(partial(OrgsApi.list_orgs_projs_id, client)).bind(
            partial(ProjectsApi.list_projs_releases, client)
        ),
    )


__all__ = [
    "SupportedStreams",
]
