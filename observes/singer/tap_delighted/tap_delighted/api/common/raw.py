# pylint: skip-file
# Standard libraries
from typing import (
    Any,
    Callable,
    Iterator,
    TypeVar,
)

# Third party libraries
import delighted
from delighted import (
    Client,
)
from delighted.errors import (
    TooManyRequestsError,
)
from returns.io import (
    IO,
    IOFailure,
    IOResult,
    IOSuccess,
)

# Local libraries
from paginator import (
    PageId,
)
from tap_delighted.common import (
    JSON,
)


class RateLimitError(TooManyRequestsError):
    pass


DataType = TypeVar('DataType')
RawApiResult = IOResult[DataType, RateLimitError]
RawItem = RawApiResult[JSON]
RawItems = RawApiResult[Iterator[JSON]]


def _wrap_manyreqs_error(request: Callable[[], Any]) -> RawApiResult[Any]:
    try:
        return IOSuccess(request())
    except TooManyRequestsError as error:
        return IOFailure(RateLimitError(error.response))


def _call_paged_resource(
    request: Callable[..., Any],
    client: Client,
    page: PageId,
) -> RawItems:
    return _wrap_manyreqs_error(
        lambda: request(
            client=client,
            page=page.page,
            per_page=page.per_page
        )
    )


def _call_single_resource(
    request: Callable[..., Any],
    client: Client,
) -> RawItem:
    return _wrap_manyreqs_error(
        lambda: request(client=client)
    )


def get_metrics(client: Client) -> RawItem:
    return _call_single_resource(
        delighted.Metrics.retrieve, client
    )


def list_bounced(client: Client, page: PageId) -> RawItems:
    return _call_paged_resource(
        delighted.Bounce.all, client, page
    )


def list_people(client: Client) -> IO[Iterator[JSON]]:
    people = delighted.Person.list(
        client=client,
        auto_handle_rate_limits=True
    )
    return IO(iter(people.auto_paging_iter()))


def list_surveys(client: Client, page: PageId) -> RawItems:
    return _call_paged_resource(
        delighted.SurveyResponse.all, client, page
    )


def list_unsubscribed(client: Client, page: PageId) -> RawItems:
    return _call_paged_resource(
        delighted.Unsubscribe.all, client, page
    )
