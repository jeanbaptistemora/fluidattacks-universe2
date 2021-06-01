# pylint: skip-file

import logging
from requests.exceptions import (
    HTTPError,
)
from requests.models import (
    Response,
)
from returns.curry import (
    partial,
)
from returns.io import (
    IO,
    IOResult,
)
from returns.pipeline import (
    is_successful,
)
import time
from typing import (
    Callable,
)


class MaxRetriesReached(Exception):
    pass


LOG = logging.getLogger(__name__)
RawResponse = IOResult[Response, HTTPError]


def _retry_request(
    retry_num: int,
    request: Callable[[], RawResponse],
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


def handle_rate_limit(
    request: Callable[[], RawResponse],
    max_retries: int,
) -> IO[Response]:
    retries = 0
    while retries < max_retries:
        retries = retries + 1
        result = request().lash(partial(_retry_request, retries, request))
        if is_successful(result):
            return result.unwrap()
    raise MaxRetriesReached()
