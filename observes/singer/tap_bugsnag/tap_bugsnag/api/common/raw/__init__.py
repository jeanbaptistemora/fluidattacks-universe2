# pylint: skip-file
# Standard libraries
from __future__ import annotations
import logging
from typing import (
    NamedTuple,
)

# Third party libraries
from requests.exceptions import HTTPError
from requests.models import Response
from returns.io import (
    IO,
    IOFailure,
    IOSuccess,
)
from returns.maybe import Maybe

# Local libraries
from paginator.object_index import (
    PageId,
)
from singer_io.common import JSON
from tap_bugsnag.api.auth import Credentials
from tap_bugsnag.api.common.raw import handlers
from tap_bugsnag.api.common.raw.handlers import RawResponse
from tap_bugsnag.api.common.raw.client import (
    Client,
)


LOG = logging.getLogger(__name__)


def _extract_http_error(response: Response) -> Maybe[HTTPError]:
    try:
        response.raise_for_status()
        return Maybe.empty
    except HTTPError as error:
        return Maybe.from_value(error)


def _get(
    client: Client, endpoint: str, page: PageId, params: JSON = {}
) -> RawResponse:
    _params: JSON = {"per_page": page.per_page, **params}
    if page.page:
        _params["offset"] = page.page
    response = client.get(
        endpoint,
        _params,
    )
    error = _extract_http_error(response)
    if error == Maybe.empty:
        return IOSuccess(response)
    return IOFailure(error.unwrap())


def _handled_get(
    client: Client, endpoint: str, page: PageId, params: JSON = {}
) -> IO[Response]:
    return handlers.handle_rate_limit(
        lambda: _get(client, endpoint, page, params), 5
    )


def _debug_log(resource: str, page: PageId, response: IO[Response]) -> None:
    LOG.debug(
        "%s [%s]: %s\n\theaders: %s\n\tdata: %s",
        resource,
        page,
        response,
        response.map(lambda x: x.headers),
        response.map(lambda x: str(x.json())[0:100] + "..."),
    )


class RawApi(NamedTuple):
    client: Client

    def list_orgs(self, page: PageId) -> IO[Response]:
        response = _handled_get(self.client, "/user/organizations", page)
        _debug_log("organizations", page, response)
        return response

    def list_projects(self, page: PageId, org_id: str) -> IO[Response]:
        response = _handled_get(
            self.client, f"/organizations/{org_id}/projects", page
        )
        _debug_log("projects", page, response)
        return response

    def list_errors(self, page: PageId, project_id: str) -> IO[Response]:
        response = _handled_get(
            self.client,
            f"/projects/{project_id}/errors",
            page,
            {"sort": "unsorted"},
        )
        _debug_log("errors", page, response)
        return response

    @classmethod
    def from_client(cls, client: Client) -> RawApi:
        return cls(client)

    @classmethod
    def new(cls, creds: Credentials) -> RawApi:
        return RawApi.from_client(Client.new(creds))
