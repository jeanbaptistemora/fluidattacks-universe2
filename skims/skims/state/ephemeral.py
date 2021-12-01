from aioextensions import (
    in_thread,
)
from os import (
    makedirs,
)
from os.path import (
    join,
)
from shutil import (
    rmtree,
)
from state.common import (
    read_blob,
    store_object,
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
    Optional,
    Tuple,
)
from utils.ctx import (
    STATE_FOLDER,
)
from utils.fs import (
    mkdir,
    recurse_dir,
)
from uuid import (
    uuid4 as uuid,
)

# Constants
EPHEMERAL: str = join(STATE_FOLDER, "ephemeral", uuid().hex)
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
    has_errors: Optional[bool] = False


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
            # Exception: WF(AsyncIterator is subtype of iterator)
            yield await in_thread(read_blob, object_key)  # NOSONAR

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
        has_errors=False,
    )


async def reset() -> None:
    await in_thread(rmtree, EPHEMERAL)
    await mkdir(EPHEMERAL, mode=0o700, exist_ok=True)
