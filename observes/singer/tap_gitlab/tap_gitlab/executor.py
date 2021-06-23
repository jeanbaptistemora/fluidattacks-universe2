from datetime import (
    datetime,
)
import logging
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
from tap_gitlab.api.auth import (
    Credentials,
)
from tap_gitlab.api.client import (
    ApiClient,
)
from tap_gitlab.api.projects.ids import (
    ProjectId,
)
from tap_gitlab.streams import (
    ApiPage,
    SupportedStreams,
)
from typing import (
    Iterator,
    Union,
)

LOG = logging.getLogger(__name__)


def _to_singer(
    stream: SupportedStreams, page: ApiPage
) -> Iterator[SingerRecord]:
    return (SingerRecord(stream.value.lower(), item) for item in page.data)


def _emit_pages(
    stream: SupportedStreams, max_pages: int, pages: Iterator[ApiPage]
) -> None:
    count = 0
    for page in pages:
        if count >= max_pages:
            break
        for item in _to_singer(stream, page):
            factory.emit(item)
        count = count + 1


def _stream_data(
    stream: SupportedStreams, pages: IO[Iterator[ApiPage]], max_pages: int
) -> None:
    pages.map(partial(_emit_pages, stream, max_pages))


def all_mrs(api: ApiClient, project: str, max_pages: int) -> None:
    start = PageId(datetime.now(pytz.utc), 100)
    pages = (
        api.project(ProjectId.from_name(project))
        .mrs()
        .list_all_updated_before(start)
    )
    _stream_data(SupportedStreams.MERGE_REQUESTS, pages, max_pages)


def all_jobs(api: ApiClient, project: str, max_pages: int) -> None:
    start = PageId(1, 100)
    pages = api.project(ProjectId.from_name(project)).jobs().list_all(start)
    _stream_data(SupportedStreams.JOBS, pages, max_pages)


def emit(
    creds: Credentials,
    target_stream: Union[str, SupportedStreams],
    project: str,
    max_pages: int,
) -> None:
    _target_stream = (
        SupportedStreams(target_stream)
        if isinstance(target_stream, str)
        else target_stream
    )
    client = ApiClient(creds)
    if _target_stream == SupportedStreams.JOBS:
        LOG.info("Executing stream: %s", _target_stream)
        all_jobs(client, project, max_pages)
    elif _target_stream == SupportedStreams.MERGE_REQUESTS:
        LOG.info("Executing stream: %s", _target_stream)
        all_mrs(client, project, max_pages)
    else:
        raise NotImplementedError(f"for {_target_stream}")


def stream_all(creds: Credentials, project: str, max_pages: int) -> None:
    for target in SupportedStreams:
        emit(creds, target, project, max_pages)
