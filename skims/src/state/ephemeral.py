# Standard library
from os import (
    makedirs,
)
from os.path import (
    join,
)
from tempfile import (
    mkdtemp,
)
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Tuple,
)

# Local libraries
from state import (
    STATE_FOLDER,
)
from state.common import (
    retrieve_object,
    store_object,
)
from utils.fs import (
    rmdir,
    recurse_dir,
)

# Constants
EPHEMERAL: str = join(STATE_FOLDER, 'ephemeral')
ClearFunction = Callable[[], Awaitable[None]]
StoreFunction = Callable[[Any, Any], Awaitable[None]]
IteratorFunction = Callable[[], AsyncIterator[Any]]

# Side effects
makedirs(EPHEMERAL, mode=0o700, exist_ok=True)


def get_ephemeral_store() -> Tuple[
    ClearFunction,
    StoreFunction,
    IteratorFunction,
]:
    """Create an ephemeral store of Python objects on-disk.

    :return: A tuple of store and iterate functions
    :rtype: Tuple[ClearFunction, StoreFunction, IteratorFunction]
    """
    folder: str = mkdtemp(dir=EPHEMERAL)

    async def clear() -> None:
        await rmdir(folder)

    async def store(key: Any, obj: Any) -> None:
        await store_object(folder, key, obj)

    async def iterate() -> AsyncIterator[Any]:
        for object_key in await recurse_dir(folder):
            yield await retrieve_object(folder, object_key)

    return clear, store, iterate
