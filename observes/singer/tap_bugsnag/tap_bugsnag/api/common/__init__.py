# pylint: skip-file
# Standard libraries
from itertools import chain
from typing import (
    Callable,
    Iterator,
    List,
    TypeVar,
)

# Third party libraries
from requests.models import Response
from returns.io import IO
from returns.maybe import Maybe
from returns.unsafe import unsafe_perform_io

# Local libraries
from paginator.object_index import PageResult
from singer_io.common import JSON
from tap_bugsnag.api.common import extractor

_Data = TypeVar("_Data")


def typed_page_builder(
    response: IO[Response], transform: Callable[[List[JSON]], _Data]
) -> IO[Maybe[PageResult[_Data]]]:
    def _from_response(response: Response) -> Maybe[PageResult[_Data]]:
        raw = extractor.from_response(response)
        return raw.map(
            lambda p_result: PageResult(
                transform(p_result.data),
                p_result.next_item,
                p_result.total_items,
            )
        )

    return response.map(_from_response)


def fold(items: Iterator[IO[Iterator[_Data]]]) -> IO[Iterator[_Data]]:
    def rm_io(items: IO[Iterator[_Data]]) -> Iterator[_Data]:
        return unsafe_perform_io(items)

    raw = map(rm_io, items)
    return IO(chain.from_iterable(raw))
