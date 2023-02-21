# pylint: skip-file

from collections.abc import (
    Callable,
)
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


class MaxRetriesReached(Exception):
    pass


RawResponse = IOResult[Response, HTTPError]
RequestCall = Callable[[], RawResponse]
ErrorHandler = Callable[[int, HTTPError], HTTPError]


def insistent_call(
    request: RequestCall,
    handler: ErrorHandler,
    max_retries: int,
) -> IO[Response]:
    retries = 0
    while retries < max_retries:
        retries = retries + 1
        result = request().alt(partial(handler, retries))
        if is_successful(result):
            return result.unwrap()
    raise MaxRetriesReached()
