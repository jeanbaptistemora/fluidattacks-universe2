# pylint: skip-file
# Standard libraries

# Third party libraries
from typing import Callable, NamedTuple, Union
from requests.exceptions import HTTPError
from requests.models import Response
from returns.maybe import Maybe
from returns.io import (
    IOFailure,
    IOResult,
    IOSuccess,
)

# Local libraries
from paginator.object_index import (
    PageId,
)
from tap_bugsnag.api.common.raw.client import (
    Client,
)


RawResponse = IOResult[Response, HTTPError]


def _extract_http_error(response: Response) -> Maybe[HTTPError]:
    try:
        response.raise_for_status()
        return Maybe.empty
    except HTTPError as error:
        return Maybe.from_value(error)


def _get(client: Client, endpoint: str, page: PageId) -> RawResponse:
    if page.page == "":
        response = client.get(
            endpoint,
            {"per_page": page.per_page},
        )
    response = client.get(
        endpoint,
        {"offset": page.page, "per_page": page.per_page},
    )
    error = _extract_http_error(response)
    if error == Maybe.empty:
        return IOSuccess(response)
    return IOFailure(error.unwrap())


def list_orgs(client: Client, page: PageId) -> RawResponse:
    return _get(client, "/user/organizations", page)


def list_projects(client: Client, page: PageId, org_id: str) -> RawResponse:
    return _get(client, f"/organizations/{org_id}/projects", page)
