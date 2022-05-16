# pylint: skip-file

from dataclasses import (
    dataclass,
)
from returns.io import (
    IO,
)
from returns.result import (
    Failure,
    Result,
    Success,
)
from singer_io import (
    factory,
)
from singer_io.singer import (
    SingerRecord,
)
from tap_gitlab.streams import (
    ApiPage,
    SupportedStreams,
)
from typing import (
    Iterator,
    TypeVar,
)

ApiPageType = TypeVar("ApiPageType", bound=ApiPage)


@dataclass(frozen=True)
class PageEmitter:
    stream: SupportedStreams

    def _to_singer(self, page: ApiPage) -> Iterator[SingerRecord]:
        return (
            SingerRecord(self.stream.value.lower(), item) for item in page.data
        )

    def emit(self, page: ApiPage) -> IO[None]:
        for item in self._to_singer(page):
            factory.emit(item)
        return IO(None)


@dataclass(frozen=True)
class PagesEmitter:
    page_emitter: PageEmitter
    max_pages: int

    def _emit_pages(self, pages: Iterator[ApiPage]) -> None:
        count = 0
        for page in pages:
            if count >= self.max_pages:
                break
            self.page_emitter.emit(page)
            count = count + 1

    def old_stream_data(self, pages: IO[Iterator[ApiPage]]) -> None:
        pages.map(self._emit_pages)

    def emit(
        self,
        pages: Iterator[ApiPageType],
        emitted_pages: int,
    ) -> Result[int, ApiPageType]:
        count = emitted_pages
        for page in pages:
            if count >= self.max_pages:
                return Failure(page)
            self.page_emitter.emit(page)
            count = count + 1
        return Success(count)
