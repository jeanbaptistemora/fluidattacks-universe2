# pylint: skip-file

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


RawResponse = IOResult[Response, HTTPError]
RequestCall = Callable[[], RawResponse]
RetryStrategy = Callable[[RequestCall, int, HTTPError], RawResponse]


def insistent_call(
    request: RequestCall,
    retry: RetryStrategy,
    max_retries: int,
) -> IO[Response]:
    retries = 0
    while retries < max_retries:
        retries = retries + 1
        result = request().lash(partial(retry, request, retries))
        if is_successful(result):
            return result.unwrap()
    raise MaxRetriesReached()
