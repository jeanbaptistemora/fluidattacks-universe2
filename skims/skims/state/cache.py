# Standard library
import functools
from os import (
    makedirs,
)
from os.path import (
    join,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    cast,
    Optional,
    TypeVar,
)

# Local libraries
from serialization import (
    LoadError,
)
from state import (
    STATE_FOLDER,
)
from state.common import (
    retrieve_object,
    store_object,
)

# Constants
CACHE_FOLDER: str = join(STATE_FOLDER, 'cache')
TFunc = TypeVar('TFunc', bound=Callable[..., Any])
TVar = TypeVar('TVar')

# Side effects
makedirs(CACHE_FOLDER, mode=0o700, exist_ok=True)


async def cache_read(key: Any) -> Any:
    """Retrieve an entry from the cache.

    :param key: Key that identifies the value to be read
    :type key: Any
    :return: The value that is hold under the specified key
    :rtype: Any
    """
    return await retrieve_object(CACHE_FOLDER, key)


async def cache_store(key: Any, value: Any, ttl: Optional[int] = None) -> None:
    """Store an entry in the cache.

    :param key: Key under the value is to be aliased
    :type key: Any
    :param value: Value to store
    :type value: Any
    :param ttl: Time to live in seconds, defaults to None
    :type ttl: Optional[int], optional
    """
    await store_object(CACHE_FOLDER, key, value, ttl)


async def cache(
    function: Callable[..., Awaitable[TVar]],
    ttl: Optional[int],
    *args: Any,
    **kwargs: Any,
) -> TVar:
    """Cache function(\\*args, \\*\\*kwargs) on-disk for ttl seconds.

    :param function: The function whose result is to be cached
    :type function: Callable[..., Awaitable[TVar]]
    :param ttl: Time to live, in seconds
    :type ttl: Optional[int]
    :return: Either the result of the evaluation, or the data retrieved from
        the cache
    :rtype: TVar
    """
    cache_key = (function.__module__, function.__name__, args, kwargs)

    try:
        cache_value: TVar = await cache_read(cache_key)
    except (FileNotFoundError, LoadError):
        cache_value = await function(*args, **kwargs)
        await cache_store(cache_key, cache_value, ttl=ttl)

    return cache_value


def cache_decorator(
    *,
    ttl: Optional[int] = None,
) -> Callable[[TFunc], TFunc]:
    """Decorate a function with an on-disk cached version.

    :param ttl: Time to live in seconds, defaults to None
    :type ttl: Optional[int], optional
    :return: A decorator
    :rtype: Callable[[TFunc], TFunc]
    """

    def decorator(function: TFunc) -> TFunc:

        @functools.wraps(function)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            return await cache(function, ttl, *args, **kwargs)

        return cast(TFunc, wrapper)

    return decorator


# Constants
CACHED_ETERNALLY: Callable[[TFunc], TFunc] = cache_decorator(ttl=None)
CACHED_1MONTH: Callable[[TFunc], TFunc] = cache_decorator(ttl=2419200)
CACHED_1WEEK: Callable[[TFunc], TFunc] = cache_decorator(ttl=604800)
CACHED_1DAY: Callable[[TFunc], TFunc] = cache_decorator(ttl=86400)
CACHED_1SEC: Callable[[TFunc], TFunc] = cache_decorator(ttl=1)
