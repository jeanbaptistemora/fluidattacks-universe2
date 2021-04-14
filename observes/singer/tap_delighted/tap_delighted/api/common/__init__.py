# pylint: skip-file
# Standard libraries
import logging
import time
from typing import (
    Callable,
    Iterator,
    TypeVar,
)

# Third party libraries
from returns.io import (
    IO,
    IOResult,
)
from returns.curry import (
    partial,
)
# Local libraries
from tap_delighted.api.common.raw import (
    RateLimitError,
    RawApiResult,
)
from tap_delighted.common import (
    JSON,
)


class MaxRetriesReached(Exception):
    pass


DataType = TypeVar('DataType')
ApiResult = IOResult[DataType, MaxRetriesReached]
LOG = logging.getLogger(__name__)


def retry_request(
    retry_num: int,
    request: Callable[[], RawApiResult[DataType]],
    error: RateLimitError,
) -> ApiResult[DataType]:
    wait_time = error.retry_after
    LOG.info('Api rate limit reached. Waiting %ss', wait_time)
    time.sleep(wait_time)
    LOG.info('Retry #%s', retry_num)
    return request()


def handle_rate_limit(
    request: Callable[[], RawApiResult[DataType]],
    max_retries: int,
) -> ApiResult:
    retries = 0
    while retries < max_retries:
        retries = retries + 1
        result = request().lash(partial(retry_request, retries, request))
        success = result.map(lambda _: True).value_or(False)
        if success == IO(True):
            return result
    raise MaxRetriesReached()
