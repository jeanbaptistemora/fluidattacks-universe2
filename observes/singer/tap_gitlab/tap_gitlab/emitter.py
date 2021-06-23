from __future__ import (
    annotations,
)

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
from returns.primitives.types import (
    Immutable,
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
from tap_gitlab.state import (
    JobStreamState,
    MrStreamState,
)
from tap_gitlab.streams import (
    ApiPage,
    JobStream,
    MrStream,
    SupportedStreams,
)
from typing import (
    Iterator,
    Optional,
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


class Emitter(Immutable):
    api: ApiClient
    max_pages: int

    def __new__(cls, creds: Credentials, max_pages: int = 10) -> Emitter:
        self = object.__new__(cls)
        object.__setattr__(self, "api", ApiClient(creds))
        object.__setattr__(self, "max_pages", max_pages)
        return self

    def emit_mrs(
        self, stream: MrStream, _state: Optional[MrStreamState] = None
    ) -> None:
        start = PageId(datetime.now(pytz.utc), 100)
        pages = (
            self.api.project(stream.project)
            .mrs(stream.scope, stream.mr_state)
            .list_all_updated_before(start)
        )
        _stream_data(SupportedStreams.MERGE_REQUESTS, pages, self.max_pages)

    def emit_jobs(
        self, stream: JobStream, _state: Optional[JobStreamState] = None
    ) -> None:
        start = PageId(1, 100)
        pages = (
            self.api.project(stream.project)
            .jobs(list(stream.scopes))
            .list_all(start)
        )
        _stream_data(SupportedStreams.JOBS, pages, self.max_pages)
