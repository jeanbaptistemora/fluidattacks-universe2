from aioextensions import (
    in_thread,
)
from concurrent.futures.thread import (
    ThreadPoolExecutor,
)
from ctx import (
    STATE_FOLDER,
)
from os import (
    cpu_count,
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
    Awaitable,
    Callable,
    Iterator,
    NamedTuple,
    Optional,
    Tuple,
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
StoreFunction = Callable[[Any], None]
LengthFunction = Callable[[], int]
IteratorFunction = Callable[[], Iterator[Any]]

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

    def length() -> int:
        return len(recurse_dir(folder))

    def store(obj: Any) -> None:
        store_object(folder, obj, obj)

    def iterate() -> Iterator[Any]:
        with ThreadPoolExecutor(max_workers=cpu_count()) as worker:
            yield from worker.map(read_blob, recurse_dir(folder))

    async def get_a_few(count: int) -> Tuple[Any, ...]:
        results = []
        for obj in iterate():
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


def reset() -> None:
    rmtree(EPHEMERAL)
    mkdir(EPHEMERAL, mode=0o700, exist_ok=True)
