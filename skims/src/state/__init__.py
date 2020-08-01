# Standard library
from os import (
    makedirs,
)
from os.path import (
    join,
)
from pickle import (  # nosec
    UnpicklingError,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    Optional,
    Tuple,
    TypeVar,
)

# Third party libraries
import aiofiles

# Local libraries
from utils.encodings import (
    py_dumps,
    py_loads,
)
from utils.crypto import (
    get_hash,
)
from utils.function import (
    get_bound_arguments,
)


# Constants
TVar = TypeVar('TVar')
STATE_FOLDER: str = '.skims'
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


async def cache_store(key: Any, value: Any) -> None:
    obj_id: bytes = await get_obj_id(key)
    obj_stream: bytes = await py_dumps(value)
    obj_location: str = join(CACHE_FOLDER, obj_id.hex())

    async with aiofiles.open(obj_location, mode='wb') as obj_store:
        await obj_store.write(obj_stream)


async def caching(
    function_cache_keys: Optional[Tuple[str, ...]],
    function: Callable[..., Awaitable[TVar]],
    *args: Any,
    **kwargs: Any,
) -> TVar:
    arguments = get_bound_arguments(function, *args, **kwargs).arguments

    # Compute a cache key based on the hand-picked arguments provided
    cache_key = {
        '__module__': function.__module__,
        '__name__': function.__name__,
    }
    for function_arg in function_cache_keys or arguments.keys():
        cache_key[function_arg] = arguments[function_arg]

    try:
        cache_value: TVar = await cache_read(cache_key)
    except (FileNotFoundError, UnpicklingError):
        cache_value = await function(*args, **kwargs)
        await cache_store(cache_key, cache_value)

    return cache_value


async def caching_all_arguments(
    function: Callable[..., Awaitable[TVar]],
    *args: Any,
    **kwargs: Any,
) -> TVar:
    return await caching(None, function, *args, **kwargs)
