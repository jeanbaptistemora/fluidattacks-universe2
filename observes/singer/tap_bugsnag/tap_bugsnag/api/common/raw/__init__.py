# pylint: skip-file
# Standard libraries
from __future__ import annotations
from typing import (
    NamedTuple,
)

# Third party libraries
from requests.exceptions import HTTPError
from requests.models import Response
from returns.io import (
    IO,
    IOFailure,
    IOResult,
    IOSuccess,
)
from returns.maybe import Maybe

# Local libraries
from paginator.object_index import (
    PageId,
)
from tap_bugsnag.api.common.raw import handlers
from tap_bugsnag.api.common.raw.handlers import RawResponse
from tap_bugsnag.api.common.raw.client import (
    Client,
)


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


def _handled_get(client: Client, endpoint: str, page: PageId) -> IO[Response]:
    return handlers.handle_rate_limit(lambda: _get(client, endpoint, page), 5)


class RawApi(NamedTuple):
    client: Client

    def list_orgs(self, page: PageId) -> IO[Response]:
        return _handled_get(self.client, "/user/organizations", page)

    def list_projects(self, page: PageId, org_id: str) -> IO[Response]:
        return _handled_get(
            self.client, f"/organizations/{org_id}/projects", page
        )

    @classmethod
    def new(cls, client: Client) -> RawApi:
        return cls(client)
