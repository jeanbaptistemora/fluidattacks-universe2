from __future__ import (
    annotations,
)

import logging
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
from tap_bugsnag.api.auth import (
    Credentials,
)
import time

API_URL_BASE = "https://api.bugsnag.com"
LOG = logging.getLogger(__name__)


def _error_handler(
    retry_num: int,
    error: HTTPError,
) -> HTTPError:
    response: Response = error.response
    if response.status_code == 429:
        wait_time = response.headers["Retry-After"]
        LOG.info("Api rate limit reached. Waiting %ss", wait_time)
        time.sleep(int(wait_time))
        LOG.info("Retry #%s", retry_num)
    else:
        raise error
    return error


def build_raw_client(creds: Credentials) -> RawClient:
    headers = {"Authorization": f"token {creds.api_key}", "X-Version": "2"}
    return RawClient(API_URL_BASE, headers, 5, Patch(_error_handler))
