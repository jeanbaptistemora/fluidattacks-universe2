from datetime import (
    datetime,
)
from enum import (
    Enum,
)
from paginator.pages import (
    PageId,
)
import pytz
from returns.curry import (
    partial,
)
from returns.io import (
    IO,
)
from singer_io import (
    factory,
)
from singer_io.singer import (
    SingerRecord,
)
from tap_gitlab.api.client import (
    ApiClient,
)
from tap_gitlab.api.projects.ids import (
    ProjectId,
)
from tap_gitlab.api.projects.merge_requests.data_page import (
    MrPage,
)
from typing import (
    Iterator,
)


class SupportedStreams(Enum):
    MERGE_REQUESTS = "MERGE_REQUESTS"


def _to_singer(
    stream: SupportedStreams, page: MrPage
) -> Iterator[SingerRecord]:
    return (SingerRecord(stream.value.lower(), item) for item in page.data)


def _emit_pages(stream: SupportedStreams, pages: Iterator[MrPage]) -> None:
    for page in pages:
        for item in _to_singer(stream, page):
            factory.emit(item)


def _stream_data(
    stream: SupportedStreams,
    pages: IO[Iterator[MrPage]],
) -> None:
    pages.map(partial(_emit_pages, stream))


def all_mrs(api: ApiClient, project: str) -> None:
    start = PageId(datetime.now(pytz.utc), 100)
    pages = api.project(
        ProjectId.from_name(project)
    ).mrs.list_all_updated_before(start)
    _stream_data(SupportedStreams.MERGE_REQUESTS, pages)
