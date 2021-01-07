# Standard library
from os import (
    makedirs,
)
from os.path import (
    join,
)
from shutil import (
    rmtree,
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
    Tuple,
)
from uuid import (
    uuid4 as uuid,
)

# Third party libraries
from aioextensions import (
    in_thread
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
    recurse_dir,
)

# Constants
EPHEMERAL: str = join(STATE_FOLDER, 'ephemeral', uuid().hex)
ClearFunction = Callable[[], Awaitable[None]]
GetAFewFunction = Callable[[int], Awaitable[Tuple[Any, ...]]]
StoreFunction = Callable[[Any], Awaitable[None]]
LengthFunction = Callable[[], Awaitable[int]]
IteratorFunction = Callable[[], AsyncIterator[Any]]

# Side effects
makedirs(EPHEMERAL, mode=0o700, exist_ok=True)


class EphemeralStore(NamedTuple):
    clear: ClearFunction
    get_a_few: GetAFewFunction
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
        await in_thread(rmtree, folder)

    async def length() -> int:
        return len(await recurse_dir(folder))

    async def store(obj: Any) -> None:
        await in_thread(store_object, folder, obj, obj)

    async def iterate() -> AsyncIterator[Any]:
        for object_key in await recurse_dir(folder):
            yield await in_thread(read_blob, object_key)

    async def get_a_few(count: int) -> Tuple[Any, ...]:
        results = []
        async for obj in iterate():
            results.append(obj)
            if len(results) == count:
                break
        return tuple(results)

    return EphemeralStore(
        clear=clear,
        get_a_few=get_a_few,
        iterate=iterate,
        length=length,
        store=store,
    )


async def reset() -> None:
    await in_thread(rmtree, EPHEMERAL)
    await mkdir(EPHEMERAL, mode=0o700, exist_ok=True)
