# Standard libraries
from typing import (
    Any,
    Callable,
    Iterator,
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


RawApiResult = IOResult[Iterator[JSON], RateLimitError]


def _wrap_manyreqs_error(request: Callable[[], Any]) -> RawApiResult:
    try:
        return IOSuccess(request())
    except TooManyRequestsError as error:
        raise RateLimitError(error)


def _call_paged_resource(
    request: Callable[..., Any],
    client: Client,
    page: PageId,
) -> RawApiResult:
    return _wrap_manyreqs_error(
        lambda: request(
            client=client,
            page=page.page,
            per_page=page.per_page
        )
    )


def list_bounced(client: Client, page: PageId) -> RawApiResult:
    return _call_paged_resource(
        delighted.Bounce.all, client, page
    )


def list_surveys(client: Client, page: PageId) -> RawApiResult:
    return _call_paged_resource(
        delighted.SurveyResponse.all, client, page
    )


def list_unsubscribed(client: Client, page: PageId) -> RawApiResult:
    return _call_paged_resource(
        delighted.Unsubscribe.all, client, page
    )
