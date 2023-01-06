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
Tfun = TypeVar("Tfun", bound=Callable[..., Any])


def never_concurrent(function: Tfun) -> Tfun:
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

    return cast(Tfun, wrapper)
