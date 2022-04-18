# pylint: skip-file

import delighted
from delighted import (
    Client,
)
from delighted.errors import (
    TooManyRequestsError,
)
import logging
from paginator import (
    PageId,
)
from returns.io import (
    IO,
    IOFailure,
    IOResult,
    IOSuccess,
)
from returns.pipeline import (
    pipe,
)
from singer_io.singer2.json import (
    JsonFactory,
    JsonObj,
)
from typing import (
    Any,
    Callable,
    Iterator,
    List,
    TypeVar,
)

LOG = logging.getLogger(__name__)


class RateLimitError(TooManyRequestsError):
    pass


DataType = TypeVar("DataType")
RawApiResult = IOResult[DataType, RateLimitError]
RawItem = RawApiResult[JsonObj]
RawItems = RawApiResult[List[JsonObj]]


def _wrap_manyreqs_error(
    request: Callable[[], DataType]
) -> RawApiResult[DataType]:  # type: ignore
    try:
        result = request()
        return IOSuccess(result)
    except TooManyRequestsError as error:
        return IOFailure(RateLimitError(error.response))


def _single_request(request: Callable[[], Any]) -> Callable[[], JsonObj]:
    return lambda: JsonFactory.from_any(request())


def _paged_request(request: Callable[[], Any]) -> Callable[[], List[JsonObj]]:
    return lambda: [JsonFactory.from_any(item) for item in request()]


_call_single_resource = pipe(_single_request, _wrap_manyreqs_error)
_call_paged_resource = pipe(_paged_request, _wrap_manyreqs_error)


def get_metrics(client: Client) -> RawItem:  # type: ignore
    return _call_single_resource(
        lambda: delighted.Metrics.retrieve(client=client)
    )


def list_bounced(client: Client, page: PageId) -> RawItems:  # type: ignore
    LOG.debug("raw list_bounced %s", page)
    return _call_paged_resource(
        lambda: delighted.Bounce.all(
            client=client, page=page.page, per_page=page.per_page
        )
    )


def list_people(client: Client) -> IO[Iterator[JsonObj]]:
    people = delighted.Person.list(client=client, auto_handle_rate_limits=True)
    pages = (JsonFactory.from_any(item) for item in people.auto_paging_iter())
    return IO(iter(pages))


def list_surveys(client: Client, page: PageId) -> RawItems:  # type: ignore
    return _call_paged_resource(
        lambda: delighted.SurveyResponse.all(
            client=client, page=page.page, per_page=page.per_page
        )
    )


def list_unsubscribed(
    client: Client,
    page: PageId,
) -> RawItems:  # type: ignore
    return _call_paged_resource(
        lambda: delighted.Unsubscribe.all(
            client=client, page=page.page, per_page=page.per_page
        )
    )
