# pylint: skip-file

import logging
from returns.curry import (
    partial,
)
from returns.io import (
    IO,
    IOResult,
)
from tap_delighted.api.common.raw import (
    RateLimitError,
    RawApiResult,
)
import time
from typing import (
    Callable,
    TypeVar,
)


class MaxRetriesReached(Exception):
    pass


DataType = TypeVar("DataType")
ApiResult = IOResult[DataType, MaxRetriesReached]
LOG = logging.getLogger(__name__)


def retry_request(
    retry_num: int,
    request: Callable[[], RawApiResult[DataType]],
    error: RateLimitError,
) -> ApiResult[DataType]:  # type: ignore
    wait_time = error.retry_after
    LOG.info("Api rate limit reached. Waiting %ss", wait_time)
    time.sleep(wait_time)
    LOG.info("Retry #%s", retry_num)
    return request()


def handle_rate_limit(
    request: Callable[[], RawApiResult[DataType]],
    max_retries: int,
) -> ApiResult:  # type: ignore
    retries = 0
    while retries < max_retries:
        retries = retries + 1
        result = request().lash(partial(retry_request, retries, request))
        success = result.map(lambda _: True).value_or(False)
        if success == IO(True):
            return result
    raise MaxRetriesReached()
