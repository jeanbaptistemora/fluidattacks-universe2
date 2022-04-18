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
from paginator.raw_client.patch import (
    Patch,
)
from requests.exceptions import (  # type: ignore
    HTTPError,
)
from requests.models import (  # type: ignore
    Response,
)
from returns.io import (
    IO,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from tap_gitlab.api.auth import (
    Credentials,
)
from typing import (
    Any,
    Dict,
    NamedTuple,
    Optional,
)
from utils_logger import (
    DEBUG,
)

LOG = logging.getLogger(__name__)
API_URL_BASE = "https://gitlab.com/api/v4"


def _error_handler(
    retry_num: int,
    error: HTTPError,
) -> HTTPError:
    response: Response = error.response
    if response.status_code in (
        500,
        502,
    ):
        items = response.json()
        LOG.info("Retry #%s response: %s", retry_num, items)
    else:
        raise error
    return error


def build_raw_client(creds: Credentials) -> RawClient:
    headers = {"Private-Token": creds.api_key}
    return RawClient(API_URL_BASE, headers, 150, Patch(_error_handler))


class PageClient(NamedTuple):
    raw_client: RawClient

    def get(
        self,
        endpoint: str,
        params: Dict[str, Any],
        page: Optional[PageId[int]] = None,
    ) -> IO[Response]:
        _params = params.copy()
        if page:
            if _params.get("page") or _params.get("per_page"):
                LOG.warning("Overwriting params `page` and/or `per_page`")
            _params["page"] = page.page
            _params["per_page"] = page.per_page
        LOG.debug("GET\n\tendpoint: %s\n\tparams: %s", endpoint, _params)
        response = self.raw_client.get(endpoint, _params)
        if DEBUG:
            items = unsafe_perform_io(response).json()
            LOG.debug(
                "%s, #items=%s, json: %s",
                response,
                len(items),
                str(items)[0:200],
            )
        return response


def build_page_client(creds: Credentials) -> PageClient:
    client = build_raw_client(creds)
    return PageClient(client)
