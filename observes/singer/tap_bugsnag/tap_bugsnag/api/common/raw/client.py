from __future__ import (
    annotations,
)

import logging
from paginator.raw_client import (
    RawClient,
)
from paginator.raw_client.handlers import (
    RawResponse,
)
from paginator.raw_client.patch import (
    Patch,
)
from requests.exceptions import (
    HTTPError,
)
from requests.models import (
    Response,
)
from tap_bugsnag.api.auth import (
    Credentials,
)
import time
from typing import (
    Callable,
)

API_URL_BASE = "https://api.bugsnag.com"
LOG = logging.getLogger(__name__)


def _retry_request(
    request: Callable[[], RawResponse],
    retry_num: int,
    error: HTTPError,
) -> RawResponse:
    response: Response = error.response
    if response.status_code == 429:
        wait_time = response.headers["Retry-After"]
        LOG.info("Api rate limit reached. Waiting %ss", wait_time)
        time.sleep(int(wait_time))
        LOG.info("Retry #%s", retry_num)
    else:
        raise error
    return request()


def build_raw_client(creds: Credentials) -> RawClient:
    headers = {"Authorization": f"token {creds.api_key}", "X-Version": "2"}
    return RawClient(API_URL_BASE, headers, 5, Patch(_retry_request))
