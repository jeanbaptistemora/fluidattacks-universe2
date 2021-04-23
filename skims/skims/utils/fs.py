# Standard library
from glob import (
    iglob as glob,
)
from itertools import (
    chain,
)
from operator import (
    attrgetter,
    methodcaller,
)
import os
from typing import (
    Awaitable,
    Callable,
    Dict,
    Iterable,
    Set,
    Tuple,
)

# Third party imports
import aiofiles
from aioextensions import (
    collect,
    in_thread,
)

# Local libraries
from utils.concurrency import (
    never_concurrent,
)
from utils.logs import (
    log,
)


def generate_file_content(
    path: str,
    encoding: str = "latin-1",
    size: int = -1,
) -> Callable[[], Awaitable[str]]:
    data: Dict[str, str] = {}

    @never_concurrent
    async def get_one() -> str:
        if not data:
            data["file_contents"] = await get_file_content(
                path=path,
                encoding=encoding,
                size=size,
            )
        return data["file_contents"]

    return get_one


def generate_file_raw_content(
    path: str,
    size: int = -1,
) -> Callable[[], Awaitable[bytes]]:
    data: Dict[str, bytes] = {}

    @never_concurrent
    async def get_one() -> bytes:
        if not data:
            data["file_raw_content"] = await get_file_raw_content(path, size)
        return data["file_raw_content"]

    return get_one


async def get_file_content(
    path: str,
    encoding: str = "latin-1",
    size: int = -1,
) -> str:
    async with aiofiles.open(  # type: ignore
        path,
        mode="r",
        encoding=encoding,
    ) as file_handle:
        file_contents: str = await file_handle.read(size)

        return file_contents


async def get_file_raw_content(path: str, size: int = -1) -> bytes:
    async with aiofiles.open(  # type: ignore
        path,
        mode="rb",
    ) as file_handle:
        file_contents: bytes = await file_handle.read(size)

        return file_contents


async def mkdir(name: str, mode: int = 0o777, exist_ok: bool = False) -> None:
    return await in_thread(os.makedirs, name, mode=mode, exist_ok=exist_ok)


async def recurse_dir(path: str) -> Tuple[str, ...]:
    try:
        scanner = tuple(os.scandir(path))
    except FileNotFoundError:
        scanner = tuple()

    dirs = map(attrgetter("path"), filter(methodcaller("is_dir"), scanner))
    files = map(attrgetter("path"), filter(methodcaller("is_file"), scanner))

    tree: Tuple[str, ...] = tuple(
        chain(
            files,
            *await collect(map(recurse_dir, dirs)),
        )
    )

    return tree


async def recurse(path: str) -> Tuple[str, ...]:
    return (path,) if os.path.isfile(path) else await recurse_dir(path)


async def resolve_paths(
    *,
    exclude: Tuple[str, ...],
    include: Tuple[str, ...],
) -> Set[str]:
    def normpath(path: str) -> str:
        return os.path.normpath(path)

    def evaluate(path: str) -> Iterable[str]:
        if path.startswith("glob(") and path.endswith(")"):
            yield from glob(path[5:-1], recursive=True)
        else:
            yield path

    try:
        unique_paths: Set[str] = set(
            map(
                normpath,
                chain.from_iterable(
                    await collect(
                        map(
                            recurse,
                            chain.from_iterable(map(evaluate, include)),
                        )
                    ),
                ),
            )
        ) - set(
            map(
                normpath,
                chain.from_iterable(
                    await collect(
                        map(
                            recurse,
                            chain.from_iterable(map(evaluate, exclude)),
                        )
                    ),
                ),
            )
        )
    except FileNotFoundError as exc:
        raise SystemExit(f"File does not exist: {exc.filename}")
    else:
        await log("info", "Files to be tested: %s", len(unique_paths))

    return unique_paths
