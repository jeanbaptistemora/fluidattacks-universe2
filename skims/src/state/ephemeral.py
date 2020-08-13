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
    read_blob,
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
LengthFunction = Callable[[], Awaitable[int]]
IteratorFunction = Callable[[], AsyncIterator[Any]]

# Side effects
makedirs(EPHEMERAL, mode=0o700, exist_ok=True)


class EphemeralStore(NamedTuple):
    clear: ClearFunction
    iterate: IteratorFunction
    length: LengthFunction
    store: StoreFunction


def get_ephemeral_store() -> EphemeralStore:
    """Create an ephemeral store of Python objects on-disk.

    :return: An object with read/write methods
    :rtype: EphemeralStore
    """
    folder: str = mkdtemp(dir=EPHEMERAL)

    async def clear() -> None:
        await rmdir(folder)

    async def length() -> int:
        return len(await recurse_dir(folder))

    async def store(obj: Any) -> None:
        await store_object(folder, obj, obj)

    async def iterate() -> AsyncIterator[Any]:
        for object_key in await recurse_dir(folder):
            yield await read_blob(object_key)

    return EphemeralStore(
        clear=clear,
        iterate=iterate,
        length=length,
        store=store,
    )


async def reset() -> None:
    await rmdir(EPHEMERAL)
    await mkdir(EPHEMERAL, mode=0o700, exist_ok=True)
