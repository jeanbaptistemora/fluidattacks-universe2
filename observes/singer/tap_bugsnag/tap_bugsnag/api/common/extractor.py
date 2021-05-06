# pylint: skip-file
# Standard libraries
from __future__ import (
    annotations,
)
import re
from typing import (
    Any,
    Callable,
    Iterator,
    List,
    Type,
    TypeVar,
)


# Third party libraries
from requests.models import Response
from returns.io import IO
from returns.maybe import Maybe

# Local libraries
from paginator import (
    AllPages,
)
from paginator.object_index import (
    PageGetterIO,
    PageOrAll,
    PageResult,
)
from singer_io.common import JSON


_Data = TypeVar("_Data")


class TypeCheckFail(Exception):
    pass


def _guarantee_list_json_type(raw: Any) -> None:
    if all(
        [
            isinstance(raw, list),
            all(map(lambda item: isinstance(item, dict), raw)),
        ]
    ):
        return None
    raise TypeCheckFail(f"raw is not a List[JSON]. raw: {raw}")


def _extract_offset(link: str) -> Maybe[str]:
    match = Maybe.from_optional(re.match("offset=([a-zA-Z0-9]+)", link))
    is_next = re.match('rel="next"', link)
    return match.map(lambda x: x.group(1)) if is_next else Maybe.empty


def _extract_result_data(
    results: Iterator[PageResult[_Data]],
) -> Iterator[_Data]:
    return iter(map(lambda result: result.data, results))


def from_response(response: Response) -> Maybe[PageResult[List[JSON]]]:
    data = response.json()
    if not data:
        return Maybe.empty
    next_item = _extract_offset(response.headers["Link"])
    total: Maybe[int] = Maybe.from_optional(
        response.headers.get("X-Total-Count", None)
    ).map(int)
    _guarantee_list_json_type(data)
    return Maybe.from_value(PageResult(data, next_item, total))


def extract_page(
    get_all: Callable[[], IO[Iterator[PageResult[_Data]]]],
    getter: PageGetterIO[_Data],
    page: PageOrAll,
) -> IO[Iterator[_Data]]:
    if isinstance(page, AllPages):
        return get_all().map(_extract_result_data)
    return getter(page).map(
        lambda page: page.map(lambda result: iter([result.data])).or_else_call(
            lambda: iter([])
        )
    )
