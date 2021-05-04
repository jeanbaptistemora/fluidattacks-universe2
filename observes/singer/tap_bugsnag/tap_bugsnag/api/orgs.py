# pylint: skip-file
# Standard libraries
from __future__ import annotations
from typing import (
    Any,
    Iterator,
    List,
    NamedTuple,
    TypeVar,
)

# Third party libraries
from requests.models import Response
from returns.curry import partial
from returns.io import IO
from returns.maybe import Maybe

# Local libraries
from paginator import (
    AllPages,
)
from paginator.object_index import (
    PageId,
    PageOrAll,
    PageResult,
    io_get_until_end,
)
from singer_io import JSON
from tap_bugsnag.api.common.raw import RawApi


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


class OrgsPage(NamedTuple):
    data: List[JSON]

    @classmethod
    def new(cls, raw: RawApi, page: PageId) -> IO[Maybe[PageResult[OrgsPage]]]:
        def _from_response(response: Response) -> Maybe[PageResult[OrgsPage]]:
            data = response.json()
            if not data:
                return Maybe.empty
            next_item = response.headers["Link"]
            total: Maybe[int] = Maybe.from_optional(
                response.headers.get("X-Total-Count", None)
            ).map(int)
            _guarantee_list_json_type(data)
            return Maybe.from_value(PageResult(cls(data), next_item, total))

        data = raw.list_orgs(page)
        return data.map(_from_response)


_Data = TypeVar("_Data")


def _extract_result_data(
    results: Iterator[PageResult[_Data]],
) -> Iterator[_Data]:
    return iter(map(lambda result: result.data, results))


def _list_orgs(
    client: RawApi,
    page: PageOrAll,
) -> IO[Iterator[OrgsPage]]:
    if isinstance(page, AllPages):
        result = io_get_until_end(
            PageId("", 100), partial(OrgsPage.new, client)
        )
        return result.map(_extract_result_data)
    return OrgsPage.new(client, page).map(
        lambda page: page.map(lambda result: iter([result.data])).or_else_call(
            lambda: iter([])
        )
    )


class OrgsApi(NamedTuple):
    client: RawApi

    @classmethod
    def new(cls, client: RawApi) -> OrgsApi:
        return cls(client)

    def list_orgs(self, page: PageOrAll) -> IO[Iterator[OrgsPage]]:
        return _list_orgs(self.client, page)
