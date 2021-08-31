# pylint: skip-file

from requests.exceptions import (  # type: ignore
    HTTPError,
)
from requests.models import (  # type: ignore
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
from typing import (
    Callable,
)


class MaxRetriesReached(Exception):
    pass


RawResponse = IOResult[Response, HTTPError]
RequestCall = Callable[[], RawResponse]  # type: ignore
ErrorHandler = Callable[[int, HTTPError], HTTPError]


def insistent_call(
    request: RequestCall,
    handler: ErrorHandler,
    max_retries: int,
) -> IO[Response]:
    retries = 0
    while retries < max_retries:
        retries = retries + 1
        result = request().alt(partial(handler, retries))  # type: ignore
        if is_successful(result):
            return result.unwrap()
    raise MaxRetriesReached()
