# Standard libraries
import time
from typing import (
    Callable,
    Optional,
    TypeVar,
)

# Third party libraries
from delighted.errors import (
    TooManyRequestsError,
)


class MaxRetriesReached(Exception):
    pass


RType = TypeVar('RType')


def handle_rate_limit(
    request: Callable[[], RType],
    max_retries: Optional[int]
) -> RType:
    retries = 0
    retries_limit = max_retries if max_retries else float('inf')
    while retries < retries_limit:
        try:
            return request()
        except TooManyRequestsError as error:
            time.sleep(error.retry_after)
            retries = retries + 1
    raise MaxRetriesReached()
