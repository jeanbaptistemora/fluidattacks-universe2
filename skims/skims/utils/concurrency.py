# Standard library
from asyncio import (
    Lock,
)
import functools
from typing import (
    Any,
    Callable,
    cast,
    TypeVar,
)

# Constants
TFun = TypeVar('TFun', bound=Callable[..., Any])


def never_concurrent(function: TFun) -> TFun:
    """Ensure the decorated function runs at max once at any point in time.

    :param function: Function to decorate
    :type function: TFun
    :return: A function capped to be executed at most once at any point in time
    :rtype: TFun
    """
    lock = Lock()

    @functools.wraps(function)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        async with lock:
            return await function(*args, **kwargs)

    return cast(TFun, wrapper)
