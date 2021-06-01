# pylint: skip-file

from __future__ import (
    annotations,
)

import logging
from paginator.object_index import (
    PageId,
)
from requests.exceptions import (
    HTTPError,
)
from requests.models import (
    Response,
)
from returns.io import (
    impure,
    IO,
    IOFailure,
    IOSuccess,
)
from returns.maybe import (
    Maybe,
)
from returns.pipeline import (
    is_successful,
)
from singer_io.common import (
    JSON,
)
from tap_bugsnag.api.auth import (
    Credentials,
)
from tap_bugsnag.api.common.raw import (
    handlers,
)
from tap_bugsnag.api.common.raw.client import (
    Client,
)
from tap_bugsnag.api.common.raw.handlers import (
    RawResponse,
)
from typing import (
    NamedTuple,
)

LOG = logging.getLogger(__name__)


class ResponseError(HTTPError):
    def __init__(self, error: HTTPError) -> None:
        super().__init__(
            response=error.response,
            request=error.request,
        )

    def __str__(self) -> str:
        return f"{self.response.json()}"


def _extract_http_error(response: Response) -> Maybe[HTTPError]:
    try:
        response.raise_for_status()
        return Maybe.empty
    except HTTPError as error:
        return Maybe.from_value(ResponseError(error))


def _get(
    client: Client, endpoint: str, page: Maybe[PageId], params: JSON = {}
) -> RawResponse:
    _params: JSON = {}
    if is_successful(page):
        _page = page.unwrap()
        _params = {"per_page": _page.per_page, **params}
        if _page.page:
            _params["offset"] = _page.page
    response = client.get(
        endpoint,
        _params,
    )
    error = _extract_http_error(response)
    if error == Maybe.empty:
        return IOSuccess(response)
    return IOFailure(error.unwrap())


def _handled_get(
    client: Client, endpoint: str, page: Maybe[PageId], params: JSON = {}
) -> IO[Response]:
    return handlers.handle_rate_limit(
        lambda: _get(client, endpoint, page, params), 5
    )


@impure
def _debug_log(
    resource: str, page: Maybe[PageId], response: IO[Response]
) -> None:
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
        _page = Maybe.from_value(page)
        response = _handled_get(self.client, "/user/organizations", _page)
        _debug_log("organizations", _page, response)
        return response

    def list_collaborators(self, page: PageId, org_id: str) -> IO[Response]:
        _page = Maybe.from_value(page)
        response = _handled_get(
            self.client, f"/organizations/{org_id}/collaborators", _page
        )
        _debug_log("collaborators", _page, response)
        return response

    def list_projects(self, page: PageId, org_id: str) -> IO[Response]:
        _page = Maybe.from_value(page)
        response = _handled_get(
            self.client, f"/organizations/{org_id}/projects", _page
        )
        _debug_log("projects", _page, response)
        return response

    def list_errors(self, page: PageId, project_id: str) -> IO[Response]:
        _page = Maybe.from_value(page)
        response = _handled_get(
            self.client,
            f"/projects/{project_id}/errors",
            _page,
            {"sort": "unsorted"},
        )
        _debug_log("errors", _page, response)
        return response

    def list_events(self, page: PageId, project_id: str) -> IO[Response]:
        _page = Maybe.from_value(page)
        response = _handled_get(
            self.client, f"/projects/{project_id}/events", _page
        )
        _debug_log("events", _page, response)
        return response

    def list_event_fields(self, page: PageId, project_id: str) -> IO[Response]:
        _page = Maybe.from_value(page)
        response = _handled_get(
            self.client, f"/projects/{project_id}/event_fields", _page
        )
        _debug_log("event_fields", _page, response)
        return response

    def list_pivots(self, page: PageId, project_id: str) -> IO[Response]:
        _page = Maybe.from_value(page)
        response = _handled_get(
            self.client, f"/projects/{project_id}/pivots", _page
        )
        _debug_log("pivots", _page, response)
        return response

    def list_releases(self, page: PageId, project_id: str) -> IO[Response]:
        _page = Maybe.from_value(page)
        response = _handled_get(
            self.client, f"/projects/{project_id}/releases", _page
        )
        _debug_log("releases", _page, response)
        return response

    def get_trend(self, project_id: str) -> IO[Response]:
        response = _handled_get(
            self.client, f"/projects/{project_id}/stability_trend", Maybe.empty
        )
        _debug_log("trend", Maybe.empty, response)
        return response

    @classmethod
    def from_client(cls, client: Client) -> RawApi:
        return cls(client)

    @classmethod
    def new(cls, creds: Credentials) -> RawApi:
        return RawApi.from_client(Client.new(creds))
