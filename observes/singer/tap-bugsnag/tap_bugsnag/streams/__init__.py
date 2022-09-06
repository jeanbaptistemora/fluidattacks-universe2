from paginator import (
    AllPages,
)
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
)
from tap_bugsnag.api import (
    ApiClient,
    ApiData,
    OrgsApi,
    ProjectsApi,
)
from tap_bugsnag.streams.objs import (
    SupportedStreams,
)
from typing import (
    Iterator,
)

ALL = AllPages()

singer_emitter = SingerEmitter(JsonEmitter())


def _to_singer(
    stream: SupportedStreams, page: ApiData
) -> Iterator[SingerRecord]:
    if isinstance(page.data, list):
        return (SingerRecord(stream.value.lower(), item) for item in page.data)
    return iter([SingerRecord(stream.value.lower(), page.data)])


def _emit_pages(stream: SupportedStreams, pages: Iterator[ApiData]) -> None:
    for page in pages:
        for item in _to_singer(stream, page):
            singer_emitter.emit(item)


def _stream_data(
    stream: SupportedStreams,
    pages: IO[Iterator[ApiData]],
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
        SupportedStreams.PROJECTS,
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


def all_event_fields(api: ApiClient) -> None:
    orgs_io = api.user.list_orgs_id(ALL)
    client = api.user.client
    _stream_data(
        SupportedStreams.EVENT_FIELDS,
        orgs_io.bind(partial(OrgsApi.list_orgs_projs_id, client)).bind(
            partial(ProjectsApi.list_projs_event_fields, client)
        ),
    )


def all_pivots(api: ApiClient) -> None:
    orgs_io = api.user.list_orgs_id(ALL)
    client = api.user.client
    _stream_data(
        SupportedStreams.PIVOTS,
        orgs_io.bind(partial(OrgsApi.list_orgs_projs_id, client)).bind(
            partial(ProjectsApi.list_projs_pivots, client)
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


def all_trends(api: ApiClient) -> None:
    orgs_io = api.user.list_orgs_id(ALL)
    client = api.user.client
    _stream_data(
        SupportedStreams.STABILITY_TREND,
        orgs_io.bind(partial(OrgsApi.list_orgs_projs_id, client)).bind(
            partial(ProjectsApi.list_projs_trends, client)
        ),
    )


__all__ = [
    "SupportedStreams",
]
