from aioextensions import (
    collect,
    in_thread,
)
import aiofiles  # type: ignore
from fnmatch import (
    fnmatch as matches_glob,
)
from glob import (
    iglob as glob,
)
from itertools import (
    chain,
)
from model.graph_model import (
    GraphShardMetadataLanguage,
)
from operator import (
    attrgetter,
    methodcaller,
)
import os
from pyparsing import (
    Regex,
)
from typing import (
    Awaitable,
    Callable,
    Dict,
    Iterable,
    List,
    Set,
    Tuple,
)
from utils.concurrency import (
    never_concurrent,
)
from utils.logs import (
    log,
)


def decide_language(path: str) -> GraphShardMetadataLanguage:
    language_extensions_map: Dict[str, List[str]] = {
        GraphShardMetadataLanguage.CSHARP: [".cs"],
        GraphShardMetadataLanguage.GO: [".go"],
        GraphShardMetadataLanguage.JAVA: [".java"],
        GraphShardMetadataLanguage.JAVASCRIPT: [".js", ".jsx"],
        GraphShardMetadataLanguage.KOTLIN: [".kt", ".ktm", ".kts"],
        GraphShardMetadataLanguage.TSX: [".ts", ".tsx"],
    }
    language = GraphShardMetadataLanguage.NOT_SUPPORTED

    for lang, extensions in language_extensions_map.items():
        if any(path.endswith(ext) for ext in extensions):
            language = lang
            break

    return language


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
    async with aiofiles.open(
        path,
        mode="r",
        encoding=encoding,
    ) as file_handle:
        file_contents: str = await file_handle.read(size)

        return file_contents


async def get_file_raw_content(path: str, size: int = -1) -> bytes:
    async with aiofiles.open(path, mode="rb") as file_handle:
        file_contents: bytes = await file_handle.read(size)

        return file_contents


async def check_dependency_code(path: str) -> bool:
    language: GraphShardMetadataLanguage = decide_language(path)

    if language == GraphShardMetadataLanguage.JAVASCRIPT:
        regex_exp = [
            Regex(r"jQuery(.)*[Cc]opyright(.)*[Ll]icen"),
            Regex(r"[Cc]opyright(.)*[Ll]icen(.)*[Jj][Qq]uery"),
            Regex(r"[Aa]ngular[Jj][Ss](.)*[Gg]oogle(.)*[Ll]icen"),
        ]
    else:
        return False

    file_content = generate_file_content(path, size=200)
    raw_content = await file_content()
    content = raw_content.replace("\n", " ")

    for regex in regex_exp:
        for _ in regex.scanString(content):
            return True
    return False


async def get_non_upgradable_paths(paths: Set[str]) -> Set[str]:
    nu_paths: Set[str] = set()

    intellisense_refs = {
        os.path.dirname(path)
        for path in paths
        if path.endswith("Scripts/_references.js")
    }

    for path in paths:
        if (
            any(
                path.startswith(intellisense_ref)
                for intellisense_ref in intellisense_refs
            )
            or any(
                matches_glob(f"/{path}", glob)
                for glob in (
                    "*/Assets*/vendor/*",
                    "*/Assets*/lib/*",
                    "*/Assets*/js/*",
                    "*/Content*/jquery*",
                    "*/GoogleMapping*.js",
                    "*/Scripts*/bootstrap*",
                    "*/Scripts*/modernizr*",
                    "*/Scripts*/jquery*",
                    "*/Scripts*/popper*",
                    "*/Scripts*/vue*",
                    "*/wwwroot/lib*",
                )
            )
            or await check_dependency_code(path)
        ):
            nu_paths.add(path)

    return nu_paths


def get_non_verifiable_paths(paths: Set[str]) -> Set[str]:
    nv_paths: Set[str] = set()

    for path in paths:
        _, file = os.path.split(path)
        file_name, file_extension = os.path.splitext(file)
        file_extension = file_extension[1:]

        if (
            file_extension
            in {
                "aar",
                "apk",
                "bin",
                "class",
                "dll",
                "DS_Store",
                "exec",
                "hprof",
                "jar",
                "jasper",
                "pdb",
                "pyc",
                "exe",
            }
            or (file_name, file_extension)
            in {
                ("debug", "log"),
                ("org.eclipse.buildship.core.prefs"),
                (".classpath", ""),
                (".project", ""),
                (".vscode", ""),
            }
            or any(
                path.endswith(end)
                for end in (
                    ".cs.bak",
                    ".csproj.bak",
                    ".min.js",
                )
            )
            or any(
                string in path
                for string in (
                    "/.serverless_plugins/",
                    "/.settings/",
                )
            )
        ):
            nv_paths.add(path)

    return nv_paths


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
) -> Tuple[Set[str], Set[str], Set[str]]:
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

        # Exclude non-upgradable paths
        unique_nu_paths: Set[str] = await get_non_upgradable_paths(
            unique_paths
        )
        unique_paths.symmetric_difference_update(unique_nu_paths)

        # Exclude non-verifiable paths
        unique_nv_paths: Set[str] = get_non_verifiable_paths(unique_paths)
        unique_paths.symmetric_difference_update(unique_nv_paths)
    except FileNotFoundError as exc:
        raise SystemExit(f"File does not exist: {exc.filename}") from exc
    else:
        await log("info", "Files to be tested: %s", len(unique_paths))

    return unique_paths, unique_nu_paths, unique_nv_paths
