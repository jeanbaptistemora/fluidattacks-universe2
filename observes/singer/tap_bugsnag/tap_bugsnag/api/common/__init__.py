# pylint: skip-file

from itertools import (
    chain,
)
from paginator.object_index import (
    PageResult,
)
from requests.models import (  # type: ignore
    Response,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from singer_io.singer2.json import (
    JsonObj,
)
from tap_bugsnag.api.common import (
    extractor,
)
from typing import (
    Callable,
    Iterator,
    List,
    TypeVar,
)

_Data = TypeVar("_Data")


class UnexpectedEmptyData(Exception):
    pass


def typed_page_builder(
    response: IO[Response], transform: Callable[[List[JsonObj]], _Data]
) -> IO[Maybe[PageResult[str, _Data]]]:
    def _from_response(response: Response) -> Maybe[PageResult[str, _Data]]:
        raw = extractor.from_response(response)
        return raw.map(
            lambda p_result: PageResult(
                transform(p_result.data),
                p_result.next_item,
                p_result.total_items,
            )
        )

    return response.map(_from_response)


def fold(items: Iterator[IO[_Data]]) -> IO[Iterator[_Data]]:
    raw: Iterator[_Data] = map(unsafe_perform_io, items)
    return IO(raw)


def fold_and_chain(
    items: Iterator[IO[Iterator[_Data]]],
) -> IO[Iterator[_Data]]:
    raw = fold(items)
    return raw.map(chain.from_iterable)
