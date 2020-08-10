# Standard library
import functools
from os import (
    makedirs,
)
from os.path import (
    expanduser,
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

# Third party libraries
import aiofiles

# Local libraries
from utils.crypto import (
    get_hash,
)
from utils.serialization import (
    dump as py_dumps,
    load as py_loads,
    LoadError,
)


# Constants
TFunc = TypeVar('TFunc', bound=Callable[..., Any])
TVar = TypeVar('TVar')
STATE_FOLDER: str = expanduser('~/.skims')
CACHE_FOLDER: str = join(STATE_FOLDER, 'cache')

# Side effects
makedirs(CACHE_FOLDER, mode=0o700, exist_ok=True)
makedirs(STATE_FOLDER, mode=0o700, exist_ok=True)


async def get_obj_id(obj: Any) -> bytes:
    return await get_hash(await py_dumps(obj))


async def cache_read(key: Any) -> Any:
    obj_id: bytes = await get_obj_id(key)
    obj_location: str = join(CACHE_FOLDER, obj_id.hex())

    async with aiofiles.open(obj_location, mode='rb') as obj_store:
        obj_stream: bytes = await obj_store.read()
        obj: Any = await py_loads(obj_stream)

    return obj


async def cache_store(key: Any, value: Any, ttl: Optional[int] = None) -> None:
    obj_id: bytes = await get_obj_id(key)
    obj_stream: bytes = await py_dumps(value, ttl=ttl)
    obj_location: str = join(CACHE_FOLDER, obj_id.hex())

    async with aiofiles.open(obj_location, mode='wb') as obj_store:
        await obj_store.write(obj_stream)


async def cache(
    function: Callable[..., Awaitable[TVar]],
    ttl: Optional[int],
    *args: Any,
    **kwargs: Any,
) -> TVar:
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

    def decorator(function: TFunc) -> TFunc:

        @functools.wraps(function)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            return await cache(function, ttl, *args, **kwargs)

        return cast(TFunc, wrapper)

    return decorator
