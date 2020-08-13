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
    NamedTuple,
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
    mkdir,
    rmdir,
    recurse_dir,
)

# Constants
EPHEMERAL: str = join(STATE_FOLDER, 'ephemeral')
ClearFunction = Callable[[], Awaitable[None]]
StoreFunction = Callable[[Any], Awaitable[None]]
IteratorFunction = Callable[[], AsyncIterator[Any]]

# Side effects
makedirs(EPHEMERAL, mode=0o700, exist_ok=True)


class EphemeralStore(NamedTuple):
    clear: ClearFunction
    iterate: IteratorFunction
    store: StoreFunction


def get_ephemeral_store() -> EphemeralStore:
    """Create an ephemeral store of Python objects on-disk.

    :return: A tuple of store and iterate functions
    :rtype: Tuple[ClearFunction, StoreFunction, IteratorFunction]
    """
    folder: str = mkdtemp(dir=EPHEMERAL)

    async def clear() -> None:
        await rmdir(folder)

    async def store(obj: Any) -> None:
        await store_object(folder, obj, obj)

    async def iterate() -> AsyncIterator[Any]:
        for object_key in await recurse_dir(folder):
            yield await retrieve_object(folder, object_key)

    return EphemeralStore(
        clear=clear,
        store=store,
        iterate=iterate,
    )


async def reset() -> None:
    await rmdir(EPHEMERAL)
    await mkdir(EPHEMERAL, mode=0o700, exist_ok=True)
