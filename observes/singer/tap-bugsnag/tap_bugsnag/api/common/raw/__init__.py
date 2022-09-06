# pylint: skip-file

from __future__ import (
    annotations,
)

import logging
from paginator.pages import (
    PageId,
)
from paginator.raw_client import (
    RawClient,
)
from requests.models import (  # type: ignore
    Response,
)
from returns.io import (
    impure,
    IO,
)
from returns.maybe import (
    Maybe,
)
from returns.pipeline import (
    is_successful,
)
from tap_bugsnag.api.auth import (
    Credentials,
)
from tap_bugsnag.api.common.raw.client import (
    build_raw_client,
)
from typing import (
    Any,
    Dict,
    NamedTuple,
)

LOG = logging.getLogger(__name__)


def _get(
    client: RawClient,
    endpoint: str,
    page: Maybe[PageId],
    params: Dict[str, Any] = {},
) -> IO[Response]:
    _params = {}
    if is_successful(page):
        _page = page.unwrap()
        _params = {"per_page": _page.per_page, **params}
        if _page.page:
            _params["offset"] = _page.page
    return client.get(
        endpoint,
        _params,
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
    client: RawClient

    @classmethod
    def from_client(cls, client: RawClient) -> RawApi:
        return cls(client)

    @classmethod
    def new(cls, creds: Credentials) -> RawApi:
        return RawApi.from_client(build_raw_client(creds))

    def list_orgs(self, page: PageId) -> IO[Response]:
        _page = Maybe.from_value(page)
        response = _get(self.client, "/user/organizations", _page)
        _debug_log("organizations", _page, response)
        return response

    def list_collaborators(self, page: PageId, org_id: str) -> IO[Response]:
        _page = Maybe.from_value(page)
        response = _get(
            self.client, f"/organizations/{org_id}/collaborators", _page
        )
        _debug_log("collaborators", _page, response)
        return response

    def list_projects(self, page: PageId, org_id: str) -> IO[Response]:
        _page = Maybe.from_value(page)
        response = _get(
            self.client, f"/organizations/{org_id}/projects", _page
        )
        _debug_log("projects", _page, response)
        return response

    def list_errors(self, page: PageId, project_id: str) -> IO[Response]:
        _page = Maybe.from_value(page)
        response = _get(
            self.client,
            f"/projects/{project_id}/errors",
            _page,
            {"sort": "unsorted"},
        )
        _debug_log("errors", _page, response)
        return response

    def list_events(self, page: PageId, project_id: str) -> IO[Response]:
        _page = Maybe.from_value(page)
        response = _get(self.client, f"/projects/{project_id}/events", _page)
        _debug_log("events", _page, response)
        return response

    def list_event_fields(self, page: PageId, project_id: str) -> IO[Response]:
        _page = Maybe.from_value(page)
        response = _get(
            self.client, f"/projects/{project_id}/event_fields", _page
        )
        _debug_log("event_fields", _page, response)
        return response

    def list_pivots(self, page: PageId, project_id: str) -> IO[Response]:
        _page = Maybe.from_value(page)
        response = _get(self.client, f"/projects/{project_id}/pivots", _page)
        _debug_log("pivots", _page, response)
        return response

    def list_releases(self, page: PageId, project_id: str) -> IO[Response]:
        _page = Maybe.from_value(page)
        response = _get(self.client, f"/projects/{project_id}/releases", _page)
        _debug_log("releases", _page, response)
        return response

    def get_trend(self, project_id: str) -> IO[Response]:
        response = _get(
            self.client, f"/projects/{project_id}/stability_trend", Maybe.empty
        )
        _debug_log("trend", Maybe.empty, response)
        return response
