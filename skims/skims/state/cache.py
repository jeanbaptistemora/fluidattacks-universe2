from aioextensions import (
    in_thread,
)
import asyncio
from ctx import (
    CTX,
    STATE_FOLDER,
)
import functools
from os import (
    makedirs,
)
from os.path import (
    join,
)
from safe_pickle import (
    LoadError,
)
from state.common import (
    retrieve_object,
    store_object,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    cast,
    Optional,
    TypeVar,
)

# Constants
CACHE_FOLDER: str = join(STATE_FOLDER, "cache")
TFunc = TypeVar("TFunc", bound=Callable[..., Any])
TVar = TypeVar("TVar")

# Side effects
makedirs(CACHE_FOLDER, mode=0o700, exist_ok=True)


def cache_read(key: Any) -> Any:
    """Retrieve an entry from the cache.

    :param key: Key that identifies the value to be read
    :type key: Any
    :return: The value that is hold under the specified key
    :rtype: Any
    """
    return retrieve_object(CACHE_FOLDER, key)


def cache_store(key: Any, value: Any, ttl: Optional[int] = None) -> None:
    """Store an entry in the cache.

    :param key: Key under the value is to be aliased
    :type key: Any
    :param value: Value to store
    :type value: Any
    :param ttl: Time to live in seconds, defaults to None
    :type ttl: Optional[int], optional
    """
    store_object(CACHE_FOLDER, key, value, ttl)


def _cache_blocking(
    function: Callable[..., TVar],
    ttl: Optional[int],
    *args: Any,
    **kwargs: Any,
) -> TVar:
    """Cache function(\\*args, \\*\\*kwargs) on-disk for ttl seconds."""
    cache_key = (
        function.__module__,
        function.__name__,
        CTX.config.namespace,
        args,
        kwargs,
    )

    try:
        cache_value: TVar = cache_read(cache_key)
    except (FileNotFoundError, LoadError):
        cache_value = function(*args, **kwargs)
        cache_store(cache_key, cache_value, ttl=ttl)

    return cache_value


async def _cache(
    function: Callable[..., Awaitable[TVar]],
    ttl: Optional[int],
    *args: Any,
    **kwargs: Any,
) -> TVar:
    """Cache function(\\*args, \\*\\*kwargs) on-disk for ttl seconds."""
    cache_key = (
        function.__module__,
        function.__name__,
        CTX.config.namespace,
        args,
        kwargs,
    )

    try:
        cache_value: TVar = await in_thread(cache_read, cache_key)
    except (FileNotFoundError, LoadError):
        cache_value = await function(*args, **kwargs)
        await in_thread(cache_store, cache_key, cache_value, ttl=ttl)

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

        if asyncio.iscoroutinefunction(function):

            @functools.wraps(function)
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                return await _cache(function, ttl, *args, **kwargs)

        elif callable(function):

            @functools.wraps(function)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                return _cache_blocking(function, ttl, *args, **kwargs)

        else:
            raise NotImplementedError()

        return cast(TFunc, wrapper)

    return decorator


# Constants
CACHE_ETERNALLY: Callable[[TFunc], TFunc] = cache_decorator(ttl=None)
CACHE_1MONTH: Callable[[TFunc], TFunc] = cache_decorator(ttl=2419200)
CACHE_1WEEK: Callable[[TFunc], TFunc] = cache_decorator(ttl=604800)
CACHE_1DAY: Callable[[TFunc], TFunc] = cache_decorator(ttl=86400)
CACHE_1SEC: Callable[[TFunc], TFunc] = cache_decorator(ttl=1)
